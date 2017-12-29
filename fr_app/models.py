from fr_app import app
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy(app)


class User(db.Model):
    """
    User model to track who added the feature request.
    Can be used for auth too. TODO : add auth
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60))

    def __repr__(self):
        return '<User %r>' % self.first_name

    __str__ = __repr__


class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id'),
        nullable=False
    )
    client = db.relationship('Client', backref='feature_requests')
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    user = db.relationship('User', backref='feature_requests')
    client_priority = db.Column(db.Integer, default=1)
    product_area_id = db.Column(
        db.Integer,
        db.ForeignKey('product_area.id'),
        nullable=False
    )
    product_area = db.relationship('ProductArea', backref='feature_requests')
    target_date = db.Column(db.Date, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow())

    def __repr__(self):
        return '<FeatureRequest %r>' % self.title

    __str__ = __repr__


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Client %r>' % self.name

    __str__ = __repr__


class ProductArea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Product Area %r>' % self.name

    __str__ = __repr__
