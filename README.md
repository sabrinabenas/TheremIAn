# TheremIAn: A Theremin Controlled by Computer Vision and Artificial Intelligence

**TheremIAn** is an interactive application that allows you to control the pitch and volume of sound in real-time using body movements detected by **DeepLabCut Live!** through a webcam. Inspired by the classic electronic instrument *Theremin*, **TheremIAn** transforms gestures into sound using computer vision and audio synthesis in Python.

---

## Overview

Theremian uses:

- **DeepLabCut Live!** to detect hand position in space.
- **PyAudio** to generate real-time audio.
- Different sound synthesis modes (continuous, pentatonic, spectral).
- Control of **frequency** and **volume** based on the position and confidence of the tracking.

The result is a contactless digital instrument that responds to gestures in front of the camera.

---

## Requirements

- Python 3.x
- DeepLabCut Live!
- OpenCV (`opencv-python`)
- PyAudio (`pyaudio`)
- Numpy

Recommended package installation:

```bash
pip install opencv-python pyaudio numpy
```

Additionally, make sure you have **DeepLabCut Live!** correctly set up in your environment (with gpu).

---

## Project Structure

```
theremian/
│
├── theremian.py      # Main code
├── dlc_model/        # Folder with the DeepLabCut model (download from DLC)
└── README.md         # Documentation (this file)
```

---

## Sound Modes Available

1. **Continuous:** The frequency varies smoothly based on the horizontal position of the hand.
2. **Pentatonic:** Positions are mapped to notes of a pentatonic scale based on A (A4 = 440 Hz).
3. **Spectral (Spectrum):** A harmonic-rich variant with multiple overtones.

Select the sound mode by changing the `sonido` variable:

```python
sonido = 'continuo'     # or 'pentatonica' or 'spectrum'
```

---

## Controls

| Movement                | Effect                                                        |
| ----------------------- | ------------------------------------------------------------- |
| **Hand left/right (X)** | Controls the **frequency** of the sound.                      |
| **Hand up/down (Y)**    | Controls the **volume** of the sound (higher = lower volume). |

Note: The system uses body keypoints detected by DeepLabCut. In this example, points `6` and `11` (e.g., wrist and elbow) are used — you may adjust these according to your model.

---

## How It Works

1. **Video Capture:** Uses `cv2.VideoCapture` to obtain real-time images.
2. **Pose Detection:** DeepLabCut predicts body part positions in each frame.
3. **Audio Control:**
   - Horizontal position (X) modifies sound frequency.
   - Vertical position (Y) adjusts volume based on vertical distance.
4. **Sound Generation:** Using `PyAudio`, it generates real-time audio with sine wave or harmonic synthesis.

---

## How to Use

1. Place your **DeepLabCut Live!** model in the appropriate folder (or in the project root).
2. Open the `theremian.py` script and select the desired sound mode.
3. Run the script:

```bash
python theremian.py
```

4. Move in front of the webcam to control the sound.
5. Press **q** to exit.

---

## Technical Notes

- The **DLCLive** display module was modified for improved visualization (`display=True` in `DLCLive`).
- The audio buffer is 256 samples to minimize latency.
- The `Normalized_phase` function ensures phase continuity when frequency changes, avoiding audible glitches.

---

## Possible Improvements

- Multi-user or multi-gesture mode.
- MIDI output or virtual instrument control.

---
