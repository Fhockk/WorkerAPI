from marshmallow import fields, ValidationError
from app.models import GenderEnum, LocationEnum, StatusEnum, SpecialtyEnum

from app import ma


class EnumField(fields.Field):
    def __init__(self, enum, *args, **kwargs):
        self._enum = enum
        super(EnumField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self._enum(value)
        except ValueError:
            raise ValidationError(f"Invalid value for enum {self._enum.__name__}.")


class GenderSchema(ma.Schema):
    name = EnumField(GenderEnum)

    class Meta:
        fields = ('id', 'name')


class UserSchema(ma.Schema):
    gender = ma.Nested(GenderSchema)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'address', 'gender')


class LocationSchema(ma.Schema):
    place = EnumField(LocationEnum)

    class Meta:
        fields = ('id', 'place')


class SpecialtySchema(ma.Schema):
    name = EnumField(SpecialtyEnum)

    class Meta:
        fields = ('id', 'name')


class WorkerSchema(ma.Schema):
    gender = ma.Nested(GenderSchema)
    specialty = ma.Nested(SpecialtySchema)

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'gender', 'specialty')


class ScheduleSchema(ma.Schema):
    location = ma.Nested(LocationSchema)
    worker = ma.Nested(WorkerSchema)
    user = ma.Nested(UserSchema)

    class Meta:
        fields = ('id', 'day', 'start_time', 'end_time', 'location', 'worker', 'user')


class StatusSchema(ma.Schema):
    name = EnumField(StatusEnum)

    class Meta:
        fields = ('id', 'name')


class AppointmentSchema(ma.Schema):
    status = ma.Nested(StatusSchema)

    class Meta:
        fields = ('id', 'day', 'start_time', 'end_time', 'status')
