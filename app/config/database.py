from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


# Database ORM
db = SQLAlchemy()

# Database migrations configuration
migrate = Migrate()

# Serializer
ma = Marshmallow()

# JWT
jwt = JWTManager()
