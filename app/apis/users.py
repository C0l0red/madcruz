from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse

from app.models import User, Profile, Permissions, db, r
from app.utils import token_required
from random import randrange

api = Namespace("users", description="")

serializer = api.model("user", {
    "id": fields.String(description="Public ID of Album", attribute="public_id", readonly=True),
    "email": fields.String(description="Email of User"),
    # "password": fields.String(description="Password of User"),
    # "phone_number": fields.String(description="Phone Number of User", attribute="profile.phone_number"), 
})


parser = reqparse.RequestParser()
parser.add_argument("email", type=str, help="Email of User", location="form")
parser.add_argument("password", type=str, help="Password of User", location="form")
# parser.add_argument("phone_number", type=str, help="Phone Number of User", location="form")
#parser.add_argument()

# @api.param("id", "ID of the User")
@api.route("/")
@api.response(404, "User Not Found")
class UserResource(Resource):
    
    @api.response(200, "User fetched successfully", model=serializer)
    @api.doc(description="Fetch current User")
    @token_required
    def get(self, user):

        # user = User.query.filter_by(public_id=id).first_or_404(f"User with ID '{id}' not found")
        return api.marshal(user, serializer, skip_none=True), 200
    
    @api.doc(description="Create a single User", security=None)
    @api.response(201, "User successfully created", model=serializer)
    @api.expect(parser, validate=True)
    def post(self):
        args = parser.parse_args()
        
        user = User(**args)
        # user.profile = Profile()
        # user.profile.permissions = Permissions()

        db.session.add(user)
        db.session.commit()

        # otp = str(randrange(999999)).zfill(6)
        # user.send_email("OTP to complete registration", otp)
        # r_otp = r.set(f"user:{user.public_id}-otp", otp, ex=900, nx=True)

        # return {
        #     "message": f"OTP sent to {user.email}"
        # }, 201
        return api.marshal(user, serializer, skip_none=True), 201

    @api.doc(description="Edit current User")
    @api.response(200, "User updated successfully", model=serializer)
    @api.expect(parser, validate=True)
    @token_required
    def patch(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404(f"User with ID {id} not found")
        
        #edit user
        return api.marshal(user, serializer, skip_none=True)
    
    @api.doc(description="Delete current User")
    @api.response(204, "Successfully deleted User") 
    @token_required   
    def delete(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404(f"User with ID {id} not found")
        
        db.session.delete(user)
        db.session.commit()
        return 204

# @api.route("/")
# @api.response(404, "User Not Found")
# class UserListResource(Resource):
    
#    @api.doc(description="Fetch multiple Users")
#    def get(self):
#        users = User.query.filter_by()
#        return
        














