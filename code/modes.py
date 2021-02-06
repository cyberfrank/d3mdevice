from device import SPLIT_LEFT, SPLIT_RIGHT, NUM_SPLIT_ZONES

class Mode:
	def register(self, d3m):
		self.d3m = d3m

	def on_enter(self):
		pass

	def on_preset_pressed(self, idx):
		pass

	def on_preset_released(self, idx):
		pass

class TrackArmMode(Mode):
	def __init__(self, offset):
		self.current = 0
		self.last = 0
		self.offset = offset

	def on_enter(self):
		self.d3m.toggle_light(self.current)

	def on_preset_pressed(self, idx):
		self.last = self.current
		self.current = idx

		self.d3m.clear_lights()
		self.d3m.toggle_light(idx)

		self.d3m.cc_send_on(self.last + (12 * self.offset))
		self.d3m.cc_send_on(self.current + (12 * self.offset))

class DetuneMode(Mode):
	def __init__(self):
		self.detune = 0

	def on_enter(self):
		self.d3m.toggle_light(self.detune)

	def on_preset_pressed(self, idx):
		self.detune = idx
		self.d3m.detune = idx
		self.d3m.clear_lights()
		self.d3m.toggle_light(idx)

class OctaveMode(Mode):
	def __init__(self):
		self.octave = [9, 4]

	def on_enter(self):
		self.d3m.toggle_light(self.octave[SPLIT_LEFT])
		self.d3m.toggle_light(self.octave[SPLIT_RIGHT])

	def on_preset_pressed(self, idx):
		if idx > 5:
			self.octave[SPLIT_RIGHT] = idx
			# convert to range (-3 -> 2)
			self.d3m.octave[SPLIT_RIGHT] = idx - 9
		else:
			self.octave[SPLIT_LEFT] = idx
			# convert to range (-3 -> 2)
			self.d3m.octave[SPLIT_LEFT] = idx - 3

		self.d3m.clear_lights()
		self.d3m.toggle_light(self.octave[SPLIT_LEFT])
		self.d3m.toggle_light(self.octave[SPLIT_RIGHT])

class SplitMode(Mode):
	def __init__(self):
		self.zone = 0

	def on_enter(self):
		self.d3m.toggle_light(self.zone)

	def on_preset_pressed(self, idx):
		if idx < NUM_SPLIT_ZONES:
			self.zone = idx
			self.d3m.zone = idx

			self.d3m.clear_lights()
			self.d3m.toggle_light(idx)

class MomentaryMode(Mode):
	def __init__(self, offset):
		self.offset = offset

	def on_preset_pressed(self, idx):
		self.d3m.toggle_light(idx, True)
		self.d3m.cc_send_on(idx + (12 * self.offset))

	def on_preset_released(self, idx):
		self.d3m.toggle_light(idx, False)
		self.d3m.cc_send_off(idx + (12 * self.offset))

class TriggerMode(Mode):
	def __init__(self, offset):
		self.offset = offset

	def on_preset_pressed(self, idx):
		self.d3m.toggle_light(idx, True)
		self.d3m.cc_send_on(idx + (12 * self.offset))

	def on_preset_released(self, idx):
		self.d3m.toggle_light(idx, False)

class TestMode(Mode):
	def __init__(self):
		self.count = 0

	def on_preset_pressed(self, idx):
		for i in range(12):
			if i % 2 == self.count % 2:
				self.d3m.toggle_light(i, True)
			else:
				self.d3m.toggle_light(i, False)
		self.count += 1