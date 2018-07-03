import os
import webapp2
import main
import jinja2
from google.appengine.api import users
import Utilidades

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key'}

class LogoutHandler(main.BaseHandler):
    def get(self):
        tokenDropbox = self.session.get('dropbox_access_token')

        if Utilidades.haIniciadoSesionEnDropBox(tokenDropbox) is True:
            self.session.pop('dropbox_access_token') #unset dropbox access token
            self.redirect("/")

        userGoogle = users.get_current_user()

        if Utilidades.haIniciadoSesionEnGoogle(userGoogle) is True:
            url = users.create_logout_url(self.request.uri)
            self.redirect(url)
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ('/logout', LogoutHandler)
], config=config, debug=True)