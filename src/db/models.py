from tortoise import fields
from tortoise.models import Model


class SomeModel(Model):
    server_id = fields.BigIntField()
