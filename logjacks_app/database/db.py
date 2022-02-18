from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy, orm
from sqlalchemy.types import (
    Integer,
    TypeDecorator,
    LargeBinary,
    String,
    DateTime,
)
from sqlalchemy.schema import Column, Table
from logjacks_app import app

db = SQLAlchemy(app)

