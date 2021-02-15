from flask import request, current_app as app, jsonify
from flask_restplus import Resource, Namespace, reqparse, fields
from random import randrange

from app.models import User, r
from app.utils import token_required

api = Namespace("auth", description="")

token_serializer = api.model("token", {
    "access_token": fields.String(description="Short lived Access Token"),
    "refresh_token": fields.String(description="Long lived Refresh Token")
})

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

    # @api.expect(create_token_parser, validate=True)
    @api.doc(description="Create API Token for User authentication", security=None)
    @api.response(201, "Token created successfully", model=token_serializer)
    @api.param("otp", "OTP Code to validate User Login")
    @api.param("id", "User ID")
    def get(self, otp, id):
        # data = create_token_parser.parse_args()
        # email = data["email"]
        # password = data["password"]
        
        user = User.query.filter_by(public_id=id).first_or_404("User Not Found")
        # if not user:
        #     api.abort(401, "Invalid credentials")
        # authorized = user.verify_password(password)
        
        # if not authorized:
        #     api.abort(401, "Invalid credentials")
        r_otp = r.get(f"user:{user.public_id}-otp")
        if r_otp and (r_otp != otp):
            api.abort(400, "Invalid OTP")

        if not r_otp:
            api.abort(400, "Create new OTP")

        public_id = user.public_id
        access_token, refresh_token = create_tokens(public_id)

        # r.hmset(f"user:{public_id}", {
        #     "access_token": access_token,
        #     "refresh_token": refresh_token 
        # })
        r.set(f"user:{public_id}-access-token", access_token, ex=900)
        r.set(f"user:{public_id}-refresh-token", refresh_token, ex=21_600)

        user.profile.is_verified_email = True
        db.session.commit()

        return {
        	    "access_token": access_token,
        	    "refresh_token": refresh_token
        	},
        200


    @api.doc(description="Create OTP for User Login", security=None)
    @api.expect(create_token_parser, validate=True)
    @api.response(200, "OTP sent successfully")
    def post(self):
        data = create_token_parser.parse_args()
        email = data["email"]
        password = data["password"]
        
        user = User.query.filter_by(email=email).one_or_none()
        if not user:
            api.abort(401, "Invalid credentials")
        authorized = user.verify_password(password)
        
        if not authorized:
            api.abort(401, "Invalid credentials")

        otp = str(randrange(999999)).zfill(6)
        user.send_email("OTP to complete registration", otp)
        r_otp = r.set(f"user:{user.public_id}-otp", otp, ex=900, nx=True)

        return {
            "message": f"OTP sent to {user.email}"
        }, 200
        
    @api.doc(description="Exchange refresh token for a new access token")
    @api.expect(refresh_token_parser, validate=True)
    @api.response(200, "Access Token and Refresh Token refreshed", model=token_serializer)
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
        
        is_valid = r.exists(f"user:{public_id}-refresh-token")
        r_refresh_token = r.set(f"temp:{public_id}-refresh-token", refresh_token,
        	     ex=21_600, nx=True
        	)
        r_access_token = r.set(f"temp:{public_id}-access-token", access_token,
        	     ex=900, nx=True
        	)
        if not (r_refresh_token and r_access_token):
            #Handle fraud
            pass
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
    @api.expect(password_reset_parser, validate=True)
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
    @api.expect(password_reset_parser, validate=True)
    @api.response(204, "Password Reset Email sent to User")
    def post(self):
        #create password reset
        data = password_reset_parser.parse_args()

        email = data.get("email")

        #send email to user

        return 204

    @api.doc(description="Save new Password for User")
    @api.expect(password_reset_parser, validate=True)
    @api.response(204, "User Password successfully changed")
    def put(self):
        
        return

# @api.route("/verify-otp/<otp>")
# @api.param("otp", "OTP Code sent to User")
# class OTP(Resource):

#     @api.doc(description="")
#     @token_required
#     def post(self, user, otp):
        # r_otp = r.get(f"user:{user.public_id}-otp")
        # if r_otp and (r_otp == otp):


        # if not r_otp:
        #     api.abort(400, "")













