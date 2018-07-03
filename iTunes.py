import webapp2
import httplib2
import urllib
import json
import jinja2
from webapp2_extras import sessions
import main
from google.appengine.api import users
import os


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key'}

class GetRequestedSongResults(main.BaseHandler):
    def post(self):
        artista = self.request.params.get("artista")
        titulo = self.request.params.get("titulo")

        http = httplib2.Http()

        metodo = 'GET'
        url = 'https://itunes.apple.com/search'
        parametros = {'term': titulo + " " + artista,
                      'limit': 5}

        parametros = urllib.urlencode(parametros)

        cabeceras = {'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(parametros))}

        respuesta, cuerpo_respuesta = http.request(url + "?" + parametros, metodo, headers=cabeceras, body='')

        self.response.write(cuerpo_respuesta)

app = webapp2.WSGIApplication([
    ('/RequestSong', GetRequestedSongResults)
], config=config, debug=True)