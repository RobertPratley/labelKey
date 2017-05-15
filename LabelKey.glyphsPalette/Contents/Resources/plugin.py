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
import os
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
		
		colorsData = Glyphs.defaults["LabelColors"]
		colorKeys = ["red",
					"orange",
					"brown",
					"yellow",
					"lightGreen",
					"darkGreen",
					"lightBlue",
					"darkBlue",
					"purple",
					"magenta",
					"lightGray",
					"charcoal"]
		colours = []
		for colorData in colorsData:
			color = NSUnarchiver.unarchiveObjectWithData_(colorData)
			colours.append(color)
		self.colours = dict(zip(colorKeys, colours))

	def update(self, sender):
		if hasattr(self.paletteView.frame, 'labels'):
			delattr(self.paletteView.frame, 'labels')
		colourLabels, order = self.mapKeys(self.getKeyFile())
		self.paletteView.frame.labels = Group((27, 3, -10, 0))
		for num, i in enumerate(order):
			setattr(self.paletteView.frame.labels, i, TextBox((0, num * 16, 0, 22), colourLabels[i], sizeStyle="small"))
			print i

	def draw( self, view ):
		keyDiameter = 10
		height = view.bounds().size.height
		order = self.mapKeys(self.getKeyFile())[1]
		for num, i in enumerate(order, 1):
			self.colours[i].set()
			NSBezierPath.bezierPathWithOvalInRect_(((0, height - (num * 16)), (keyDiameter, keyDiameter))).fill()

	def getKeyFile( self ):
		keyFile = None
		try:
			thisDirPath = os.path.dirname(self.windowController().document().font.filepath)
			localKeyFile = thisDirPath + '/labelkey.txt'
			if os.path.exists(localKeyFile):
				keyFile = localKeyFile
		except:
			pass
		if keyFile is None:
			keyFile = os.path.expanduser('~/Library/Application Support/Glyphs/Info/labelkey.txt')
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
		print colourLabels, order
		return colourLabels, order
	

	def start(self):
		Glyphs.addCallback(self.update, DOCUMENTACTIVATED)

	def __del__(self):
		Glyphs.removeCallback(self.update)

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__