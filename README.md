# d3mdevice

![](https://i.imgur.com/dp9ROJl.png)

## Introduction
This software was created to allow the Doepfer D3M keyboard to control parameters, change MIDI settings and arm instruments on the fly, using only the onboard buttons.

The interface takes inputs from the D3M, modifies them and outputs them to a loopback MIDI interface. This makes it possible to modify the MIDI data before it reaches the sound generator. The software also focuses on making the onboard LEDs actually function in various modes. There is also multiplexing of outputs using the preset banks, which gives a lot more control surface.

## Requirements
* Python 3+
* A loopback MIDI interface

## Features
* Simple and fast integration
* Keybed split zones for dual channel note transmission
* LED feedback
* Onboard detune and octave shift
* Velocity correction (fixes common FATAR waterfall keybed issue)
* Different DAW remote control modes
