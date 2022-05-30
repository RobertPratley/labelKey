# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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
import objc
import re
import os
import codecs
from GlyphsApp.plugins import *
from GlyphsApp.UI import *

class labelKey(PalettePlugin):

	@objc.python_method
	def settings(self):
		self.name = 'Label Key'
		self.width = 160
		self.elementHeight = 16
		keyQuantity = 12
		self.height = keyQuantity * self.elementHeight
		self.paletteView = Window((self.width, self.height + 10))
		self.paletteView.frame = Group((0, 0, self.width, self.height + 5))
		
		self.paletteView.frame.swatches = CanvasView((10, 0, -10, 0), self)
		
		self.dialog = self.paletteView.frame.getNSView()
		
		#colorsData = GSGlyphsInfo.labelColors()
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
		colours = [
			(0.85, 0.26, 0.06, 0.5),
			(0.99, 0.62, 0.11, 0.5),
			(0.65, 0.48, 0.20, 0.5),
			(0.97, 0.90, 0.00, 0.5),
			(0.67, 0.95, 0.38, 0.5),
			(0.04, 0.57, 0.04, 0.5),
			(0.06, 0.60, 0.98, 0.5),
			(0.00, 0.20, 0.88, 0.5),
			(0.50, 0.09, 0.79, 0.5),
			(0.98, 0.36, 0.67, 0.5),
			(0.75, 0.75, 0.75, 0.5),
			(0.25, 0.25, 0.25, 0.5),
			]
		# for colorData in colorsData:
		# 	color = NSUnarchiver.unarchiveObjectWithData_(colorData)
		# 	colours.append(color)
		self.colours = dict(zip(colorKeys, colours))
		self.order = []

	@objc.python_method
	def update(self, sender):
		if hasattr(self.paletteView.frame, 'labels'):
			delattr(self.paletteView.frame, 'labels')
		colourLabels, self.order = self.mapKeys(self.getKeyFile())
		self.paletteView.frame.labels = Group((27, 4, -10, 0))
		for num, i in enumerate(self.order):
			setattr(self.paletteView.frame.labels, i, TextBox((0, num * self.elementHeight, 0, 22), colourLabels[i], sizeStyle="small"))
		newHeight = self.elementHeight * len(self.order)
		self.paletteView.frame.resize(self.width, newHeight + 10)

	@objc.python_method
	def draw(self, view):
		keyDiameter = 10
		height = view.bounds().size.height
		for num, i in enumerate(self.order, 1):
			if bool(re.search(r"\d", i)):
				duplicateColour = re.match(r".*?(?=\d)", i).group(0)
				self.colours[duplicateColour].set()
			else:
				NSColor.colorWithRed_green_blue_alpha_(*(self.colours[i])).set()
			NSBezierPath.bezierPathWithOvalInRect_(((0, height - (num * self.elementHeight)), (keyDiameter, keyDiameter))).fill()

	@objc.python_method
	def getKeyFile(self):
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

		if not os.path.exists(keyFile):
			f = open(keyFile,"w+")
			f.write("red=Red\norange=Orange\nbrown=Brown\nyellow=Yellow\nlightGreen=Light green\ndarkGreen=Dark green\nlightBlue=Light blue\ndarkBlue=Dark blue\npurple=Purple\nmagenta=Magenta\nlightGray=Light Gray\ncharcoal=Charcoal") 
		else:
			pass
		return keyFile


	@objc.python_method
	def mapKeys(self, keyFile):

		order = []
		colourLabels = {}
		if os.path.exists(keyFile):
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
			import traceback
			self.logError(traceback.format_exc())

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
