SPLIT_RIGHT = 0
SPLIT_LEFT = 1
CONTROL_CHANNEL = 2
NUM_SPLIT_ZONES = 6

import math
from transmitter import Transmitter
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF
	
class D3MDevice:
	def __init__(self, midi_in, midi_out, loopback, modes):
		self.midi_in = midi_in
		self.led_control = Transmitter(midi_out)
		self.transmitter = Transmitter(loopback)

		self.active_mode = None
		self.active_bank = 0
		self.button_state = [False] * 12
		self.detune = 0
		self.octave = [0, 0]
		self.split_zone = 0

		self.black_key_indices = [
			1, 3, 6, 8, 10,
		]

		self.modes = modes
		for mode in self.modes:
			mode.register(self)

		# set initial mode on start
		self.set_mode(0)
		print('Ready!')

	def update(self):
		message = self.midi_in.get_message()

		if message is None:
			return

		command 	= message[0][0]
		note 		= message[0][1]
		velocity 	= message[0][2]

		# undefined command, send to both channels
		if command != NOTE_ON:
			self.transmitter.send(command, note, velocity, SPLIT_LEFT)
			self.transmitter.send(command, note, velocity, SPLIT_RIGHT)
			return

		# check if keybed is pressed
		if note >= 36 and note <= 96:
			# adjust velocity
			if (note % 12) in self.black_key_indices and velocity > 0:
				velocity -= (int)(math.log(velocity) * 2)
				velocity = max(velocity, 0)
			# select output channel
			zone = ((note - 36) / 12) % NUM_SPLIT_ZONES
			# detune note
			note += self.detune
			# select zone
			if zone >= self.split_zone:
				note += self.octave[SPLIT_RIGHT] * 12
				self.transmitter.send(NOTE_ON, note, velocity, SPLIT_RIGHT)
			else:
				note += self.octave[SPLIT_LEFT] * 12
				self.transmitter.send(NOTE_ON, note, velocity, SPLIT_LEFT)
		# check preset buttons
		elif note >= 0 and note < 12:
			if not self.button_state[note] and velocity == 127:
				self.active_mode.on_preset_pressed(note)
			elif self.button_state[note] and velocity == 0:
				self.active_mode.on_preset_released(note)
		# check preset banks
		elif note >= 14 and note < 24 and velocity == 127:
			bank_index = note - 14
			if bank_index != self.active_bank:
				self.set_mode(bank_index)
				self.active_bank = bank_index

	def cc_send_on(self, note):
		self.transmitter.send(NOTE_ON, note, 127, CONTROL_CHANNEL)

	def cc_send_off(self, note):
		self.transmitter.send(NOTE_OFF, note, 127, CONTROL_CHANNEL)

	def toggle_light(self, number, state = True):
		self.led_control.send(NOTE_ON, number, 127 if state else 0)
		self.button_state[number] = state

	def clear_lights(self):
		for i in range(12):
			self.toggle_light(i, False)

	def set_mode(self, bank_index):
		# set bank lights
		for i in range(10):
			self.led_control.send(NOTE_ON, i + 14, 0)
		self.led_control.send(NOTE_ON, bank_index + 14, 127)

		if self.modes[bank_index] is not self.active_mode:
			self.clear_lights()
			self.active_mode = self.modes[bank_index]
			self.active_mode.on_enter()

	def close(self):
		self.clear_lights()
		for i in range(10):
			self.led_control.send(NOTE_ON, i + 14, 0)
