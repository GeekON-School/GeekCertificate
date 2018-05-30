#!/usr/bin/env python



import json
import os
import uuid

import tornado.escape
import tornado.ioloop
import tornado.template
import tornado.web
from PIL import Image, ImageDraw, ImageFont


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("working")

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        path = 'gekkon_template.jpg'
        font_type = 'HelveticaNeueCyr-Medium.ttf'
        output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     "images")
        name_font = ImageFont.truetype(font_type, 170)
        mark_font = ImageFont.truetype(font_type, 150)
        course_font = ImageFont.truetype('HelveticaNeueCyr-Thin.ttf', 105)
        course_font_small = ImageFont.truetype('HelveticaNeueCyr-Thin.ttf', 60)
        teacher_font = ImageFont.truetype('HelveticaNeueCyr-Thin.ttf', 70)
        data_return = {}
        for course in data['courses']:
            students = course['students']

            for student in students:
                image = Image.open(path)
                draw = ImageDraw.Draw(image)
                image_width = image.size[0]
                text_size = draw.textsize(student['name'], font=name_font)
                course_size = draw.textsize("«" + course['name'] + "»", font=course_font)
                x_name = (image_width / 2) - (text_size[0] / 2)
                x_course = (image_width / 2) - (course_size[0] / 2)
                # drawing student's name
                draw.text((x_name, 1070), student['name'], (0, 0, 0), font=name_font)
                # drawing course's name
                draw.text((x_course, 1480), "«" + course['name'] + "»", (0, 0, 0),
                          font=course_font)
                draw.text((947, 2130), "«" + course['name'] + "»", (0, 0, 0), font=course_font_small)
                # drawing mark
                draw.text((3100, 2025), student['mark'], (97, 167, 7), font=mark_font)
                # drawing teacher
                draw.text((356, 1973), "Бородин Ростислав", (0, 0, 0), font=teacher_font)
                draw.text((356, 2210), course['teachers'][0]['name'], (0, 0, 0), font=teacher_font)
                name = str(uuid.uuid4()) + '.jpg'
                image.save(os.path.join(output_folder, name))

                direct_url = 'https://cert.geekclass.ru/images/' + name
                data_return[student['id']] = {}
                data_return[student['id']]['name'] = student['name']
                data_return[student['id']]['link'] = direct_url

        print(json.dumps(data_return, ensure_ascii=False))
        self.write(json.dumps(data_return, ensure_ascii=False))


settings = [
    (r'/', MainHandler),
    (r'/images/(.*)', tornado.web.StaticFileHandler,
     {'path': os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images')})
]
app = tornado.web.Application(settings)
app.listen(8088)
tornado.ioloop.IOLoop.current().start()
