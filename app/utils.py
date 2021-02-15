from functools import wraps
import jwt
from datetime import datetime, timedelta
from flask import request

from app.models import User, r

authorizations = {
    "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY"
        }
}

def create_tokens(public_id):
    access_payload = {
            "public_id": user.public_id,
            "exp": datetime.utcnow() + timedelta(minutes=15) 
        }
    refresh_payload = {
            "public_id": user.public_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=6)
        }
        
    access_token = jwt.encode(access_payload, app.config["SECRET_KEY"])
    refresh_token = jwt.encode(refresh_payload, app.config["SECRET_KEY"])

    return access_token, refresh_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-API-KEY")
        
        if token is None:
            return {"error": "Access token is missing"}

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            public_id = data.get("public_id")
            
        except jwt.ExpiredSignatureError:
            temp = r.get(f)
            return {"error": "Access token is expired"}, 401
        except jwt.InvalidSignatureError:
            return {"error": "Access token is invalid"}, 401
        
        r_access_token = r.get(f"user:{public_id}-access-token")
        if not r_access_token:
            r.delete(f"user:{public_id}-refresh-token")
            #Create security threat

            return {"error": "Access token revoked. Please re-authenticate"}, 401
        
        if r_access_token != token:
            te
            
        user = User.query.filter_by(public_id=public_id).first_or_404("User Not Found")

        return f(user, *args, **kwargs)
    return decorated

