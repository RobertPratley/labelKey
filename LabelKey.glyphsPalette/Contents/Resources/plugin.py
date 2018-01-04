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
import codecs
from GlyphsApp.plugins import *
from GlyphsApp.UI import *

class labelKey(PalettePlugin):


	def settings( self ):
		self.name = 'Label Key'
		self.width = 160
		self.elementHeight = 16
		keyQuantity = 12
		self.height = keyQuantity * self.elementHeight
		self.paletteView = Window((self.width, self.height + 10))
		self.paletteView.frame = Group((0, 0, self.width, self.height + 5))
		
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
		colourLabels, self.order = self.mapKeys(self.getKeyFile())
		self.paletteView.frame.labels = Group((27, 4, -10, 0))
		for num, i in enumerate(self.order):
			setattr(self.paletteView.frame.labels, i, TextBox((0, num * self.elementHeight, 0, 22), colourLabels[i], sizeStyle="small"))
		newHeight = self.elementHeight * len(self.order)
		self.paletteView.frame.resize(self.width, newHeight + 10)

	def draw( self, view ):
		keyDiameter = 10
		height = view.bounds().size.height
		for num, i in enumerate(self.order, 1):
                    if bool(re.search(r"\d", i)):
                        duplicateColour = re.match(r".*?(?=\d)", i).group(0)
                        self.colours[duplicateColour].set()
                    else:    
			self.colours[i].set()
		    NSBezierPath.bezierPathWithOvalInRect_(((0, height - (num * self.elementHeight)), (keyDiameter, keyDiameter))).fill()

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
		with codecs.open(keyFile, "r", "utf-8") as file:
			for line in file:
				colour = re.match(r".*?(?=\=)", line).group(0)
				label = re.search(r"(?<=\=).*", line).group(0)
				colourLabels[colour] = label
				order.append(colour)
		#print "__colourLabels:", colourLabels, order
		return colourLabels, order
	
	def setWindowController_(self, windowController):
		try:
			self._windowController = windowController
			self.update(None)
		except:
			self.logError(traceback.format_exc())

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
