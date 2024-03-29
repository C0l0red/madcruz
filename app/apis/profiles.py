from flask import request, current_app as app
from flask_restplus import Namespace, Resource, fields, reqparse
from datetime import datetime

from app.models import db, Profile, User
from app.utils import token_required

api = Namespace("profiles", description="")

serializer = api.model("profile", {
    "id": fields.String(description="Profile ID", attribute="public_id", readonly=True),
    "first_name": fields.String(description="First name of User"),
    "middle_names": fields.String(description="Middle name of User"),
    "last_name": fields.String(description="Last name of User"),
    "date_of_birth": fields.Date(description="User's date of birth"),
    "phone_number": fields.String(description="User's phone number"),
    "citizenship": fields.String(description="User's citizenship"),
    "bvn": fields.Integer(description="User's Identification using BVN"),
    "nin": fields.Integer(description="User's Identification using NIN"),
    # "notifications": fields.Nested(description="", attribute=""),
    # "devices": fields.Nested(description="", attribute=""),
    # "stores": fields.Nested(description="", attribute=""),
})

parser = reqparse.RequestParser()
parser.add_argument("first_name", type=str, help="", required=False, location="form")
parser.add_argument("middle_names", type=str, help="", required=False, location="form")
parser.add_argument("last_name", type=str, help="", required=False, location="form")
parser.add_argument("date_of_birth", type=datetime, help="", required=False, location="form")
parser.add_argument("phone_number", type=str, help="", required=False, location="form")
parser.add_argument("citizenship", type=str, help="", required=False, location="form")
parser.add_argument("bvn", type=str, help="", required=False, location="form")
parser.add_argument("nin", type=str, help="", required=False, location="form")
# parser.add_argument("", type=str, help="", required=False, location="")

@api.route("/")
class ProfileResource(Resource):
    
    @api.doc(description="Fetch current User Profile")
    @api.response(200, "User Successfully fetched", model=serializer)
    @token_required
    def get(self, user):
        # user = user.query.filter_by(public_id=id).first_or_404("User Not Found")
        profile = user.profile

        return api.marshal(profile, serializer, skip_none=True), 200

    # @api.doc(description="Create User Profile")
    # @api.response(201, "User Profile created successfully")
    # @api.expect(parser=parser, validate=True)
    # @token_required
    # def post(self, id):
    #     user = User.query.filter_by(public_id=id).first_or_404()

    #     form = parser.parse_args()

    #     # first_name = form.get("first_name")
    #     # middle_names = form.get("middle_names")
    #     # last_name = form.get("last_name")
    #     # date_of_birth = form.get("date_of_birth")
    #     # phone_number = form.get("phone_number")
    #     # citizenship = form.get("citizenship")
    #     # bvn = form.get("bvn")
    #     # nin = form.get("nin")

    #     profile = Profile(**form)
    #     user.profile = profile
    #     # db.session.add(profile)
    #     db.session.commit()

    #     return api.marshal(profile, serializer, skip_none=True), 201

    @api.doc(description="Update a User Profile")
    @api.response(200, "Successfully updated User Profile", model=serializer)
    @api.expect(parser, validate=True)
    @token_required
    def patch(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404("User Not Found. Check API token")
        profile = user.profile

        json = parser.parse_args()
        data = {key:val for key,val in json.items() if val is not None}

        for key, val in data.items():
            setattr(profile, key, val)

        try:
            db.session.commit()
        except:
            api.abort(400, "Error updating profile")
        
        return api.marshal(profile, serializer, skip_none=True), 200
    
    @api.doc(description="Delete a User Profile")
    @api.response(204, "Successfully Deleted Profile")
    @token_required
    def delete(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404("User Not Found. Check API token")
        profile = user.profile

        db.session.delete(profile)
        db.session.commit()

        return 204
        


        