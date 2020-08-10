import json, copy
from google.cloud import firestore
from django.core import checks, exceptions, validators
from django.db.models.query_utils import DeferredAttribute, RegisterLookupMixin
from django.utils.translation import gettext_lazy as _

class Empty:
    pass

class Field(RegisterLookupMixin):

	empty_values = list(validators.EMPTY_VALUES)
	default_error_messages = {
		'invalid': _('El campo no es valido'),
		'invalid_choice': _('Value %(value)r is not a valid choice.'),
		'null': _('This field cannot be null.'),
		'blank': _('This field cannot be blank.'),
		'unique': _('%(model_name)s with this %(field_label)s already exists.'),
		'unique_for_date': _("%(field_label)s must be unique for %(date_field_label)s %(lookup_type)s."),
    }

	def __init__(self, name=None, primary_key=False, max_length=None, decimal_places=None, blank=True, null=False, validators=[], default=None, choices=(), error_messages=None, auto_now=False, struct=None):
		self.name = name
		self.max_length = max_length
		self.decimal_places = decimal_places
		self.null = null
		self.validators = validators
		self.default = default
		self.value = self.default
		self.blank = blank
		self.choices = choices
		self.primary_key = primary_key
		self.auto_now = auto_now
		self.struct = struct
		messages = {}
		for c in reversed(self.__class__.__mro__):
			messages.update(getattr(c, 'default_error_messages', {}))
		messages.update(error_messages or {})
		self.error_messages = messages

	def validate(self, value, model_instance):
		if self.choices and value not in self.empty_values:
			for option_key, option_value in self.choices:
				if isinstance(option_value, (list, tuple)):
					for optgroup_key, optgroup_value in option_value:
						if value == optgroup_key:
							return
				elif value == option_key:
					return
			raise exceptions.ValidationError(
				self.error_messages['invalid_choice'],
				code='invalid_choice',
				params={'value': value},
			)
		if value is None and not self.null:
			raise exceptions.ValidationError(self.error_messages['null'], code='null')

		if not self.blank and value in self.empty_values:
			raise exceptions.ValidationError(self.error_messages['blank'], code='blank')

	def check(self):
		return [
			*self._check_field_name(),
			*self._check_validators(),
		]

	def _check_field_name(self):
		if self.name == None:
			return [
				'Field names cannot be null',
			]
		elif self.name == 'pk':
			return [
				"'pk' is a reserved word that cannot be used as a field name.",
			]
		else:
			return []

	def _check_validators(self):
		errors = []
		for i, validator in enumerate(self.validators):
			if not callable(validator):
				errors.append(
					"validators[{i}] ({repr}) isn't a function or "
					"instance of a validator class.".format(
						i=i, repr=repr(validator),
					)
				)
		return errors

	def run_validators(self, value):
		if value in self.empty_values:
			return
		errors = []
		for v in self.validators:
			print(v)
			try:
				v(value)

			except exceptions.ValidationError as e:
				if hasattr(e, 'code') and e.code in self.error_messages:
					e.message = self.error_messages[e.code]
				errors.extend(e.error_list)
		if errors:
			raise exceptions.ValidationError(errors)

	def to_python(self, value):
		return value

	def clean(self, value, model_instance):
		value = self.to_python(value)
		self.validate(value, model_instance)
		self.run_validators(value)
		return value

	def deconstruct(self):
		keywords = {}
		possibles = {
			"primary_key": False,
			"max_length": None,
			"unique": False,
			"blank": False,
			"null": False,
			"default": NOT_PROVIDED,
			"choices": [],
			"validators": [],
			"error_messages": None,
		}
		attr_overrides = {
			"unique": "_unique",
			"error_messages": "_error_messages",
			"validators": "_validators",
			"verbose_name": "_verbose_name",
			"db_tablespace": "_db_tablespace",
		}
		equals_comparison = {"choices", "validators"}
		for name, default in possibles.items():
			value = getattr(self, attr_overrides.get(name, name))
			if name == "choices" and isinstance(value, collections.abc.Iterable):
				value = list(value)
			if name in equals_comparison:
				if value != default:
					keywords[name] = value
			else:
				if value is not default:
					keywords[name] = value
		path = "%s.%s" % (self.__class__.__module__, self.__class__.__qualname__)
		if path.startswith("django.db.models.fields.related"):
			path = path.replace("django.db.models.fields.related", "django.db.models")
		if path.startswith("django.db.models.fields.files"):
			path = path.replace("django.db.models.fields.files", "django.db.models")
		if path.startswith("django.db.models.fields.proxy"):
			path = path.replace("django.db.models.fields.proxy", "django.db.models")
		if path.startswith("django.db.models.fields"):
			path = path.replace("django.db.models.fields", "django.db.models")
		return (self.name, path, [], keywords)

	def clone(self):
		name, path, args, kwargs = self.deconstruct()
		return self.__class__(*args, **kwargs)

	def __deepcopy__(self, memodict):
		obj = copy.copy(self)
		if self.remote_field:
			obj.remote_field = copy.copy(self.remote_field)
			if hasattr(self.remote_field, 'field') and self.remote_field.field is self:
				obj.remote_field.field = obj
		memodict[id(self)] = obj
		return obj

	def __copy__(self):
		obj = Empty()
		obj.__class__ = self.__class__
		obj.__dict__ = self.__dict__.copy()
		return obj

