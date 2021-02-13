from flask import current_app as app, request
from flask_restplus import Namespace, Resource, fields, reqparse

from app.models import Profile, User
from app.utils import token_required

api = Namespace("bitcoin", description="")

serializer = api.model("bitcoin", {

})

parser = reqparse.RequestParser()
# parser.add_argument()

@api.route("/fund")
class Fund(Resource):

    # @api.expect()
    @api.doc(description="Fund your Bitcoin Wallet")
    @token_required
    def post(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404("User Not Found")
        #Fund Crypto Wallet

        return 

@api.route("/withdraw")
class Withdraw(Resource):

    @api.doc(description="Withdraw from your Bitcoin Wallet")
    @token_required
    def post(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404("User Not Found")
        #Withdraw from wallet

        return

@api.route("/sell")
class Sell(Resource):

    @api.doc(description="Sell Bitcoin")
    @token_required
    def post(self, user):
        # user = User.query.filter_by(public_id=id).first_or_404("User Not Found")
        #Sell Bitcoin

        return