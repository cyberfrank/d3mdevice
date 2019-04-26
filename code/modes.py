from device import SPLIT_LEFT, SPLIT_RIGHT, NUM_SPLIT_ZONES

class Mode:
	def register(self, d3m):
		self.d3m = d3m

	def on_enter(self):
		pass

	def on_preset_pressed(self, number):
		pass

	def on_preset_released(self, number):
		pass

class TrackArmMode(Mode):
	def __init__(self, offset):
		self.currSelection = 0
		self.prevSelection = 0
		self.offset = offset + 1

	def on_enter(self):
		self.d3m.toggle_light(self.currSelection)

	def on_preset_pressed(self, number):
		self.prevSelection = self.currSelection
		self.currSelection = number

		self.d3m.clear_lights()
		self.d3m.toggle_light(number)

		self.d3m.transmit_message(self.prevSelection * self.offset)
		self.d3m.transmit_message(self.currSelection * self.offset)

class DetuneMode(Mode):
	def __init__(self):
		self.currDetune = 0

	def on_enter(self):
		self.d3m.toggle_light(self.currDetune)

	def on_preset_pressed(self, number):
		self.currDetune = number
		self.d3m.detune = self.currDetune

		self.d3m.clear_lights()
		self.d3m.toggle_light(number)

class OctaveMode(Mode):
	def __init__(self):
		self.currOctave = [9, 4]

	def on_enter(self):
		self.d3m.toggle_light(self.currOctave[SPLIT_LEFT])
		self.d3m.toggle_light(self.currOctave[SPLIT_RIGHT])

	def on_preset_pressed(self, number):
		if number > 5:
			self.currOctave[SPLIT_RIGHT] = number
			# convert to range (-3 -> 2)
			self.d3m.octave[SPLIT_RIGHT] = number - 9
		else:
			self.currOctave[SPLIT_LEFT] = number
			# convert to range (-3 -> 2)
			self.d3m.octave[SPLIT_LEFT] = number - 3

		self.d3m.clear_lights()
		self.d3m.toggle_light(self.currOctave[SPLIT_LEFT])
		self.d3m.toggle_light(self.currOctave[SPLIT_RIGHT])

class SplitMode(Mode):
	def __init__(self):
		self.currZone = 0

	def on_enter(self):
		self.d3m.toggle_light(self.currZone)

	def on_preset_pressed(self, number):
		if number < NUM_SPLIT_ZONES:
			self.currZone = number
			self.d3m.splitZone = self.currZone

			self.d3m.clear_lights()
			self.d3m.toggle_light(number)

class MomentaryMode(Mode):
	def __init__(self, offset):
		self.offset = offset + 1

	def on_preset_pressed(self, number):
		self.d3m.toggle_light(number, True)
		self.d3m.transmit_message(number * self.offset)

	def on_preset_released(self, number):
		self.d3m.toggle_light(number, False)
		self.d3m.transmit_message(number * self.offset)

class TriggerMode(Mode):
	def __init__(self, offset):
		self.offset = offset + 1

	def on_preset_pressed(self, number):
		self.d3m.toggle_light(number, True)
		self.d3m.transmit_message(number * self.offset)

	def on_preset_released(self, number):
		self.d3m.toggle_light(number, False)