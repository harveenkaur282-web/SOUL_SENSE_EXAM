from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import only existing models
from .reflection import UserReflection

# Expose Base for db usage
# DO NOT import non-existent files until they are created
