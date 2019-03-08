# d3mdevice

![](https://i.imgur.com/dp9ROJl.png)

## Introduction
This software was created to allow the Doepfer D3M keyboard to control parameters, change MIDI settings and arm instruments on the fly, using only the onboard buttons.

The interface takes inputs from the D3M, modifies them and outputs them to some loopback MIDI interface. This makes it possible to modify the MIDI data before it reaches a sound generator. The software also focuses on making the on-board LEDs actually function in various modes. There is also some multiplexing of outputs using the preset banks, which gives a lot more control surface.

## Requirements
* Python 3+
* A loopback MIDI interface

## Features
* Simple and fast integration
* Correct LED feedback
* Onboard detune and octave modification
* Velocity fix for the black keys*
* Various modes for DAW remote control

\* a common velocity issue occuring on FATAR keybeds

## Control Modes
### Track Arm Mode
Preset Bank 1-2
* Select a single preset between 1-12
* Outputs message for pressed button and previous button
* Useful to arm track and switch instruments
* Allows for a total of 24 tracks

### Control Mode
Preset Bank 3-4
* Toggle any preset between 1-12
* Outputs message for pressed button
* Useful to toggle effects and switches

### Detune Mode
Preset Bank 5
* Detunes outgoing keyboard data
* Preset number 8 represents the C key and 12 is the E key
* If the bank is changed, the latest selection will be used

### Octave Mode
Preset Bank 6
* Changes the octave output of the keyboard
* Select higher or lower octaves using the number buttons (preset 8 is the default setting)

### Daisy Chain Mode
Preset Bank 7-10
* Reserved for secondary keyboard
* Not yet released!
