import os
import unittest
import tempfile

from fr_app import app
from fr_app.models import db, User, FeatureRequest, Client, ProductArea
from flask_fixtures import FixturesMixin


app.config.from_object('fr_app.settings.TestingConf')


class FeatureRequestTestCase(unittest.TestCase, FixturesMixin):
    fixtures = ['clients.json', 'product_areas.json', 'users.json']
    app, db = app, db

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        db.drop_all()
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_product_area_data(self):
        """Test initial data for ProductArea model."""
        product_areas = ProductArea.query.all()
        assert len(product_areas) == ProductArea.query.count() == 4

    def test_client_data(self):
        """Test initial data for Client model."""
        clients = Client.query.all()
        assert len(clients) == Client.query.count() == 3

    def test_user_data(self):
        """Test initial data for User model."""
        users = User.query.all()
        assert len(users) == User.query.count() == 3

    def test_feature_request_data(self):
        """Test initial data for FeatureRequest model."""
        feature_requests = FeatureRequest.query.all()
        assert len(feature_requests) == FeatureRequest.query.count() == 0

if __name__ == '__main__':
    unittest.main()
