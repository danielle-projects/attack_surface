import time

from flask import request

from service.attack_surface import AttackSurfaceService
from service.consts import ApiConsts


def configure_routes(app):
    attack_surface = AttackSurfaceService(
        input_file_path='/home/danielle/MyProj/attack_surface/data/input-3.json',
    )

    @app.route('/api/v1/stats', methods=['GET'])
    def stats():
        request_count = app.cache.get('request_count')
        avg_process_time = \
            attack_surface.cumulative_process_time / attack_surface.requests_count \
            if attack_surface.requests_count > 0 else 0

        stats_dict = {
            'cache_request_number': request_count,
            'request_count': attack_surface.requests_count,
            'vm_count': attack_surface.vms_number,
            'average_request_time': round(
                avg_process_time,
                ApiConsts.ROUND_DECIMAL_NUMBER,
            ),
        }
        return stats_dict

    @app.route('/api/v1/attack', methods=['GET'])
    def attack():
        request_current_count = app.cache.get('request_count')
        app.cache.set('request_count', request_current_count + 1)
        attack_surface.incr_req_counter()
        vm_id = request.args.get('vm_id')
        start_time = time.time()
        response = attack_surface.process_request(vm_id)
        request_time_ms = (time.time() - start_time) * 1000
        attack_surface.cumulative_process_time += request_time_ms
        return response
