from pickle import dumps, loads
from hashlib import sha256
from logjacks_app.database.db import DateTime, LargeBinary, String, timezone, TypeDecorator


class Blob(TypeDecorator):
    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = loads(value)
        return value


class UTCDateTime(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, engine):
        if value is None:
            return
        if value.utcoffset() is None:
            raise ValueError('Got naive datetime while timezone-aware is expected')
        return value.astimezone(timezone.utc)

    def process_result_value(self, value, engine):
        if value is not None:
            x = value.replace(tzinfo=timezone.utc)
            return f'{x.month}/{x.day}/{x.year}'


class Sensitive(TypeDecorator):
    impl = String(64)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = sha256(value.encode('utf-8')).hexdigest()
        return value

    def process_result_value(self, value, dialect):
        return value