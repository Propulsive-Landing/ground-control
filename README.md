

# AIAA Propulsive Landing Ground Control

This repository contains scripts and resources to monitor and control the launching of our rocket.

## Display layout

<a href="https://uconnpl.weebly.com/avionics.html">
 <img src="https://user-images.githubusercontent.com/72774655/207448314-8606bf1a-ea82-4008-ab17-d0999dbd2d63.png" height="500px">
</a>

## Organization

 
|Folder|Contents|
|--|--|
|`live_monitoring`|Tools to communicate with rocket during a launch or test|
|`runs`|Data from past launches or tests
|`structure_manager`|Tools to synchronize ground control with rocket 

## First Time Initialization
 1. Install python3 from [python.org](https://www.python.org/downloads/)
 2. Install `poetry`: follow [poetry installation](https://python-poetry.org/docs/#installing-with-the-official-installer).
 3. Install dependencies: `poetry install`

## Test / Launch Usage

 1. Run the command `poetry run python3 live_monitoring/gui.py` (A gui should appear)
 2. If default values are not automatically filled in:
     1. Click the `Select Struct Defintion Directory` button to select where the incoming structure is defined. (It will almost always be in `./structure_manager/data` folder)
     2. Click the `Select Output Directory` to determine where the output folder will be generated.
 3. Enter the XBee dongle port name into the GUI (e.g. "COM11")
 4. Click `Connect Serial and Listen` to begin listening for data
 5. Click `Stop Listening and Save` to stop listening (cannot be resumed)
 6. Click `Reset and Save Graphs` when you are done looking at your graphs and want to begin another trial.
     * `Reset and Discard` will delete all files related to most recent run
  
  ## Structure Synchronization
  
 1. Run `python structure_manager.py` in the `strucutre_manager` folder
 2. Modify the types, names, and numbers so it matches what is sent from the flight computer
 3. The structure is saved when closing the window

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.
