import webapp2
import jinja2
from webapp2_extras import sessions
from google.appengine.api import users
import os
import Utilidades

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'html')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'my-super-secret-key'}



class MainHandler(BaseHandler):
    def get(self):

        mostrarLogin = True

        tokenDropbox = self.session.get('dropbox_access_token')

        if Utilidades.haIniciadoSesionEnDropBox(tokenDropbox) is True:
            valida = Utilidades.tokenDropboxTodaviaValida(tokenDropbox)
            if valida is True:
                mostrarLogin = False

        userGoogle = users.get_current_user()

        if Utilidades.haIniciadoSesionEnGoogle(userGoogle) is True:
            mostrarLogin = False

        if mostrarLogin is False:
            self.redirect("/index")
        else:
            #El usuario no ha iniciado sesion
            url = users.create_login_url(self.request.uri)

            template_values = {'urlGoogle': url}

            template = JINJA_ENVIRONMENT.get_template("login.html")

            # Para  renderizarlo con algunas variables, simplemente llame al metodo
            self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], config=config, debug=True)