import webapp2
import jinja2
import os
import httplib2
from bs4 import BeautifulSoup
import urllib
from google.appengine.api import users
import json
import re
import main
import Utilidades

api_key = "c01645c0365e99cf2b57333dc48259ff"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key'}


class MainHandler(main.BaseHandler):
    def get(self):
        mostrarIndex = False

        tokenDropbox = self.session.get('dropbox_access_token')

        if Utilidades.haIniciadoSesionEnDropBox(tokenDropbox) is True:
            valida = Utilidades.tokenDropboxTodaviaValida(tokenDropbox)
            if valida is True:
                mostrarIndex = True

        userGoogle = users.get_current_user()


        if Utilidades.haIniciadoSesionEnGoogle(userGoogle) is True:
            mostrarIndex = True


        if mostrarIndex is True:
            # Para cargar una plantilla del entorno definido solo hay que llamar al
            # metodo get_template(), que  devuelve la  plantilla
            http = httplib2.Http()
            method = 'GET'
            base_url = 'https://api.musixmatch.com/ws/1.1/chart.artists.get'
            params = {'format': 'json',
                      'callback': 'callback',
                      'page': 1,
                      'page_size': 6,
                      'country': 'es',
                      'apikey': api_key
                      }

            params = urllib.urlencode(params)
            request_url = base_url + '?' + params
            respuesta, content = http.request(request_url, method)

            jsoncontent = json.loads(content)

            artist_List = jsoncontent["message"]["body"]["artist_list"]

            html = ""

            if artist_List is None:
                html = "No se han encontrado resultados :("
            else:
                length = len(artist_List) - 1

                for y in range(0, length):
                    oneTrack = artist_List[y]['artist']

                    artistName = oneTrack['artist_name']
                    artist_id = oneTrack['artist_id']
                    artistName = artistName.replace("'", "&#39")


                    html += "<a href='/datosArtista?nombreArtista=" + artistName + "&id=" + str(artist_id) + "'><b>" + artistName + "</a><br />"

            datos = {'artistas': html}

            template = JINJA_ENVIRONMENT.get_template("index.html")

            # Para  renderizarlo con algunas variables, simplemente llame al metodo
            self.response.out.write(template.render(datos))
        else:
            self.redirect("/")

class BuscarCancionesAjaxHandler(webapp2.RequestHandler):
    def post(self):

        tituloCancion = self.request.body

        http = httplib2.Http()
        method = 'GET'
        base_url = 'https://api.musixmatch.com/ws/1.1/track.search'
        params = {'format': 'json',
                  'callback': 'callback',
                  'q_track': tituloCancion,
                  'f_has_lyrics': 1.0,
                  's_artist_rating': 'desc',
                  'quorum_factor': 1,
                  'page_size': 15,
                  'apikey': api_key}

        params = urllib.urlencode(params)
        request_url = base_url + '?' + params
        respuesta, content = http.request(request_url, method)

        self.response.write(content)

class BuscarArtistaAjaxHandler(webapp2.RequestHandler):
    def post(self):

        nombreArtista = self.request.body

        http = httplib2.Http()
        method = 'GET'
        base_url = 'https://api.musixmatch.com/ws/1.1/artist.search'
        params = {'format': 'json',
                  'callback': 'callback',
                  'q_artist': nombreArtista,
                  'page_size': 15,
                  'apikey': api_key}

        params = urllib.urlencode(params)
        request_url = base_url + '?' + params
        respuesta, content = http.request(request_url, method)

        self.response.write(content)

def split_uppercase(value):
    return re.sub(r'([A-H,J-Z])', r'<br />\1', value)

def scrappLyrics(url):
    http = httplib2.Http()
    method = 'GET'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    }

    respuesta, content = http.request(url, method, headers=headers)

    soup = BeautifulSoup(content, "html.parser")

    letraCancion = []

    for trozo in soup.find_all('p'):
        trozoTexto = trozo.get_text()

        trozoTexto = split_uppercase(trozoTexto)
        textoSeparado = trozoTexto.split("<br />")
        for a in textoSeparado:
            if a.startswith(","):
                a = a.replace(",", "", 1)

            letraCancion.append(a)

    return letraCancion

