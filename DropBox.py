import webapp2
import httplib2
import urllib
import json
import jinja2
from webapp2_extras import sessions
import os
import main
import Utilidades

gae_app_id = 'swgae10'
# Cuidado con la callBack URI definida en DROPBOX
gae_callback_url = 'https://' + gae_app_id + '.appspot.com/Doauth_callback'

dropbox_app_key = 'nv1zw2g78xza8gn'
dropbox_app_secret = '1to3dr7wgt5y6ck'



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key'}



class LoginAndAuthorize(webapp2.RequestHandler):
    def get(self):
        url = 'https://www.dropbox.com/1/oauth2/authorize'
        parametros = {'response_type': 'code',
                      'client_id': dropbox_app_key,  # App key
                      'redirect_uri': gae_callback_url}

        parametros = urllib.urlencode(parametros)
        self.redirect(url + '?' + parametros)


class OAuthHandler(main.BaseHandler):
    def get(self):
        request_url = self.request.url
        code = request_url.split('code=')[1]

        http = httplib2.Http()

        metodo = 'POST'
        url = 'https://api.dropbox.com/1/oauth2/token'
        parametros = {'code': code,
                      'grant_type': 'authorization_code',
        		      'client_id': dropbox_app_key, # App key
                      'client_secret': dropbox_app_secret,  #App secret
                      'redirect_uri': gae_callback_url}

        parametros = urllib.urlencode(parametros)

        cabeceras = {'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(parametros))}

        respuesta, cuerpo_respuesta = http.request(url, metodo, headers=cabeceras, body=parametros)

        json_contenido = json.loads(cuerpo_respuesta)

        self.session['dropbox_access_token'] = json_contenido['access_token']

        self.redirect("/index")


class SaveSongDropBox(main.BaseHandler):
    def post(self):
        valida = False

        tokenDropbox = self.session.get('dropbox_access_token')

        if Utilidades.haIniciadoSesionEnDropBox(tokenDropbox) is True:
            valida = Utilidades.tokenDropboxTodaviaValida(tokenDropbox)

        if valida is False:
            # devolver mensaje sesion caducada
            self.response.write("False")

        else:

            contenido = self.request.body.split("&letra=")
            titulo = contenido[0].split("titulo=")[1]
            letra = contenido[1].split("&artista=")[0]
            artista = contenido[1].split("&artista=")[1]

            http = httplib2.Http()
            metodo = 'POST'
            path = '/'+titulo+'.txt'
            url = 'https://content.dropboxapi.com/2/files/upload'

            cuerpo = titulo + " by " + artista + "\n" + letra

            cabeceras = {'Authorization': 'Bearer ' + tokenDropbox,
                          "Dropbox-API-Arg": "{\"path\":\"" + path + "\",\"autorename\":true}",
                         'Content-Type': 'application/octet-stream',
                         'Content-Length': str(len(cuerpo))}

            cabeceraRespuesta, bodyRespuesta = http.request(url, metodo, headers=cabeceras, body=cuerpo)

            if cabeceraRespuesta.status is not 200:
                self.response.write("Se ha producido un error al intentar guardar el fichero:")
                self.response.write(bodyRespuesta)
            else:
                self.response.write("True")


app = webapp2.WSGIApplication([
    ('/DropBox', LoginAndAuthorize),
    ('/Doauth_callback', OAuthHandler),
    ('/SaveSongDropBox', SaveSongDropBox)
], config=config, debug=True)