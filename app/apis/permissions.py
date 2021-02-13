from flask import request, current_app as app
from flask_restplus import Namespace, Resource, fields, reqparse

from app.models import Permissions, User, db
from app.utils import token_required

api = Namespace("permissions", description="")

serializer = api.model("permissions", {
    "user_id": fields.String(description="", attribute="user.public_id", read_only=True),
    "admin": fields.Boolean(description=""),
    "buy_crypto": fields.Boolean(description=""),
    "sell_crypto": fields.Boolean(description=""),
    "receive_crypto": fields.Boolean(description=""),
    "fund_crypto_wallet": fields.Boolean(description=""),
    "fund_naira_wallet": fields.Boolean(description=""),
    "withdraw_crypto": fields.Boolean(description=""),
    "withdraw_naira": fields.Boolean(description=""),
    "view_market": fields.Boolean(description=""),
})

parser = reqparse.RequestParser()
parser.add_argument("buy_crypto", type=bool, help="", required=False, location="form")
parser.add_argument("sell_crypto", type=bool, help="", required=False, location="form")
parser.add_argument("receive_crypto", type=bool, help="", required=False, location="form")
parser.add_argument("fund_crypto_wallet", type=bool, help="", required=False, location="form")
parser.add_argument("fund_naira_wallet", type=bool, help="", required=False, location="form")
parser.add_argument("withdraw_crypto", type=bool, help="", required=False, location="form")
parser.add_argument("withdraw_naira", type=bool, help="", required=False, location="form")
parser.add_argument("view_market", type=bool, help="", required=False, location="form")
# parser.add_argument("buy_crypto", type=bool, help="", required=False, location="form")

class Permissions(Resource):

    @api.doc(description="Update User Permissions")
    @api.expect(parser=parser, validate=True)
    @token_required
    def patch(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404("User Not Found")
        permissions = user.profile.permissions

        json = parser.parse_args()
        data = {key:val for key,val in json.items() if val is not None}

        for key, val in data.items():
            setattr(permissions, key, val)

        db.session.commit()

        return api.marshal(permissions, serializer)
