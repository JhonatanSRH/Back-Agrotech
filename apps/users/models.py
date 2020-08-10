"""Users models."""

from utils.firebase import fields
from utils.firebase.functions import FunctionsFirebase


class User(FunctionsFirebase):
    email = fields.EmailField()
    password = fields.CharField()
