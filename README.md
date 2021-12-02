

# AIAA Propulsive Landing Ground Control

This repository contains scripts and resources to monitor and control the launching of our rocket.

## Organization

 
|Folder|Contents|
|--|--|
|`live_monitoring`|Tools to communicate with rocket during a launch or test|
|`runs`|Data from past launches or tests
|`data_viewer`|Resources to analyze past data
|`structure_manager`|Tools to synchronize ground control with rocket 

## Test / Launch Usage

 1. Install python from [python.org](https://www.python.org/downloads/)
 2. Navigate to the `live_monitoring` folder in your terminal
 3. Run the command `python main.py` (A gui should appear)
 4. Enter the XBee dongle port name into the GUI (e.g. "COM11")
 5. Click the `Select Data Directory` button to select where you want the folder for the run to be generated.
 6. Click the `start recording` button in the GUI
 7. When the test or launch is complete, click `save and exit`
  
  ## Structure Synchronization
  
 1. Run `python structure_manager.py` in the `strucutre_manager` folder
 2. Modify the types, names, and numbers so it matches what is sent from the flight computer
 3. The structure is saved when closing the window

##  Analysis
 - To be completed

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.
