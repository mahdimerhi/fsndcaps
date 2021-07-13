from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode


app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='Tgci7nSzOpfgtTPh9KbEimofvOVXauFP',
    client_secret='B8PaCIk31l2dgV03847BSuo8AROhnDZI7KACJg89x0Z7Q9pHrIRrRvFAv9PPnYll',
    api_base_url='https://udacafe.eu.auth0.com',
    access_token_url='https://udacafe.eu.auth0.com/oauth/token',
    authorize_url='https://udacafe.eu.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth_2(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/login')
    return f(*args, **kwargs)

  return decorated
