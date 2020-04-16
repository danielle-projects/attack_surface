import pytest

from flask import request

import service.api as api
from service.consts import ApiConsts
# from service.graph_utils import GraphUtils


class TestAllRoutes(object):

    @pytest.fixture
    def client(self):
        with api.app.test_client() as client:
            yield client

    def test_stats_route(self, client):
        rv = client.get('/api/v1/stats')
        assert rv.status_code == ApiConsts.SUCCESSFUL_RESPONSE_CODE

    def test_attack_route(self, client):
        response = client.get('/api/v1/attack?vm_id=vm-9ea3998')
        assert response.status_code == ApiConsts.SUCCESSFUL_RESPONSE_CODE
        assert request.args['vm_id'] == 'vm-9ea3998'

    # def test_prepare_graph_edges(self):
    #     graph_edges = GraphUtils.prepare_graph_edges(self, vms_data=[], fw_rules_data=[])
    #     assert graph_edges == []


