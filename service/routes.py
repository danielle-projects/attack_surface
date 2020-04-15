import time
import logging

from flask import request

from service.attack_surface import AttackSurfaceService
from service.consts import ApiConsts

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)


def configure_routes(app, input_file_path):
    attack_surface = AttackSurfaceService(
        input_file_path=input_file_path,
    )
    logger.info('attack surface configured properly')

    @app.route('/api/v1/stats', methods=['GET'])
    def stats():
        logger.info('stats endpoint was called')
        requests_count = attack_surface.request_count
        avg_process_time = \
            attack_surface.cumulative_process_time / requests_count \
            if requests_count > 0 else 0

        stats_dict = {
            'request_count': requests_count,
            'vm_count': attack_surface.vms_number,
            'average_request_time': round(
                avg_process_time,
                ApiConsts.ROUND_DECIMAL_NUMBER,
            ),
        }
        return stats_dict

    @app.route('/api/v1/attack', methods=['GET'])
    def attack():
        attack_surface.incr_req_counter()
        vm_id = request.args.get('vm_id')
        start_time = time.time()
        response = attack_surface.process_request(vm_id)
        request_time_ms = (time.time() - start_time) * 1000
        attack_surface.cumulative_process_time += request_time_ms
        return response
