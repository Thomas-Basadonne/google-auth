from flask import Flask, url_for, session, redirect, render_template
from authlib.integrations.flask_client import OAuth
import json

app = Flask(__name__)

# Configurazione dell'applicazione
appConfig = {
    "google_client_id" :'<aggiungi_client_id>',
    "google_client_secret" :'<aggiungi_client_secret>',
    "google_redirect_uri" :'/signin-google',
    "meta_url": "https://accounts.google.com/.well-known/openid-configuration",
    "flask_secret" : "unaStringaRandom",
    "flask_port" :8000
}

app.secret_key = appConfig.get("flask_secret")

# Inizializzazione di OAuth con Flask
oauth = OAuth(app)

# Registrazione del servizio di autenticazione OAuth con Google
oauth.register("sfattura",
               client_id = appConfig.get("google_client_id"),
               client_secret = appConfig.get("google_client_secret"),
               server_metadata_url = appConfig.get("meta_url"),
               client_kwargs = {
                   "scope" : "https://www.googleapis.com/auth/gmail.readonly"
               })

# Pagina principale
@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"),
                           pretty = json.dumps(session.get("user"), indent=4))
    
# Rotta per l'inizio del processo di login con Google
@app.route("/google-login")
def googleLogin():
    return oauth.sfattura.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

# Rotta per la gestione del callback di Google dopo il login
#URI REDIRECT DA AGGIUNGERE IN CONSOLE GOOGLE
@app.route("/signin-google")
def googleCallback():
    token = oauth.sfattura.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=appConfig.get("flask_port"), debug=True)