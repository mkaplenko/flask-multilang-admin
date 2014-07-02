__author__ = 'mkaplenko'
import wtforms
import sqlalchemy as sa


class FieldContainer(object):
    _fields = []

    @property
    def fields(self):
        return {x.db_field: x for x in self._fields}

    def add_field(self, field):
        self._fields.append(field)


class AdminField(object):
    form_field = None
    db_field = None
    label = None

    def __init__(self, name=None, label=None, validators=None, filters=tuple(),
                 description='', id=None, default=None, widget=None,
                 _form=None, _name=None, _prefix='', _translations=None):

        self.name = name
        self.label = label if not self.label else self.label
        self.form_field_instance = self.form_field(label=label)

    def form_field_(self):

        return self.form_field_instance

fields = FieldContainer()


class StringField(AdminField):
    form_field = wtforms.StringField
    db_field = sa.String

fields.add_field(StringField)


class IntegerField(AdminField):
    form_field = wtforms.StringField
    db_field = sa.Integer

fields.add_field(IntegerField)


class BooleanField(AdminField):
    form_field = wtforms.BooleanField
    db_field = sa.Boolean

fields.add_field(BooleanField)
