# -*- coding: utf-8 -*-
""""
    app.model
    ~~~~~~~~~~

    This module implements the database tables using Flask-SqlAlchemy ORM.

"""

from app.extensions import db


class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return '<Feature %r>'.format(self.title)

    @staticmethod
    def reorder_priority(priority, client):
        """"
        Check the client priority and re-order them.
            Get all the priorities of a given client priority which is greater then it.
            If there are priorities greater then the given one, re-order their priority number.
        """

        features = Feature.query.filter(Feature.priority >= priority, Feature.client == client).all()
        if features:
            for feature in features:
                feature.priority += 1


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Client %r>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Product %r>'.format(self.name)
