import pygame
import pyaudio
import numpy as np
import math
import itertools
import struct
from time import time

# Configuración de Pygame
pygame.init()
ancho = 800
largo = 600
screen = pygame.display.set_mode((ancho, largo))
pygame.display.set_caption("Generación de Sonidos basada en la Posición del Mouse")
clock = pygame.time.Clock()

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

def Normalized_phase(phase):
    return phase + np.ceil(-phase * 0.5 / np.pi) * 2 * np.pi

#No termine usando esta funcion, si no que meti cosas adentro del callback
def Frequency_shift(Frequency,newFrequency,offset,timeStep,phase):
    newFrequency = max([0,newFrequency])
    if newFrequency != Frequency:
        phase = Normalized_phase(offset * timeStep * 2 * np.pi * ( Frequency - newFrequency ) + phase)
        Frequency = newFrequency
    return phase, Frequency

def generate_sound(Frequency,offset,phase,buffer_length,volume):
    
    xs = np.arange(fs * duration)##(0,buffer_length-1) 
    omega = 2 * np.pi * Frequency
    samples = (np.sin( (xs+offset) * omega / fs + phase)).astype(np.float32)
    
    return samples*volume


def callback(in_data, frame_count, time_info, status):
    global TT,phase,Frequency,newFrequency
    if newFrequency != Frequency:
        phase = 2*np.pi*TT*(Frequency-newFrequency)+phase
        phase = Normalized_phase(phase)
        Frequency=newFrequency
    left = (np.sin(phase+2*np.pi*Frequency*(TT+np.arange(frame_count)/float(fs))))
    data = np.zeros((left.shape[0]*2,),np.float32)
    data[::2] = left
    data[1::2] = left
    TT+=frame_count/float(fs)
    return (data, pyaudio.paContinue)


# def callback(input_data, frame_count, time_info, status):
# #    return (data.tostring(), pyaudio.paContinue)
#     x_max = 2*np.pi
#     omega = 2 * np.pi * Frequency
#     if fs*omega < x_max:  #tf
#         data, _ = generate_sound(Frequency,offset,phase,buffer_length,volume)  #tf
#         return (data.tostring(), pyaudio.paContinue)
#     else:
#         return (None, pyaudio.paComplete)


##Julian, o lo que deje medio tocado de lo que estaba
# def get_samples(notes_dict, num_samples=buffer_length):
#     return [
#         sum([int(next(osc) * 32767) for _, osc in notes_dict.items()])
#         for _ in range(num_samples)
#     ]


# def get_sin_oscillator(freq=Frequency, amp=1, sample_rate=fs):
#     increment = (2 * math.pi * freq) / sample_rate
#     return (
#         math.sin(v) * amp * 0.1 for v in itertools.count(start=0, step=increment)
#     )



def dibujar(sound, Frequency):
    screen.fill((0,0,0))
    points = [(x,200*y+200) for x,y in enumerate(sound)]
#    points= []
#    for x in range(ancho):
#        y = largo/2 + int (200 * math.sin(0.0002* Frequency*x))
#        points.append((x,y))
        
    pygame.draw.lines(screen, (255,255,255), False, points, 2) 
    pygame.display.flip()
    


stream = p.open(format=pyaudio.paFloat32,  ##paInt16 para lo nuevo
                channels=2,
                rate=fs,
                output=True,
                frames_per_buffer=buffer_length,
                stream_callback=callback)

running = True
duration = 0.1  # Duración de la onda en segundos
iterator = 0
notes_dict = {}
stream.start_stream()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición del mouse en X
    mouse_x = pygame.mouse.get_pos()[0]

    # Calcular la frecuencia del sonido basada en la posición del mouse
    newFrequency = 10 + (mouse_x / 800) * 1000  # Rango de frecuencia de 100 a 1100 Hz
    
    #phase, Frequency = Frequency_shift(Frequency,newFrequency,offset,timeStep,phase)
   
    # Generar el sonido
    sound = generate_sound(Frequency,offset,phase,buffer_length,volume)
    
    iterator =+ 1
    offset = buffer_length * iterator
    # Reproducir el sonido
    #stream.write(sound.tobytes())
    dibujar(sound, Frequency)
    
    #Cabeza de Julian
    #notes_dict[iterator] = get_sin_oscillator(freq=Frequency, amp=1)
    #recorte = get_samples(notes_dict)
    #recorte = np.int16(recorte).tobytes()
    #stream.write(recorte)
    #dibujar(sound, Frequency)
    
    # Refrescar la pantalla
    #pygame.display.flip()
    clock.tick(10)

# Cerrar PyAudio
stream.stop_stream()
stream.close()
p.terminate()

pygame.quit()

#%%

import pyaudio
from time import time

CHANNELS = 2



phase = 0


# p = pyaudio.PyAudio()

# stream = p.open(format=pyaudio.paFloat32,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 output=True,
#                 stream_callback=callback)

# stream.start_stream()
# start = time()
# try:
#     while 1:
#         now = time()     
#         if now-start>1/24.:
#             newfreq=200+np.sin(2*np.pi*1/20.*now)*100 #update the frequency This will depend on y on the future
#             print (newfreq)
#         start=now
# finally:
#     stream.stop_stream()
#     stream.close()
#     p.terminate()