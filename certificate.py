import json
import os

from PIL import Image, ImageDraw, ImageFont


class CertificateCreator(object):
	def __init__(self, dataJson=None, settingsJson=None):
		self.setDefault()
		self.__data = None
		if (dataJson is not None):
			self.setData(dataJson)
		if (settingsJson is not None):
			self.setSettings(settingsJson)

	def setData(self, dataJson):
		with open(dataJson) as dataJson:
			self.__data = json.load(dataJson)


	def setSettings(self, settingsJson):
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

	def setDefault(self):
		self.__templatePath = 'base_template.jpg'
		self.__nameXY = (400, 410)
		self.__courseXY = (400, 550)
		self.__markXY = (900, 550)
		self.__teacherXY = (400, 630)
		self.__fontSize = 30
		self.__color = (0, 0, 0)
		self.__font = 'arial.ttf'
		self.__outputFolder  = os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      "images")

	def createCertificates(self):
		if (self.__isDataInizialised()):
			image = Image.open(self.__templatePath)
			draw = ImageDraw.Draw(image)
			font = ImageFont.truetype(self.__font, self.__fontSize)
			for student in self.__data['students']:
				for course in student['courses']:
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
					file_path = os.path.join(self.__outputFolder,
								 student['name'] + " " + course['courseName'] +
								 '.jpg')
					image.save(file_path)
		else:
			raise Exception("Data file is not provided")

	def __isDataInizialised(self):
		if (self.__data is not None):
			return True
		else:
			return False

	def __isBaseTemplate(self):
		if (self.__templatePath is not None):
			return False
		else:
			return True
