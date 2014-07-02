from flask import render_template
from flask.ext.wtf import Form
from .register import admin_register
from .fields import fields
import importlib
import dontworry


class AdminModule(object):
    model = None
    list_template = 'admin/admin_list.html'

    def __init__(self):
        self.__construct_fields()

    def get_list_fields(self):
        # self.__construct_fields()
        f = []
        for item in self.__dict__:
            f.append(self.__dict__[item])

        return f

    def get_objects(self):
        objects = self.model.query.all()
        return objects

    def get_object(self, object_id):
        return self.model.query.get(object_id)

    def render_form(self):
        form = self.__get_form()
        return form

    def __construct_fields(self):
        for column in self.model.__table__.columns:
            if not column.primary_key and not column.foreign_keys:
                setattr(self, column.name, fields.fields[type(column.type)].__call__(label=column.name, name=column.name))
            if column.foreign_keys:
                print('COLUMN ==> ', column.foreign_keys)

    def __get_form(self):
        # self.__construct_fields()

        # dontworry.dump(self)
        class admin_form(Form):
            pass

        for count, admin_field in enumerate(self.__dict__):
            setattr(admin_form, admin_field, self.__dict__[admin_field].form_field_instance)

        return admin_form


class Admin(object):
    modules = []
    app = None
    db = None

    def init_app(self, app=None, db=None):
        self.app = app
        self.db = db
        admin_register(app)

    @classmethod
    def site_register(cls, admin_module):
        cls.modules.append(admin_module())

    def get_module(self, module_name):
        getted_module = None
        for module in self.modules:
            if module.model.__tablename__ == module_name:
                getted_module = module
        return getted_module


admin=Admin()