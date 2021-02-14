from flask import Blueprint
from flask_restplus import Api

from .utils import authorizations
from .apis.auth import api as auth
# from .apis.bitcoin import api as bitcoin
from .apis.permissions import api as permissions
from .apis.profiles import api as profiles
from .apis.users import api as users
# from apis.auth import api as auth

blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')
api = Api(blueprint,
    title='Madcruz API',
    version='0.1.1',
    description="Make requests to the Madcruz API",
    authorizations= authorizations,
    security='apikey'
    # All API metadatas
)

api.add_namespace(auth, path="/auth")
api.add_namespace(permissions, path="/permissions")
api.add_namespace(profiles, path='/profiles')
api.add_namespace(users, path="/users")
# api.add_namespace(bitcoin, path="/bitcoin")
# api.add_namespace()