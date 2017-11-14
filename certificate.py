import json
import os

import qrcode
from PIL import Image, ImageDraw, ImageFont


class CertificateCreator(object):

	def __init__(self, dataJson=None, settingsJson=None, qr = None):
		self.setDefault()
		self.__data = None
		if (dataJson is not None):
			self.setData(dataJson)
		if (settingsJson is not None):
			self.setSettings(settingsJson)
		if (qr == True):
			self.__qr=True


	def setData(self, dataJson):
		'''
		Sets data file for this object
		@param dataJson: filename
		'''
		with open(dataJson) as dataJson:
			self.__data = json.load(dataJson)

	def setQr (self, addQr):
		'''
		@param addQr: True to create qr on each certificate
		'''
		if (addQr):
			self.__qr = True
		else:
			self.__qr = None


	def setSettings(self, settingsJson):
		'''
		Sets all params from settings file instead of default params
		@param settingsJson settings filename
		'''
		with open(settingsJson) as settingsFile:
			settings = json.load(settingsFile)
			self.__templatePath = settings['path']
			self.__nameXY = (settings['name']['x'], settings['name']['y'])
			self.__font = settings['font']
			self.__fontSize = settings['font_size']
			self.__courseXY = (settings['course']['x'], settings['course']['y'])
			self.__markXY = (settings['mark']['x'], settings['mark']['y'])
			self.__teacherXY = (settings['teacher']['x'], settings['teacher']['y'])
			self.__color = (settings['color']['r'], settings['color']['r'], settings['color']['r'])
			if (settings['output_folder'] != 0):
				self.__outputFolder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
								   settings['output_folder'])
			if (settings['qr_size']!=-1):
				self.__qrSize = settings['qr_size']
				self.__qrXY=(settings['qr']['x'],settings['qr']['y'])

	def setDefault(self):
		'''
		Sets all params to default
		'''
		self.__templatePath = 'base_template.jpg'
		self.__nameXY = (400, 410)
		self.__courseXY = (400, 550)
		self.__markXY = (900, 550)
		self.__teacherXY = (400, 630)
		self.__fontSize = 30
		self.__color = (0, 0, 0)
		self.__font = 'arial.ttf'
		self.__qrSize = 128
		self.__qrXY = (10,10)
		self.__qr = None
		self.__outputFolder  = os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      "images")

	def createCertificates(self):
		'''
		Creates certificates images in current folder (if provided) based on the class values. Also creates
		qr codes with name, course and mark if __qr = True
		'''
		if (self.__isDataInizialised()):
			for student in self.__data['students']:
				for course in student['courses']:
					image = Image.open(self.__templatePath)
					draw = ImageDraw.Draw(image)
					font = ImageFont.truetype(self.__font, self.__fontSize)
					draw.text(self.__nameXY, student['name'], self.__color,
						  font=font)
					draw.text(self.__courseXY, course['courseName'],
						  self.__color,
						  font=font)
					draw.text(self.__markXY, "Оценка: " + str(course['mark']),
						  self.__color,
						  font=font)
					draw.text(self.__teacherXY,
						  "Преподаватель: " + course['teacher'],
						  self.__color,
						  font=font)
					if (self.__qr == True):
						qrImg = qrcode.make(student['name']
								    +course['courseName']
								    +str(course['mark']))
						qrImg = qrImg.resize ((self.__qrSize,self.__qrSize),Image.ANTIALIAS)
						image.paste (qrImg, (self.__qrXY))
					file_path = os.path.join(self.__outputFolder,
								 student['name'] + " " + course['courseName'] +
								 '.jpg')
					image.save(file_path)
		else:
			raise Exception("Data file is not provided")

	def __isDataInizialised(self):
		'''
		Checking if object has data file
		'''
		if (self.__data is not None):
			return True
		else:
			return False

