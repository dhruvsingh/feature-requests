import os
import json
import unittest
import tempfile

from copy import deepcopy
from datetime import datetime

from dateutil.relativedelta import relativedelta

from fr_app import app
from fr_app.models import db, User, FeatureRequest, Client, ProductArea
from flask_fixtures import FixturesMixin


app.config.from_object('fr_app.settings.TestingConf')


class FeatureRequestTestCase(unittest.TestCase, FixturesMixin):
    fixtures = ['clients.json', 'product_areas.json', 'users.json']
    app, db = app, db
    post_data = {
        "user": 1,
        "client": 1,
        "product_area": 1,
        "title": "First Feature Request",
        "client_priority": 1,
        "description": "First Feature Request description",
        "target_date": str(datetime.utcnow().date())
    }

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

    def test_creating_feature_request_no_data(self):
        response = self.app.post('/api/feature_requests/add/', data=dict())
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'No input data provided'

    def test_creating_feature_request_valid_data(self):
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'

    def test_creating_feature_request_invalid_title(self):
        post_data = deepcopy(self.post_data)
        post_data['title'] = 'less'
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['title'][0] == \
            'Length must be between 6 and 255.'

    def test_creating_feature_request_past_target_date(self):
        post_data = deepcopy(self.post_data)
        now = datetime.utcnow().date()
        post_data['target_date'] = str(now - relativedelta(months=1))
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['target_date'][0] == \
            'Target date must be in the future'

    def test_creating_feature_request_negative_client_priority(self):
        post_data = deepcopy(self.post_data)
        post_data['client_priority'] = -1
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['client_priority'][0] == \
            'Must be at least 1.'

    def test_creating_feature_request_no_user_data(self):
        post_data = deepcopy(self.post_data)
        del post_data['user']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['user'][0] == \
            'Missing data for required field.'

    def test_creating_feature_request_no_client_data(self):
        post_data = deepcopy(self.post_data)
        del post_data['client']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['client'][0] == \
            'Missing data for required field.'

    def test_creating_feature_request_no_product_area_data(self):
        post_data = deepcopy(self.post_data)
        del post_data['product_area']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['product_area'][0] == \
            'Missing data for required field.'

    def test_creating_feature_request_no_title_data(self):
        post_data = deepcopy(self.post_data)
        del post_data['title']
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['errors']['title'][0] == \
            'Missing data for required field.'

    def test_creating_feature_request_check_client_priority_reordering(self):
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'
        first_id, first_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        assert first_id == 1
        assert first_client_priority == 1

        # sending same client_priority again will result in moving the first
        # priority to 2
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'
        second_id, second_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        first_fr = FeatureRequest.query.get(first_id)
        assert first_fr.id == 1
        # got reordered after adding another feature request
        assert first_fr.client_priority == 2
        assert second_id == 2
        assert second_client_priority == 1

    def test_creating_feature_request_check_client_priority_no_reordering(
            self):
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'
        first_id, first_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        assert first_id == 1
        assert first_client_priority == 1

        post_data = deepcopy(self.post_data)
        post_data['client_priority'] = 2
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'
        second_id, second_client_priority = \
            response_data['data'][0]['id'],\
            response_data['data'][0]['client_priority']

        first_fr = FeatureRequest.query.get(first_id)

        assert first_fr.id == 1
        # got reordered after adding another feature request
        assert first_fr.client_priority == 1
        assert second_id == 2
        assert second_client_priority == 2

    def test_updating_feature_request_description(self):
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'
        description = response_data['data'][0]['description']

        assert description == self.post_data['description']

        # update FR now
        self.post_data['description'] = "I updated description"
        response = self.app.post(
            '/api/feature_requests/1/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['data'][0]['description'] ==\
            self.post_data['description']

    def test_updating_feature_request_client_priority(self):
        """Create a feature with priority 1, and update it to 2"""
        response = self.app.post(
            '/api/feature_requests/add/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['message'] == 'Created new feature request.'
        client_priority = response_data['data'][0]['client_priority']

        assert client_priority == self.post_data['client_priority']

        # update FR now
        self.post_data['client_priority'] = 2
        response = self.app.post(
            '/api/feature_requests/1/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['data'][0]['client_priority'] ==\
            self.post_data['client_priority']

    def test_updating_feature_requests_client_priority(self):
        """
        Create feature requests with priority 1, and 2.
        Update the second one to be 3, check only 1 and 3 exist.
        """
        for turn in range(1, 3):
            self.post_data['client_priority'] = turn
            response = self.app.post(
                '/api/feature_requests/add/',
                data=json.dumps(self.post_data),
                content_type='application/json'
            )
            response_data = json.loads(response.get_data().decode('utf-8'))
            assert response_data['message'] == 'Created new feature request.'
            client_priority = response_data['data'][0]['client_priority']

        assert client_priority == self.post_data['client_priority']

        # update FR now
        self.post_data['client_priority'] = 3
        response = self.app.post(
            '/api/feature_requests/2/',
            data=json.dumps(self.post_data),
            content_type='application/json'
        )
        response_data = json.loads(response.get_data().decode('utf-8'))
        assert response_data['data'][0]['client_priority'] ==\
            self.post_data['client_priority']
        assert FeatureRequest.query.get(1).client_priority == 1
        assert FeatureRequest.query.get(2).client_priority == 3


if __name__ == '__main__':
    unittest.main()
