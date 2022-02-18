from logjacks_app.database.db import db, datetime, timezone
from logjacks_app.database.datatypes import Sensitive, UTCDateTime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(UTCDateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    f_name = db.Column(db.String(128), nullable=False)
    l_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    phone = db.Column(db.String(32), nullable=True)
    company = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(Sensitive, nullable=False)
