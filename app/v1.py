from flask import Blueprint
from flask_restplus import Api

from .apis.auth import api as auth
from .apis.profiles import api as profiles
from .apis.users import api as users
# from apis.auth import api as auth

blueprint = Blueprint('v1', __name__, url_prefix='/api/V1')
api = Api(blueprint,
    title='Madcruz API',
    version='0.1.1',
    description='"Make requests to the Madcruz API"',
    # All API metadatas
)

# api.add_namespace(auth, path="/auth")
# api.add_namespace(profiles, path='/profiles')
# api.add_namespace(users, path="/users")
# api.add_namespace()