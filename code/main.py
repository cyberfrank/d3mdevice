import sys
import time
from device import D3MDevice
from rtmidi.midiutil import open_midiport
from modes import *

# setup modes
modes = []
modes.append(TrackArmMode(0))
modes.append(TrackArmMode(1))
modes.append(TriggerMode(2))
modes.append(TriggerMode(3))
modes.append(MomentaryMode(4))
modes.append(MomentaryMode(5))
modes.append(SplitMode())		# select split zone
modes.append(OctaveMode())		# octave channel 2 and 1
modes.append(DetuneMode())		# detune all channels
modes.append(TestMode())		# experimental

try:
	print('\nSELECT D3M MIDI IN')
	midi_in, input_name = open_midiport(None, 'input')
	print('\nSELECT D3M MIDI OUT')
	midi_out, output_name = open_midiport(None, 'output')
	print('\nSELECT MIDI LOOPBACK')
	loopback, virtual_name = open_midiport(None, 'output')
except (EOFError, KeyboardInterrupt):
	sys.exit()

device = D3MDevice(midi_in, midi_out, loopback, modes)
try:
	while True:
		device.update()
except KeyboardInterrupt:
	pass
finally:
	device.close()
