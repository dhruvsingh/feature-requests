from fr_app import app
from flask import render_template, request, jsonify
from .models import db, User, Client, ProductArea, FeatureRequest
from .schema import (
    UserSchema,
    ClientSchema,
    ProductAreaSchema,
    FeatureRequestSchema
)


def _build_feature_request_data(feature_request, data):
    for field in [
        "title",
        "user_id",
        "client_id",
        "description",
        "target_date",
        "client_priority",
        "product_area_id"
    ]:
        setattr(feature_request, field, data.get(field, None))

    return feature_request


@app.route('/')
def home_page():
    return render_template(
        'index.html',
        title='All Requests',
        home_active='active',
    )


@app.route('/api/users/', methods=('GET',))
def get_users():
    """Fetch all users."""
    users = User.query.all()
    users_schema = UserSchema()
    result = users_schema.dump(users, many=True)
    return jsonify({'users': result.data})


@app.route('/api/product_areas/', methods=('GET',))
def get_product_areas():
    """Fetch all product areas."""
    product_areas = ProductArea.query.all()
    pa_schema = ProductAreaSchema()
    result = pa_schema.dump(product_areas, many=True)
    return jsonify({'product_areas': result.data})


@app.route('/api/clients/', methods=('GET',))
def get_clients():
    """Fetch all clients."""
    clients = Client.query.all()
    clients_schema = ClientSchema()
    result = clients_schema.dump(clients, many=True)
    return jsonify({'clients': result.data})


@app.route('/api/feature_requests/', methods=('GET',))
def get_feature_requests():
    """Fetch all feature_requests."""
    feature_requests = FeatureRequest.query.all()
    feature_requests_schema = FeatureRequestSchema()
    result = feature_requests_schema.dump(feature_requests, many=True)
    return jsonify({'feature_requests': result.data})


@app.route('/api/feature_requests/<int:id>/', methods=('GET', 'POST'))
def fetch_feature_request_by_id(id=None):
    """Add/update a feature request."""
    if not id:
        return jsonify(
            {"message": "Feature Request id is needed."}
        ), 400

    feature_requests_schema = FeatureRequestSchema()
    json_data = request.get_json()
    feature_request = FeatureRequest.query.get(id)

    if not feature_request:
        return jsonify(
            {"message": "Feature Request could not be found."}
        ), 400

    result = feature_requests_schema.dump(feature_request)

    # if no json data came in consider the request as GET
    if not json_data:
        return jsonify({"feature_request": result.data})

    # POST request
    data, errors = feature_requests_schema.load(json_data)

    if errors:
        return jsonify({"errors": errors}), 422

    feature_request = _build_feature_request_data(feature_request, data)

    db.session.add(feature_request)
    db.session.commit()

    return jsonify(
        {
            "message": "Updated feature request.",
            "data": FeatureRequestSchema().dump(feature_request)
        }
    ), 200


@app.route('/api/feature_requests/add/', methods=('POST',))
def add_feature_request():
    """Add feature request."""
    feature_requests_schema = FeatureRequestSchema()
    json_data = request.get_json()

    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    data, errors = feature_requests_schema.load(json_data)

    if errors:
        return jsonify({"errors": errors}), 400

    feature_request = FeatureRequest()
    feature_request = _build_feature_request_data(feature_request, data)

    db.session.add(feature_request)
    db.session.commit()

    return jsonify(
        {
            "message": "Created new feature request.",
            "data": FeatureRequestSchema().dump(feature_request)
        }
    ), 201
