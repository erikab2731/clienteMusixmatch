import httplib2
import json

def haIniciadoSesionEnGoogle(googleUser):
    if googleUser:
        return True
    else:
        return False

def haIniciadoSesionEnDropBox(token):
    if token is None:
        return False
    else:
        return True

def tokenDropboxTodaviaValida(access_token):
    # Comprueba si la token es valida y no ha caducado
    # si es valida devuelve true

    http = httplib2.Http()

    metodo = 'POST'
    url = "https://api.dropboxapi.com/2/users/get_current_account"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    body = None

    respuesta, cuerpo_respuesta = http.request(url, metodo, headers=headers, body=json.dumps(body))

    # PROCESAMOS LA RESPUESTA
    if respuesta.status is not 200:
        return False
    else:
        return True

