# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################


from AppKit import NSBezierPath, NSColor, NSFont, NSImage, NSGradient, NSColorSpace, NSMiterLineJoinStyle, NSRoundLineJoinStyle, NSBevelLineJoinStyle, NSFontAttributeName, NSForegroundColorAttributeName, NSGraphicsContext, NSCompositeSourceOver, NSGradientDrawsBeforeStartingLocation, NSGradientDrawsAfterEndingLocation
from Foundation import NSMakeRect, NSAffineTransform, NSClassFromString, NSMakePoint, NSZeroRect
from vanilla import *
from GlyphsApp.plugins import *
from GlyphsApp.UI import *
import re
import os.path
from os.path import exists
from os.path import expanduser


class labelKey (PalettePlugin):
	def assignKeys(self, keyFile):
		colorLabels = {}
		global order
		order = []
		with open(keyFile) as f:
			for line in f:
				color = re.match(r".*?(?=\=)", line).group(0)
				label = re.search(r"(?<=\=).*", line).group(0)
				order.append(color)
				colorLabels[color] = label
			f.close()
		# This works	
		return colorLabels, order
    

	def settings(self):
		
		self.name = 'Label Key'
		thisFont = Glyphs.font
		thisDirPath = os.path.dirname(thisFont.filepath)
		localKeyFile = thisDirPath + '/labelkey.txt'
		userKeyFile = '{0}{1}'.format(os.path.abspath(expanduser('~')), '/Library/Application Support/Glyphs/Info/labelkey.txt')
		if exists(localKeyFile):
			colorLabels, order = self.assignKeys(localKeyFile)
		elif exists(userKeyFile):
			colorLabels, order = self.assignKeys(userKeyFile)
		height = len(order) * 17
		self.w = Window((150, height))
		self.w.frame = Group((0, 0, 150, height))
		self.w.frame.labels = Group((27, 3, -10, 0))
		self.w.frame.swatches = CanvasView((10 ,0 ,-10 , 0), self)


		for num, i in enumerate(order):
			setattr(self.w.frame.labels, i, TextBox((0, num * 16, 0, 22), colorLabels[i], sizeStyle="small"))

		self.dialog = self.w.frame.getNSView()
		
	colours = {
	"red": [0.96, 0.17, 0.17, 1],
	"orange": [1, 0.6, 0.17, 1],
	"brown": [0.58, 0.37, 0.17, 1],
	"yellow": [0.98, 0.87, 0.1, 1],
	"lightGreen": [0.58, 0.87, 0, 1],
	"darkGreen": [0.24, 0.57, 0.32, 1],
	"lightBlue": [0.24, 0.73, 0.85, 1],
	"darkBlue": [0, 0.23, 0.85, 1],
	"purple": [0.54, 0, 0.77, 1],
	"magenta": [1, 0, 0.9, 1],
	"lightGray": [0.7, 0.7, 0.7, 1],
	"charcoal": [0.3, 0.3, 0.3, 1]}

	#def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		

	

	def draw(self, view):
		keyDiameter = 10
		height = view.bounds().size.height
		for num, i in enumerate(order, 1):
			r, g, b, a = self.colours[i]
			NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a).set()
			NSBezierPath.bezierPathWithOvalInRect_(((0, height - (num * 16)), (keyDiameter, keyDiameter))).fill()
				
	def __del__(self):
		pass