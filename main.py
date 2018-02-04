#!/usr/bin/env python



import json
import os
import uuid

import tornado.escape
import tornado.ioloop
import tornado.template
import tornado.web
from PIL import Image, ImageDraw, ImageFont


class MainHandler (tornado.web.RequestHandler):
	def post(self):
		data = tornado.escape.json_decode(self.request.body)
		path = 'gekkon_template.jpg'
		font_type = 'HelveticaNeueCyr-Medium_0.ttf'
		output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
					      "images")
		name_font = ImageFont.truetype(font_type, 170)
		mark_font = ImageFont.truetype(font_type, 150)
		course_font = ImageFont.truetype('HelveticaNeueCyr-Thin', 110)
		course_font_small = ImageFont.truetype('HelveticaNeueCyr-Thin', 70)
		teacher_font = ImageFont.truetype('HelveticaNeueCyr-Thin', 70)
		data_return = {}
		for course in data['courses']:
			students = course ['students']

			for student in students:
				image = Image.open(path)
				draw = ImageDraw.Draw(image)
				image_width = image.size[0]
				text_size = draw.textsize(student['name'], font=name_font)
				x = (image_width / 2) - (text_size[0] / 2)
				#drawing student's name
				draw.text((x, 1070), student['name'], (0,0,0),font=name_font)
				#drawing course's name
				draw.text((1680, 1360), "«" + course['name'] + "»", (0, 0, 0), font=course_font)
				draw.text((960, 2120), "«" + course['name'] + "»", (0, 0, 0), font=course_font_small)
				#drawing mark
				draw.text((3100, 2025), student['mark'], (97,167, 7), font=mark_font)
				#drawing teacher
				draw.text((356, 1973), course['teachers'][0]['name'], (0, 0, 0), font=teacher_font)
				draw.text((356, 2210), course['teachers'][1]['name'], (0, 0, 0), font=teacher_font)
				name = str(uuid.uuid4())+ '.jpg'
				image.save(os.path.join(output_folder, name) )

				direct_url = 'https://cert.geekclass.ru/images/' +name
				data_return[student['name'].replace(" ", "_")] = direct_url
		print(json.dumps(data_return, ensure_ascii=False))
		self.write(json.dumps(data_return, ensure_ascii=False))





settings = [
    (r'/', MainHandler),
	(r'/images/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(os.path.realpath(__file__)),'images')})
]
app = tornado.web.Application(settings)
app.listen(8085)
tornado.ioloop.IOLoop.current().start()


