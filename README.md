# d3mdevice

![](https://i.imgur.com/dp9ROJl.png)

## Introduction
This software was created to allow the Doepfer D3M keyboard to control parameters, change MIDI settings and arm instruments on the fly, using only the onboard buttons.

The interface takes inputs from the D3M, modifies them and outputs them to some loopback MIDI interface. This makes it possible to modify the MIDI data before it reaches a sound generator. The software also focuses on making the onboard LEDs actually function in various modes. There is also some multiplexing of outputs using the preset banks, which gives a lot more control surface.

## Requirements
* Python 3+
* A loopback MIDI interface

## Features
* Simple and fast integration
* Keybed split zones for dual channel note transmission
* Correct LED feedback
* Onboard detune and octave modification
* Velocity correction
* Various modes for DAW remote control

## Available Modes
A mode can be assigned to any available preset bank of choice. The configuration of various modes may be set however you like.

### Track Arm Mode
* Select a single preset between 1-12
* Outputs message for pressed button and previous button
* Useful to arm track and switch instruments

### Split Mode
* Splits the keybed into two channels
* Select a split zone between any octave
* Useful when playing two instruments at once

### Detune Mode
* Detunes outgoing keyboard data
* Select a offset using the number buttons
* Can modify both output channels independently

### Momentary Mode
* Press and release buttons to fire consequent MIDI commands
* Useful for DAW remote control

### Octave Mode
* Changes the octave output of the keyboard
* Select higher or lower octaves using the number buttons
* Select the octave for both zones independetly

### Trigger Mode
* Press to fire a single MIDI command
* Useful for DAW remote control