class LetraCancionHandler(main.BaseHandler):
    def get(self):

        # Llegan nombreCancion=sxxxx&id=xxxxxx&artist=xxxx

        nombreCancion = self.request.params.get("nombreCancion")
        idCancion = self.request.params.get("id")
        artista = self.request.params.get("artist")

        http = httplib2.Http()
        method = 'GET'
        base_url = 'https://api.musixmatch.com/ws/1.1/track.lyrics.get'
        params = {'format': 'json',
                  'callback': 'callback',
                  'track_id': idCancion,
                  'apikey': api_key}

        params = urllib.urlencode(params)
        request_url = base_url + '?' + params
        respuesta, content = http.request(request_url, method)

        jsoncontent = json.loads(content)

        #La url de la letra
        lyricsUrl = jsoncontent["message"]["body"]["lyrics"]["backlink_url"]

        ## https://www.musixmatch.com/lyrics/Demi-Lovato/Skyscraper?utm_source=application&utm_campaign=api&utm_medium=UPV%3A1409617698108
        lyricsUrl = lyricsUrl.split("?utm", 1)[0]

        # Se obtiene la letra scrapping
        lyrics = scrappLyrics(lyricsUrl)


        tokenDropbox = self.session.get('dropbox_access_token')
        mostrarBoton = False

        if Utilidades.haIniciadoSesionEnDropBox(tokenDropbox) is True:
            valida = Utilidades.tokenDropboxTodaviaValida(tokenDropbox)
            if valida is True:
                mostrarBoton = True

        if mostrarBoton:
            estiloBoton = ""
            estiloMensaje = 'display:none'
        else:
            estiloBoton = 'display:none'
            estiloMensaje = ""

        datos = {'nombreCancion': nombreCancion,
                 'lyrics': lyrics,
                 'artist': artista,
                 'estiloBoton': estiloBoton,
                 'estiloMensaje': estiloMensaje}

        # Para cargar una plantilla del entorno definido solo hay que llamar al
        # metodo get_template(), que  devuelve la  plantilla
        template = JINJA_ENVIRONMENT.get_template("cancion.html")

        # Para  renderizarlo con algunas variables, simplemente llame al metodo
        self.response.out.write(template.render(datos))

class datosArtistaHandler(webapp2.RequestHandler):

    def get(self):
        nombreArtista = self.request.params.get("nombreArtista")

        http = httplib2.Http()
        method = 'GET'
        base_url = 'https://api.musixmatch.com/ws/1.1/track.search'
        params = {'format': 'json',
              'callback': 'callback',
              'q_artist': nombreArtista,
              's_track_rating': 'desc',
              'quorum_factor' : 1,
              'apikey': api_key,
              'page_size': 20}

        params = urllib.urlencode(params)
        request_url = base_url + '?' + params
        respuesta, content = http.request(request_url, method)

        jsoncontent = json.loads(content)

        trackList = jsoncontent["message"]["body"]["track_list"]

        html = ""

        if trackList is None:
            html = "No se han encontrado resultados :("
        else:
            length = len(trackList) - 1

            for y in range(0, length):
                oneTrack = trackList[y]['track']

                artistName = oneTrack['artist_name']
                trackId = str(oneTrack['track_id']).decode('utf-8').encode('utf-8')
                trackName = oneTrack['track_name']

                artistName = artistName.replace("'", "&#39")
                trackName = trackName.replace("'", "&#39")

                html += "<a href='/letraCancion?nombreCancion=" + trackName + "&id=" + trackId + "&artist=" + artistName + "'><b>" + trackName + "</b>, by " + artistName + "<br />"


        datos = {'artista': nombreArtista,
                'canciones': html}

        # Para cargar una plantilla del entorno definido solo hay que llamar al
        # metodo get_template(), que  devuelve la  plantilla
        template = JINJA_ENVIRONMENT.get_template("artista.html")

        # Para  renderizarlo con algunas variables, simplemente llame al metodo
        self.response.out.write(template.render(datos))


app = webapp2.WSGIApplication((
    ('/index', MainHandler),
    ('/buscarCancion', BuscarCancionesAjaxHandler),
    ('/buscarArtista', BuscarArtistaAjaxHandler),
    ('/letraCancion', LetraCancionHandler),
    ('/datosArtista', datosArtistaHandler)
), config=config, debug=True)