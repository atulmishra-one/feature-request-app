# -*- coding: utf-8 -*-
""""
    app.api
    ~~~~~~~~

    This module encapsulates the REST application.

"""

from datetime import datetime

from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from sqlalchemy import exc

from app.extensions import db
from app.model import Feature
from app.model import Client
from app.model import Product


api_views = Blueprint('api', __name__, url_prefix='/api')


@api_views.route('list_features', methods=['GET', ])
def list_features():
    try:
        features = Feature.query.join(Product).join(Client).add_columns(
            Product.name.label('product_name'),
            Client.name.label('client_name'),
            Feature.id,
            Feature.title,
            Feature.priority,
            Feature.description,
            Feature.target_date
        ).filter(
            Feature.product == Product.id,
            Feature.client == Client.id
        ).order_by(Feature.id.desc()).all()
    except exc.OperationalError as e:
        abort(make_response(jsonify(message="Database Error {0}".format(e)), 400))

    results = [
        {
            'id': feature.id,
            'title': feature.title,
            'priority': feature.priority,
            'description': feature.description,
            'target_date': feature.target_date.strftime("%Y/%m/%d"),
            'client': feature.client_name,
            'product': feature.product_name
         }
        for feature in features
    ]
    return jsonify(results)


@api_views.route('request_new_feature', methods=['POST', ])
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
        product = data['product']

        today = datetime.now()
        if target_date < today:
            abort(make_response(jsonify(message="Target date cannot be in past."), 400))

        Feature.reorder_priority(priority, client)  # Test and Re-Order Priority
        new_feature = Feature(
            title=title,
            description=description,
            client=client,
            priority=priority,
            target_date=target_date,
            product=product
        )
        db.session.add(new_feature)
        db.session.commit()
    except KeyError as e:
        abort(make_response(jsonify(message="Missing Key {0}".format(e)), 400))
    except exc.OperationalError as e:
        abort(make_response(jsonify(message="Database Error {0}".format(e)), 400))
    except exc.SQLAlchemyError as e:
        abort(make_response(jsonify(message="Database Error {0}".format(e)), 400))

    return jsonify(message="Feature was created successfully")


@api_views.route('clients', methods=['GET', ])
def client_values():
    clients = Client.query.all()
    results = [{"id": client.id, "name": client.name} for client in clients]
    return jsonify(results)


@api_views.route('products', methods=['GET', ])
def products_values():
    products = Product.query.all()
    results = [{"id": product.id, "name": product.name} for product in products]
    return jsonify(results)


@api_views.route('delete_feature', methods=['DELETE', ])
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
