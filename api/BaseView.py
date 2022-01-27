from flask.views import MethodView
from flask import render_template, make_response
import connexion
import app

class BaseView(MethodView):

    def accept_html(self):
        return connexion.request.accept_mimetypes.accept_html

    def accept_json(self):
        return connexion.request.accept_mimetypes.accept_json

    def render_html(self, template, params=None, filters=None):
        return make_response(render_template(template, val=params, filters=filters), 200)

    def open_connection(self):
        return app.dbengine.connect()