from flask import request, current_app as app, jsonify
from flask_restplus import Resource, Namespace, reqparse, fields

from app.models import User, r
from app.utils import token_required

api = Namespace("auth", description="")

create_token_parser = reqparse.RequestParser()
create_token_parser.add_argument("email", type=str, help="Email of User", location="form")
# create_token_parser.add_argument()

refresh_token_parser = reqparse.RequestParser()
refresh_token_parser.add_argument("token", type=str, help="Refresh Token for User", location="form")

password_reset_parser = reqparse.RequestParser()
password_reset_parser.add_argument("email", type=str, help="Email of User to reset password for", location='form')
password_reset_parser.add_argument("new_password", type=str, help="New Password for User", location='form')
password_reset_parser.add_argument("reset_token", type=str, help="Reset Token bearing the User's ID", location='form')

            

@api.route("/token")
class Token(Resource):
    
    @api.doc(description="Create API Token for User authentication")
    @api.expect(parser=create_token_parser, validate=True)
    @api.response(201, "Token created successfully")
    def post():
        data = create_token_parser.parse_args()
        email = data["email"]
        password = data["password"]
        
        user = User.query.filter_by(email=email).one_or_none()
        if not user:
            api.abort(401, "Invalid credentials")
        authorized = user.verify_password(password)
        
        if not authorized:
            api.abort(401, "Invalid credentials")
        
        public_id = user.public_id
        access_token, refresh_token = create_tokens(public_id)

        # r.hmset(f"user:{public_id}", {
        #     "access_token": access_token,
        #     "refresh_token": refresh_token 
        # })
        r.set(f"user:{public_id}-access-token", access_token, ex=900)
        r.set(f"user:{public_id}-refresh-token", refresh_token, ex=21_600)

        return {
        	    "access_token": access_token,
        	    "refresh_token": refresh_token
        	},
        200
        
    @api.doc(description="Exchange refresh token for a new access token")
    @api.expect(parser=refresh_token_parser, validate=True)
    @api.response(200, "Access Token and Refresh Token refreshed")
    def put(self):
        args = refresh_token_parser.parse_args()
        
        refresh_token = data["refresh_token"]
        
        try:
            data = jwt.decode(refresh_token, app.config["SECRET_KEY"])
            public_id = data["public_id"]
            # user = User.query.filter_by(public_id=public_id).first_or_404("User Not Found")
        except jwt.ExpiredSignatureError:
            return {"error": "API token expired"}, 401
        except jwt.InvalidSignatureError:
            return {"error": "API token is invalid"}, 401

        access_token, refresh_token = create_tokens(public_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_parser
        },
        200

        @api.doc(description="Delete access and refresh tokens")
        @api.response(204, "Tokens deleted successfully")
        @token_required
        def delete(self, user):
            public_id = user.public_id

            r.delete(f"user:{public_id}-access-token")
            r.delete(f"user:{public_id}-refresh-token")

            return 204
    
        
@api.route("/password-reset")      
class PasswordReset(Resource):

    @api.doc(description="Validate User Token for password reset")
    @api.expect(parser=password_reset_parser, validate=True)
    @api.response(200, "User Token validated")
    def get(self):
        data = password_reset_parser.parse_args()

        token = data.get("reset_token")
        if not token:
            api.abort(401, "Reset Token missing")
        
        #decode token

        public_id = None
        user = User.query.filter_by(public_id=public_id).first_or_404("User Not Found")

        return api.marshal(user, ser)

    @api.doc(description="Send User a Password Reset email")
    @api.expect(parser=password_reset_parser, validate=True)
    @api.response(204, "Password Reset Email sent to User")
    def post(self):
        #create password reset
        data = password_reset_parser.parse_args()

        email = data.get("email")

        #send email to user

        return 204

    @api.doc(description="Save new Password for User")
    @api.expect(parser=password_reset_parser, validate=True)
    @api.response(204, "User Password successfully changed")
    def put(self):
        
        return














