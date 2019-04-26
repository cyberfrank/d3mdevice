SPLIT_RIGHT = 0
SPLIT_LEFT = 1
CONTROL_CHANNEL = 2
NUM_SPLIT_ZONES = 6

import math
from modes import TrackArmMode, DetuneMode, OctaveMode, SplitMode, MomentaryMode, TriggerMode
from transmitter import Transmitter
from rtmidi.midiconstants import NOTE_ON
	
class D3MDevice:
	def __init__(self, midiIn, midiOut, loopback):
		self.midiIn = midiIn
		self.ledControl = Transmitter(midiOut)
		self.transmitter = Transmitter(loopback)

		self.activeMode = None
		self.activeBank = 0
		self.buttonState = [False] * 12
		self.detune = 0
		self.octave = [0, 0]
		self.splitZone = 0

		self.blackKeyIndices = [
			1, 3, 6, 8, 10,
		]

		# setup modes
		self.modes = []
		self.modes.insert(0, TrackArmMode(0)) 			# track arm
		self.modes.insert(1, TrackArmMode(1)) 			# track arm
		self.modes.insert(2, SplitMode())				# select split zone
		self.modes.insert(3, OctaveMode())				# octave channel 2 and 1
		self.modes.insert(4, DetuneMode())				# detune all channels
		self.modes.insert(6, TrackArmMode(2)) 			# track arm
		self.modes.insert(7, TrackArmMode(3)) 			# track arm
		self.modes.insert(8, MomentaryMode(4)) 			# momentary buttons (dual fire event)
		self.modes.insert(9, TriggerMode(5))			# trigger buttons (single fire event)

		for mode in self.modes:
			mode.register(self)

		# set initial mode on start
		self.set_mode(0)

	def update(self):
		message = self.midiIn.get_message()

		if message is None:
			return

		command = message[0][0]
		note = message[0][1]
		velocity = message[0][2]

		# undefined command, send to both channels
		if command != NOTE_ON:
			self.transmitter.send_message(command, note, velocity, SPLIT_LEFT)
			self.transmitter.send_message(command, note, velocity, SPLIT_RIGHT)
			return

		# check if keybed is pressed
		if note >= 36 and note <= 96:
			# adjust velocity
			if (note % 12) in self.blackKeyIndices and velocity > 0:
				velocity -= (int)(math.log(velocity) * 2)
				velocity = max(velocity, 0)

			# select output channel
			zone = ((note - 36) / 12) % NUM_SPLIT_ZONES
			# detune note
			note += self.detune
			# select zone
			if zone >= self.splitZone:
				note += self.octave[SPLIT_RIGHT] * 12
				self.transmitter.note_on(note, velocity, SPLIT_RIGHT)
			else:
				note += self.octave[SPLIT_LEFT] * 12
				self.transmitter.note_on(note, velocity, SPLIT_LEFT)

		# check preset buttons
		elif note >= 0  and note < 12:
			if not self.buttonState[note] and velocity == 127:
				self.activeMode.on_preset_pressed(note)
			elif self.buttonState[note] and velocity == 0:
				self.activeMode.on_preset_released(note)

		# check preset banks
		elif note >= 14 and note < 24 and velocity == 127:
			bankIndex = note - 14
			if bankIndex != self.activeBank:
				self.set_mode(bankIndex)
				self.activeBank = bankIndex

	def transmit_message(self, note):
		self.transmitter.send(note, 127, CONTROL_CHANNEL)

	def toggle_light(self, number, lightOn = True):
		self.ledControl.note_on(number, 127 if lightOn else 0)
		self.buttonState[number] = lightOn

	def clear_lights(self):
		for i in range(12):
			self.toggle_light(i, False)

	def toggle_bank(self, bank):
		for i in range(10):
			self.ledControl.note_on(i + 14, 0)
		self.ledControl.note_on(bank + 14, 127)

	def set_mode(self, bankIndex):
		self.toggle_bank(bankIndex)

		if self.modes[bankIndex] is not self.activeMode:
			self.clear_lights()
			self.activeMode = self.modes[bankIndex]
			self.activeMode.on_enter()

	def close(self):
		self.clear_lights()
		for i in range(10):
			self.ledControl.note_on(i + 14, 0)