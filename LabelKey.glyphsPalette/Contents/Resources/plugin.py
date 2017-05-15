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
from vanilla import *
import re
import os.path
from os.path import expanduser
from os.path import exists
from GlyphsApp.plugins import *
from GlyphsApp.UI import *

class labelKey(PalettePlugin):


	def settings( self ):
		self.name = 'Label Key'
		width = 160
		elementHeight = 17
		self.height = 11 * elementHeight
		self.paletteView = Window((width, self.height + 10))
		self.paletteView.frame = Group((0, 0, width, self.height + 10))
		
		self.paletteView.frame.swatches = CanvasView((10, 0, -10, 0), self)
		
		self.dialog = self.paletteView.frame.getNSView()

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




	def update(self, sender):
		if hasattr(self.paletteView.frame, 'labels'):
			delattr(self.paletteView.frame, 'labels')
		colourLabels, order = self.mapKeys(self.setKeyFile())
		self.paletteView.frame.labels = Group((27, 3, -10, 0))
		for num, i in enumerate(order):
			setattr(self.paletteView.frame.labels, i, TextBox((0, num * 16, 0, 22), colourLabels[i], sizeStyle="small"))
			print i

	def draw( self, view ):
		keyDiameter = 10
		height = view.bounds().size.height
		order = self.mapKeys(self.setKeyFile())[1]
		for num, i in enumerate(order, 1):
			r, g, b, a = self.colours[i]
			NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a).set()
			NSBezierPath.bezierPathWithOvalInRect_(((0, height - (num * 16)), (keyDiameter, keyDiameter))).fill()

	def setKeyFile( self ):
		thisDirPath = os.path.dirname(Glyphs.font.filepath)
		localKeyFile = thisDirPath + '/labelkey.txt'
		if exists(localKeyFile):
			keyFile = localKeyFile
		else:
			keyFile = '{0}{1}'.format(os.path.abspath(expanduser('~')), '/Library/Application Support/Glyphs/Info/labelkey.txt')
		return keyFile
				
	def mapKeys( self, keyFile ):
		order = []
		colourLabels = {}
		with open(keyFile) as file:
			for line in file:
				colour = re.match(r".*?(?=\=)", line).group(0)
				label = re.search(r"(?<=\=).*", line).group(0)
				colourLabels[colour] = label
				order.append(colour)
		file.close()
		print colourLabels, order
		return colourLabels, order
	

	def start(self):
		Glyphs.addCallback(self.update, DOCUMENTACTIVATED)

	def __del__(self):
		Glyphs.removeCallback(self.update)

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__