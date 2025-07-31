# ok_garmin

Simple Python-based voice recognition tool to save NVIDIA instant replay

The voice model runs in the background and continuously checks for the _"OK Garmin"_ voice command.
Once an _"OK Garmin"_-command was heard, it will listen for a follow-up command.
If the follow-up is _"Video speichern"_, the default NVIDIA instant replay hotkey will be executed, i.e. `Alt`+`F10`.

## Setup and installation

See _Detailed installation guide for Windows users_, if you've never set up a Python project. Otherwise:

1. Set up a Python environment and install [`requirements.txt`](./requirements.txt)
2. Run [`print_mic_ids.py`](./print_mic_ids.py) and note your preferred microphone device ID
3. Modify the `INPUT_DEVICE_ID` in [`ok_garmin.py`](./ok_garmin.py) accordingly

## Running the application

Activate your environment and run `python ok_garmin.py` in the base directory.
It will download the voice recognition model on the first run and place it in a new `model` directory.
After that, the main loop is run until the application is killed.

## Detailed installation guide for Windows users

In case all of this is new to you, here's a detailed installation guide for Windows machines:

1. Install git and download project
    1. Download the latest x64 Setup from the [git webpage](https://git-scm.com/downloads/win)
    2. Run and install it
    3. On this GitHub page, open _Code > Clone > HTTPS_ and copy the link
    4. Open Git GUI and select _Clone Existing Repository_
    5. Enter the copied link into the _source location_ field, and the directory to where you want to install the project into the _target directory_ field
    6. You can then close the Git GUI
2. Install Python and set up environment
    1. Open the Microsoft Store
    2. Install the latest Python version
    3. Navigate to the project directory with Windows Explorer
    4. _Right click > Open in Terminal_
    5. Run `Python -m venv venv` in the project base directory (`ok_garmin`)
    6. Run `.\venv\Scripts\activate.bat`
    7. Run `Python -m pip install -r requirements.txt`
    8. Now your environment is set up and you can close the terminal. For future re-activations, you can skip every step except `2.vi.`
3. Set up the microphone device ID
    1. Run `Python print_mic_ids.py`
    2. Note the ID of your microphone (usually 1)
    3. Open `ok_garmin.py` with a text editor (_select > Open with > Notepad_)
    4. Modify the line `INPUT_DEVICE_ID = -1` by changing `-1` to your microphone ID
    5. Save and close
4. Running the application
    1. Do steps `2.iii.`, `2.iv.` and `2.vi.` 
    2. Then run `Python ok_garmin.py`
    3. Accept microphone access for Python (in pop-up window)
    4. Terminate application by closing the terminal or `Ctrl+C`
