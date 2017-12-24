from .models import User, Client, ProductArea


def get_user_choices():
    return User.query.all()


def get_client_choices():
    return Client.query.all()


def get_product_areas_choices():
    return ProductArea.query.all()
