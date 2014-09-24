import sys
import os
import zlib
import tornado.ioloop
import tornado.web
import subprocess
from bitarray import bitarray

from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from wtforms_tornado import Form

def GetRandomness(original_bit_string):
    with open('tmp','w') as f:
      ba = bitarray()
      ba.fromstring(original_bit_string)
      for bit in ba.tolist():
          if(bit):
              f.write('1')
          else:
              f.write('0')
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
            self.render("index.html", form=form, randomness=str(GetRandomness(form.data['bits'])))
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
