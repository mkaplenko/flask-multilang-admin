__author__ = 'mkaplenko'
from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask.ext.babel import gettext as _
from .models import admin
import dontworry


bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')
db = admin.db


@bp.route('/')
def admin_index():
    return '<h1>Admin Index</h1>'


@bp.route('/<module_name>/', methods=['GET', 'POST'])
def admin_list(module_name):
    admin_module = admin.get_module(module_name)
    objects = admin_module.get_objects()
    return render_template(admin_module.list_template,
                           objects=objects,
                           fields=admin_module.get_list_fields(),
                           getattr=getattr,
                           module_name=module_name
                           )


@bp.route('/<module_name>/add/', methods=['GET', 'POST'])
@bp.route('/<module_name>/<int:object_id>/', methods=['GET', 'POST'])
def edit_view(module_name, object_id=None):
    admin_module = admin.get_module(module_name)
    entity = admin_module.get_object(object_id) if object_id else admin_module.model()
    form_class = admin_module.render_form()
    form = form_class(obj=entity, csrf_enabled=False)

    if form.validate_on_submit():
        try:
            form.populate_obj(entity)

            # TODO: Set Attachments handler

            if not object_id:
                db.session.add(entity)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception(e)
        else:
            flash(_('Successfully saved') if object_id else _('Successfully added'), 'success')
            return redirect(url_for('.admin_list', module_name=module_name))

    return render_template('admin/admin_edit.html', form=form)