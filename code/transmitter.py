import rtmidi
from rtmidi.midiconstants import NOTE_ON

class Transmitter:
	def __init__(self, midi):
		self.midi = midi

	def send(self, command, note, velocity, channel=0):
		command = (command & 0xf0) | (channel & 0xf)
		self.midi.send_message([command, note, velocity])