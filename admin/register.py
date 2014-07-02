__author__ = 'mkaplenko'
import importlib


def admin_register(app):
    if not app.config['BLUEPRINTS']:
        app.config['BLUEPRINTS'] = []

    app.config['BLUEPRINTS'].append('brpr_admin')
    for name in app.config['BLUEPRINTS']:
        try:
            m = importlib.import_module(name + '.admin')
        except ImportError:
            app.logger.debug('{0} blueprint does not have admin.py module.'.format(name))
        else:
            for _ in dir(m):
                app.logger.debug('Admin {0} registered'.format(name))
