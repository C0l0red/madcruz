from flask import request, current_app as app
from flask_restplus import Namespace, Resource, fields, reqparse

from app.models import Permissions, User, db
from app.utils import token_required

api = Namespace("permissions", description="")

serializer = api.model("permissions", {
    "user_id": fields.String(description="User ID", attribute="user.public_id", read_only=True),
    "admin": fields.Boolean(description="Admin status"),
    "buy_crypto": fields.Boolean(description="Permission to buy Cryptocurrency"),
    "sell_crypto": fields.Boolean(description="Permission to sell Cryptocurrency"),
    "receive_crypto": fields.Boolean(description="Permission to receive Cryptocurrency"),
    "fund_crypto_wallet": fields.Boolean(description="Permission to fund Cryptocurrencty Wallet"),
    "fund_naira_wallet": fields.Boolean(description="Permission to fund Naira Wallet"),
    "withdraw_crypto": fields.Boolean(description="Permission to withdraw from Cryptocurrency Wallet"),
    "withdraw_naira": fields.Boolean(description="Permission to withdraw from Naira Wallet"),
    "view_market": fields.Boolean(description="Permission to view Market")
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

@api.route("/")
class PermissionsResource(Resource):

    @api.doc(description="Update User Permissions")
    @api.expect(parser, validate=True)
    @api.response(200, "User Permission successfully updated", model=serializer)
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
