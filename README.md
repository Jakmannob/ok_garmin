# ok_garmin

Simple Python-based voice recognition tool to save NVIDIA instant replay

The voice model runs in the background and continuously checks for the _"OK Garmin"_ voice command.
Once an _"OK Garmin"_-command was heard, it will listen for a follow-up command.
If the follow-up is _"Video speichern"_, the default NVIDIA instant replay hotkey will be executed, i.e. `Alt`+`F10`.

## Setup and installation

1. Set up a Python environment and install [`requirements.txt`](./requirements.txt)
2. Run [`print_mic_ids.py`](./print_mic_ids.py) and note your preferred microphone device ID
3. Modify the `INPUT_DEVICE_ID` in [`ok_garmin.py`](./ok_garmin.py) accordingly

## Running the application

Activate your environment and run `python ok_garmin.py` in the base directory.
It will download the voice recognition model on the first run and place it in a new `model` directory.
After that, the main loop is run until the application is killed.
