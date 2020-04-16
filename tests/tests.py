import pytest

from flask import request

import service.api as api
from service.api_consts import APIConsts


class TestAllRoutes(object):

    @pytest.fixture
    def client(self):
        with api.app.test_client() as client:
            yield client

    def test_stats_route(self, client):
        rv = client.get('/api/v1/stats')
        assert rv.status_code == APIConsts.SUCCESSFUL_RESPONSE_CODE

    def test_attack_route(self, client):
        response = client.get('/api/v1/attack?vm_id=vm-9ea3998')
        assert response.status_code == APIConsts.SUCCESSFUL_RESPONSE_CODE
        assert request.args['vm_id'] == 'vm-9ea3998'


