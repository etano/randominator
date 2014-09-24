import sys
import os
import zlib
import tornado.ioloop
import tornado.web
import subprocess

from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from wtforms_tornado import Form

def strBin(s_str):
    binary = []
    for s in s_str:
        if s == ' ':
            binary.append('00100000')
        else:
            binary.append(bin(ord(s)))
    return binary

def GetRandomness(original_string):
    with open('tmp','w') as f:
        bit_string = ''.join(str(b) for b in strBin(original_string)).replace('b','')
        f.write(bit_string)
    r = subprocess.check_output(['python','./testrandom.py','-t', '1', '-i', 'tmp']) # Backup original
    return float(r)*100.

class RandomForm(Form):
    bits = TextAreaField(validators=[Required()])
    submit = SubmitField()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        form = RandomForm(self.request.arguments)
        self.render("index.html", form=form, randomness='')

    def post(self):
        form = RandomForm(self.request.arguments)
        if form.validate():
            form = RandomForm(self.request.arguments)
            self.render("index.html", form=form, randomness="You're "+str(GetRandomness(form.data['bits']))+" % random!")
        else:
            self.set_status(400)
            self.write("aasdfasdf" % form.errors)

handlers = [
    (r"/", MainHandler),
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
)

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
