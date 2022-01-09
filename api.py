from flask import json, render_template, make_response
from sqlalchemy import select
import connexion

import app
import orm

def getOrigins():
    if connexion.request.accept_mimetypes.accept_html :
        print('get origins from db')
        with app.sessionmaker.begin() as session:
            origins = session.execute(select(orm.Origin)).scalars().all()
            resp = make_response(render_template('origins.html', origins=origins), 200)
            return resp
    
    elif connexion.request.accept_mimetypes.accept_json :
        return json.jsonify([("hond", "Honduras"), ("col", "Colombia")])