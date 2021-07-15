import os
from flask import Flask, app, request, jsonify, abort, redirect, session
import json
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import *
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config['SECRET_KEY'] = SECRET_KEY
    setup_db(app)
    CORS(app)
    
    
    '''
    Uncomment the following line before first run
    then comment it back in order not to reset
    the databse each time the server restarts
    '''
    
    
    #db_drop_and_create_all()



    # AUTH0

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=CLIENT_ID,
        client_secret=SECRET_KEY,
        api_base_url=AUTH0_DOMAIN,
        access_token_url='https://udacafe.eu.auth0.com/oauth/token',
        authorize_url='https://udacafe.eu.auth0.com/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
        'GET,PATCH,POST,DELETE')
        return response


    # ROUTES


    @app.route('/')
    def index():
        return 'healthy.'


    @app.route('/login')
    def login():
        return auth0.authorize_redirect(
            audience=API_AUDIENCE,
            redirect_uri=CALLBACK_URL
        )


    @app.route('/callback')
    def callback_handling():
        # get authorization token

        try:
            token = auth0.authorize_access_token()
            session['token'] = token['access_token']
            
            return jsonify({
                'success': True,
                'token': token['access_token']
                }), 200

        except Exception as e:
            print(e)


    @app.route('/logout')
    def log_out():
        # clear the session
        session.clear()
        # redirect user to logout endpoint
        params = {'returnTo': 'https://fsndcaps.herokuapp.com/login',
        'client_id': CLIENT_ID}
        return redirect(AUTH0_DOMAIN + '/v2/logout?' + urlencode(params))


    @app.route('/drinks')
    def get_drinks():

        try:
            drinks_all = Drink.query.order_by(Drink.id).all()

            drinks = [drink.short() for drink in drinks_all]

            if len(drinks) == 0:
                print('No drinks available at the moment.')
                abort(404)

            return jsonify({
                'success': True,
                'drinks': drinks
            }), 200

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/drinks-detail')
    @requires_auth('get:drinks-detail')
    def drinks_detail(payload):

        try:
            drinks_all = Drink.query.all()
            drinks = [drink.long() for drink in drinks_all]

            if len(drinks) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'drinks': drinks
            }), 200

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink(payload):

        try:
            body = request.get_json()

            new_title = body.get('title')
            new_recipe = body.get('recipe')
            new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))

            new_drink.insert()

            return jsonify({
                'success': True,
                'drinks': [new_drink.long()]
            }), 200

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/drinks/<int:id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def edit_drink(payload, id):

        try:

            drink = Drink.query.filter(Drink.id == id).one_or_none()
            body = request.get_json()

            if drink is None:
                print('Drink ID does not exist.')
                abort(404)

            drink.title = body.get('title', drink.title)
            drink.recipe = json.dumps(body.get('recipe'))

            drink.update()

            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            }), 200

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/drinks/<int:id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drinks(payload, id):

        try:
            drink = Drink.query.filter(Drink.id == id).one_or_none()

            if drink is None:
                abort(404)

            drink.delete()

            return jsonify({
                'success': True,
                'delete': id
            }), 200

        except Exception as e:
            print(e)
            abort(404)


    # Error Handling


    @app.errorhandler(422)
    def unprocessable_entry(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entry'
        }), 422


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400




    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''


    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
