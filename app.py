# Simple Bubble app by Merlin Howse EMF 2024 on-site - www.merlinhowse.co.uk

import app
import imu
import math

from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES
from app_components.tokens import line_height


class BubbleApp(app.App):
	def __init__(self):
		self.button_states = Buttons(self)
		self.acc_read = None
		self.bgdone = False

	def update(self, delta):
		if self.button_states.get(BUTTON_TYPES["CANCEL"]):
			self.button_states.clear()
			self.minimise()
		else:
			self.acc_read = imu.acc_read()
			self.xdeg = '{0:.1f}'.format(self.acc_read[0] * 9)
			self.ydeg = '{0:.1f}'.format(self.acc_read[1] * 9)
			self.xpos = self.acc_read[0] * 12
			self.ypos = self.acc_read[1] * 12

	def draw(self, ctx):
		#if not self.bgdone:
		if True: # Oh - it seems we have to re-draw everything every frame or the menu reappears!
			clear_background(ctx)
			# Gradient
			ctx.radial_gradient(0, 0, 0, 0, 0, 120)
			ctx.add_stop(0, (255,150,0), 0)
			ctx.add_stop(1, (0,150,0), 1)
			ctx.rectangle(-120, -120, 240, 240).fill()
			ctx.stroke()
			# Cross hairs
			ctx.rgb(0, 1, 0).begin_path()
			ctx.move_to(-120,0)
			ctx.line_to(120, 0)
			ctx.move_to(0, 120)
			ctx.line_to(0, -120)
			for i in range(-5,6):
				# draw indicator lines for x
				ctx.move_to(i*20, 5)
				ctx.line_to(i*20, -5)
				# draw indicator lines for y
				ctx.move_to(-5, i*20)
				ctx.line_to(5, i*20)
			ctx.stroke()
			# Center circle
			ctx.rgba(0, 1, 0, 0.25).arc(0, 0, 40, 0, 2 * math.pi, True).fill()
			ctx.stroke()
			self.bgdone = True
		if self.acc_read:
			# Text
			ctx.font_size = 16
			ctx.rgb(0,1,0).move_to(-60,80).text("x:{}".format(self.xdeg))
			ctx.rgb(0,1,0).move_to(20,80).text("y:{}".format(self.ydeg))
			# Bubble
			ctx.rgba(0, 0.8, 0.3, 0.8).arc(-self.ypos, -self.xpos, 30, 0, 2 * math.pi, True).fill()
			ctx.rgba(0, 1, 0.6, 0.8).arc(-self.ypos-10, -self.xpos-10, 8, 0, 2 * math.pi, True).fill()
		else:
			ctx.rgb(1,0,0).move_to(-80,0).text("no readings yet")

__app_export__ = BubbleApp
