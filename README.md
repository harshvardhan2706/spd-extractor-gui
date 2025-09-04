# spd-extractor-gui

## Overview
Roland SPD Extractor GUI is a Python application for extracting WAV audio samples from Roland SPD (.SPD) files using a simple graphical interface.

## Features
- Select and extract WAV samples from .SPD files
- User-friendly PyQt5 GUI
- Progress bar and log area for extraction status
- Splash screen with logo

## How to Use
1. Run `python gui.py`.
2. Click "Choose .SPD File" and select your SPD file.
3. Choose a destination folder when prompted.
4. Extracted WAV files will be saved in a new folder named `<filename>_extracted`.

## Requirements
- Python 3.11 or newer
- PyQt5 (`pip install pyqt5`)

## File Structure

```
spd-extractor-gui/
├── extractor.py
├── gui.py
├── README.md
├── img/
│   └── spdlogo.png
├── __pycache__/
│   └── extractor.cpython-311.pyc
```

- `gui.py`: Main GUI application
- `extractor.py`: SPD file extraction logic
- `img/spdlogo.png`: Logo for splash screen

## License
MIT