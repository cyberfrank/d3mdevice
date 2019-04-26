import sys
import time
from device import D3MDevice
from rtmidi.midiutil import open_midiport

# TODO: add custom selection screen
try:
    midiin, input_name = open_midiport(None,'input')
    midiout, output_name = open_midiport(None, 'output')
    loopback, virtual_name = open_midiport(None, 'output')
except (EOFError, KeyboardInterrupt):
    sys.exit()

device = D3MDevice(midiin, midiout, loopback)
try:
	while True:
		device.update()
except KeyboardInterrupt:
	pass
finally:
	device.close()