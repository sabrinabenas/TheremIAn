from dlclive import DLCLive, Processor
import cv2
import pyaudio
import numpy as np
import math
import itertools
import struct
from time import time

#obs: modifique el display del dlclive en miniconda3\envs\cudnn_env1\Lib\site-packages\dlclive

def sonido_continuo(phase,Frequency,TT,frame_count,fs,volume):
    return (np.sin(phase+2*np.pi*Frequency*(TT+np.arange(frame_count)/float(fs)))) * volume


def pentatonica(f0,octavas = 3):
    potencias = np.cumsum([3,2,2,3,2])
    return [f0 / (octavas - 1)] + [f0 * 0.5 * 2 ** ((n + potencias[-1] * i) / 12) for i in range(octavas) for n in potencias] + [f0 * (octavas - 1)]

notas = pentatonica(440,3)
sonido = 'spectrum' #'continuo', 'pentatonica', 'spectrum'

def sonido_spectrum(phase,Frequency,TT,frame_count,fs,volume):
    left = 0
    for n in range(1,3):
        left += np.sin(phase+2*np.pi*Frequency*n*(TT+np.arange(frame_count)/float(fs))) / n
    return left * volume


def Normalized_phase(phase):
    return phase + np.ceil(-phase * 0.5 / np.pi) * 2 * np.pi

def callback(in_data, frame_count, time_info, status):
    global TT,phase,Frequency,newFrequency,volume,sonido
    if newFrequency != Frequency:
        phase = 2*np.pi*TT*(Frequency-newFrequency)+phase
        phase = Normalized_phase(phase)
        Frequency=newFrequency

    if sonido == 'continuo':    
        left = sonido_continuo(phase,Frequency,TT,frame_count,fs,volume)
    if sonido == 'spectrum':
        left = sonido_spectrum(phase,Frequency,TT,frame_count,fs,volume) #que spectrum sea caract de cont o pent
    if sonido == 'pentatonica':
        left = sonido_continuo(phase,Frequency,TT,frame_count,fs,volume)

    data = np.zeros((left.shape[0]*2,),np.float32)
    data[::2] = left
    data[1::2] = left
    TT+=frame_count/float(fs)
    return (data, pyaudio.paContinue)

def amplitud(value,confidence):
    if confidence>0.5:
        volum = max((350-value)*0.005,0) #puede llegar hasta 1 :)
        if volum > 1:
            return 0.99
        else: 
            return volum
    return 0

# Configuración de PyAudio
p = pyaudio.PyAudio()
fs = 44100    # Frecuencia de muestreo (samples por segundo)
buffer_length = 256
volume = 0.5  # Volumen del sonido
timeStep = 1 / fs
offset = 0
phase = 0
Frequency = 55
newFrequency = 55
TT = time()
duration = 1
stream = p.open(format=pyaudio.paFloat32,  ##paInt16 para lo nuevo
                channels=2,
                rate=fs,
                output=True,
                frames_per_buffer=buffer_length,
                stream_callback=callback)

dlc_proc = Processor()
dlc_live = DLCLive(".", processor=dlc_proc, display=True)

  
# define a video capture object
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if vid.isOpened(): # try to get the first frame
    rval, frame = vid.read()
    dlc_live.init_inference(frame)
    print('hola')
else:
    rval = False


while(True):
      
    # Capture the video frame
    ret, frame = vid.read()

    pose = dlc_live.get_pose(frame)
    
    #print(pose[6,0])
    mun_x = pose[6,0]
    mun_y = pose[11,1]
    confidence = pose[11,2]

    volume = amplitud(mun_y,confidence)


    # Calcular la frecuencia del sonido basada en la posición del mouse
    if sonido == 'pentatonica':        
        newFrequency = notas[np.argmin([np.abs(10 + (mun_x / 800) * 250 - nota) for nota in notas])] 
    if sonido == 'continuo':
        newFrequency = 10 + (mun_x / 800) * 250  # Rango de frecuencia de 100 a 1100 Hz
    if sonido == 'spectrum':
        newFrequency = 10 + (mun_x / 800) * 250  # Rango de frecuencia de 100 a 1100 Hz

    if cv2.waitKey(1) == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

