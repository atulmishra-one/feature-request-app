""""App views
This views serves all the static pages of the feature app

"""

from flask import Blueprint
from flask import render_template
from flask import jsonify
from app.model import Feature
from flask import request
from flask import abort
from flask import make_response
from app.extensions import db
from sqlalchemy import exc

from datetime import datetime

app_views = Blueprint('views', __name__, url_prefix='/')


@app_views.route('')
def index():
    return render_template("index.html")


@app_views.route('/request_feature')
def request_feature():
    return render_template("create_feature.html")


@app_views.route('/api/list_features', methods=['GET', ])
def list_features():
    features = Feature.query.order_by(Feature.id.desc()).all()
    results = [
        {
            'id': feature.id,
            'title': feature.title,
            'priority': feature.priority,
            'description': feature.description,
            'target_date': feature.target_date,
            'client': feature.client,
            'product_area': feature.product_area
         }
        for feature in features
    ]
    return jsonify(results)


@app_views.route('/api/request_new_feature', methods=['POST', ])
def request_new_feature():
    data = request.get_json()
    if data is None:
        abort(400)
    try:
        priority = int(data['priority'])
        client = data['client']
        title = data['title']
        target_date = datetime.strptime(data['target_date'], "%Y-%m-%d")
        description = data['description']
        product_area = data['product_area']
        new_feature = Feature(
            title=title,
            description=description,
            client=client,
            priority=priority,
            target_date=target_date,
            product_area=product_area
        )
        db.session.add(new_feature)
        Feature.reorder_priority(priority, client)
        db.session.commit()
    except KeyError as e:
        abort(make_response(jsonify(message="Missing Key {0}".format(e)), 400))
    except exc.IntegrityError as e:
        abort(make_response(jsonify(message="Database Error {0}".format(e)), 400))
    except exc.SQLAlchemyError as e:
        abort(make_response(jsonify(message="Database Error {0}".format(e)), 400))

    return jsonify(message="Feature was created successfully")


@app_views.route('/api/client_values', methods=['GET', ])
def client_values():
    results = [
        {"name": "Client A", "id": "A"},
        {"name": "Client B", "id": "B"},
        {"name": "Client C", "id": "C"}
    ]
    return jsonify(results)


@app_views.route('/api/areas_values', methods=['GET', ])
def areas_values():
    results = [
        {"name": "Policies", "id": "Policies"},
        {"name": "Billings", "id": "Billings"},
        {"name": "Claims", "id": "Claims"},
        {"name": "Reports", "id": "Reports"}
    ]
    return jsonify(results)


@app_views.route('/api/delete_feature', methods=['DELETE', ])
def delete_feature():
    data = request.get_json()
    if data is None:
        abort(400)
    try:
        feature_id = data['id']
        feature_to_delete = Feature.query.get(feature_id)
        db.session.delete(feature_to_delete)
        db.session.commit()
    except KeyError as e:
        abort(make_response(jsonify(message="Missing Key {0}".format(e)), 400))
    except exc.SQLAlchemyError as e:
        abort(make_response(jsonify(message="Database Error {0}".format(e)), 400))
    return jsonify(success=True)
