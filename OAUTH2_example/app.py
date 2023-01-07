from __future__ import print_function

from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from user import User

app = Flask(__name__)
app.secret_key = 'super secret string'

login_manager = LoginManager()
login_manager.init_app(app)

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    return render_template('index.html', user=None)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET'])
def login():
    flow = Flow.from_client_secrets_file(
        'config/client_secret.json',
        scopes=SCOPES
    )

    flow.redirect_uri = request.host_url[:-1] + url_for('oauth2callback')

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return redirect(authorization_url)


@app.route('/login/oauth2callback', methods=['GET'])
def oauth2callback():
    state = request.args.get('state')
    flow = Flow.from_client_secrets_file(
        'config/client_secret.json',
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = request.base_url

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()

    user = User.create(
        id_=user_info['id'],
        name=user_info['name'],
        email=user_info['email'],
        profile_pic=user_info['picture']
    )

    if user:
        login_user(user)
        return redirect(url_for('postlogin'))

    return redirect(url_for('index'))


@app.route('/postlogin', methods=['GET'])
@login_required
def postlogin():
    return render_template('postlogin.html', user=current_user), {'Refresh': '3; url=/'}


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('logout.html'), {'Refresh': '3; url=/'}


@app.route('/user/<username>', methods=['GET'])
@login_required
def user(username):
    if current_user.username == username:
        return render_template('user.html', user=current_user, public_user=current_user)
    return render_template('user.html', user=current_user, public_user=User.get_public_by_username(username))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, ssl_context='adhoc')
