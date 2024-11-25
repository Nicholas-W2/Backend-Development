# #Part 1 
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Predefined username and password for Basic Auth
# USERNAME = "admin"
# PASSWORD = "password123"

# @app.route('/basic-auth')
# def basic_auth():
#     # Get the authorization header
#     auth = request.authorization

#     # Check if the authorization header exists and contains valid credentials
#     if not auth or auth.username != USERNAME or auth.password != PASSWORD:
#         return jsonify({"message": "Authentication required!"}), 401

#     # If credentials are correct, return a success message
#     return jsonify({"message": "You are authorized!"})

# if __name__ == '__main__':
#     app.run(debug=True)


# # Part 2 
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Predefined username and password for Basic Auth
# USERNAME = "admin"
# PASSWORD = "password123"

# # Predefined Bearer token for Bearer Auth
# BEARER_TOKEN = "your_secret_token_here"

# @app.route('/basic-auth')
# def basic_auth():
#     auth = request.authorization

#     if not auth or auth.username != USERNAME or auth.password != PASSWORD:
#         return jsonify({"message": "Authentication required!"}), 401

#     return jsonify({"message": "You are authorized!"})

# @app.route('/bearer-auth')
# def bearer_auth():
#     # Get the Authorization header
#     auth_header = request.headers.get('Authorization')

#     if not auth_header or not auth_header.startswith('Bearer '):
#         return jsonify({"message": "Authentication required!"}), 401

#     # Extract the token from the header
#     token = auth_header[len('Bearer '):]

#     if token != BEARER_TOKEN:
#         return jsonify({"message": "Invalid token!"}), 401

#     return jsonify({"message": "You are authorized with Bearer token!"})

# if __name__ == '__main__':
#     app.run(debug=True)

# #Part 3 
# import os
# from flask import Flask, redirect, request, jsonify, session, url_for
# import requests
# from requests_oauthlib import OAuth2Session

# app = Flask(__name__)

# # Set a secret key to enable sessions
# app.secret_key = os.urandom(24)

# # GitHub OAuth Settings
# CLIENT_ID = 'Ov23liia229vR4DYoTNT'  # Replace with your GitHub OAuth Client ID
# CLIENT_SECRET = 'ffe63234e338368cf5df0c57791dff6b27fd2c04'  # Replace with your GitHub OAuth Client Secret
# GITHUB_API_URL = 'https://api.github.com/user'
# GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
# GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'

# # Redirect to GitHub for OAuth authentication
# @app.route('/oauth')
# def oauth():
#     github = OAuth2Session(CLIENT_ID, redirect_uri=url_for('callback', _external=True))
#     authorization_url, state = github.authorization_url(GITHUB_AUTH_URL)
    
#     # Save the state to the session for security reasons
#     session['oauth_state'] = state
    
#     # Redirect to GitHub's OAuth page
#     return redirect(authorization_url)


# # Handle the GitHub OAuth callback
# @app.route('/callback')
# def callback():
#     # Get the code from the GitHub callback
#     code = request.args.get('code')

#     # Create an OAuth2 session object to exchange the code for a token
#     github = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=url_for('callback', _external=True))
    
#     # Exchange the code for an access token
#     token = github.fetch_token(GITHUB_TOKEN_URL, client_secret=CLIENT_SECRET, code=code)

#     # Use the token to get user information from GitHub
#     user_info = github.get(GITHUB_API_URL).json()

#     # Return the user information as a JSON response
#     return jsonify(user_info)

# if __name__ == '__main__':
#     app.run(debug=True)

import os
from flask import Flask, redirect, request, jsonify, session, url_for
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# Set a secret key to enable sessions
app.secret_key = os.urandom(24)

# GitHub OAuth Settings
CLIENT_ID = 'Ov23liia229vR4DYoTNT'  
CLIENT_SECRET = '6287343661a2bac8569dc2597b40d65039025631'  
GITHUB_API_URL = 'https://api.github.com/user'
GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'

# Redirect to GitHub for OAuth authentication
@app.route('/oauth')
def oauth():
    # Generate the callback URL dynamically
    redirect_uri = url_for('callback', _external=True)
    
    # Log the redirect_uri for debugging purposes
    print(f"Redirect URI being used: {redirect_uri}")

    # Create an OAuth2 session with the callback URL
    github = OAuth2Session(CLIENT_ID, redirect_uri=redirect_uri)
    
    # Generate the GitHub authorization URL
    authorization_url, state = github.authorization_url(GITHUB_AUTH_URL)
    
    # Save the state in the session for security purposes
    session['oauth_state'] = state
    
    # Redirect the user to GitHub's OAuth page
    return redirect(authorization_url)

# Handle the GitHub OAuth callback
@app.route('/callback')
def callback():
    # Get the authorization code and state from the callback
    code = request.args.get('code')
    state = request.args.get('state')

    # Log the code and state for debugging
    print(f"Authorization code received: {code}")
    print(f"State received: {state}, Session State: {session.get('oauth_state')}")

    # Check if the state is valid
    if state != session.get('oauth_state'):
        return jsonify({"error": "Invalid state!"}), 400
    
    # Ensure the code is present
    if not code:
        return jsonify({"error": "Authorization code is missing!"}), 400

    # Create an OAuth2 session to exchange the code for an access token
    redirect_uri = url_for('callback', _external=True)
    github = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=redirect_uri)
    
    # Exchange the authorization code for an access token
    try:
        token = github.fetch_token(GITHUB_TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
        print(f"Access Token: {token}")  # Log the token for debugging
    except Exception as e:
        return jsonify({"error": f"Failed to fetch token: {e}"}), 500

    # Use the access token to fetch the user's information from GitHub
    try:
        user_info = github.get(GITHUB_API_URL).json()
        print(f"User Info: {user_info}")  # Log user info for debugging
    except Exception as e:
        return jsonify({"error": f"Failed to fetch user info: {e}"}), 500

    # Return the user information as JSON
    return jsonify(user_info)

if __name__ == '__main__':
    app.run(debug=True)