class CharField(Field):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#self.validators.append(validators.MaxLengthValidator(self.max_length))
		#self.validators=[validators.MaxLengthValidator(self.max_length)]

	def to_python(self, value):
		if isinstance(value, str) or value is None:
			return value
		return str(value)

class IntegerField(Field):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.validators = []

	def to_python(self, value):
		if value is None:
			return value
		try:
			return int(value)
		except (TypeError, ValueError):
			raise exceptions.ValidationError(
				self.error_messages['invalid'],
				code='invalid',
				params={'value': value},
			)

class BooleanField(Field):

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)
		self.validators = []

	def to_python(self,value):
		if value is None:
			return None
		if isinstance(value,bool):
			return value
		else:
			raise exceptions.ValidationError(
				self.error_messages['invalid'],
				code='invalid',
				params={'value': value},
			)

class ArrayField(Field):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.validators = []

	def to_python(self, value):
		if value is None:
			return value
		if isinstance(value, list) or isinstance(value, tuple):
			return value
		else:
			raise exceptions.ValidationError(
				self.error_messages['invalid'],
				code='invalid',
				params={'value': value},
			)

class JsonField(Field):

	def to_python(self, value):
		if value in [None, {}]:
			return value
		try:
			if not isinstance(value, dict):
				return json.loads(value)
			else:
				return value
		except (TypeError, ValueError):
			raise exceptions.ValidationError(
				self.error_messages['invalid'],
				code='invalid',
				params={'value': value},
			)

	def validate(self, value, model_instance):
		if value == None and (self.default == None or self.null == False):
			raise exceptions.ValidationError(
				self.error_messages['null'],
				code='invalid',
				params={'value': value},
			)
		if self.struct and (self.default == None or self.null == False):
			if len(value.keys()) != len(self.struct):
				raise exceptions.ValidationError(_('el campo no contiene las mismas propiedades. '+', '.join(self.struct)), code='invalid')
			elif len(set(value.keys()).intersection(self.struct)) != len(self.struct):
				raise exceptions.ValidationError(_('el campo no contiene las mismas propiedades. '+', '.join(self.struct)), code='invalid')

class DatetimeField(Field):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.auto_now:
			self.default = firestore.SERVER_TIMESTAMP
		self.validators = []

	def to_python(self, value):
		return value

class FloatField(Field):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.validators = []

	def to_python(self, value):
		if value is None:
			return value
		try:
			if self.decimal_places != None:
				decimal_format = "." + str(self.decimal_places) + "f"
				return float(format(value,decimal_format))
			return float(value)
		except (TypeError, ValueError):
			raise exceptions.ValidationError(
				self.error_messages['invalid'],
				code='invalid',
				params={'value': value},
			)
