import time
import logging

from flask import request

from service.attack_surface import AttackSurfaceService
from service.api_consts import APIConsts

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(filename='attack_surface_app.log', filemode='w')


def configure_routes(app):
    attack_surface = AttackSurfaceService(
        input_file_path=app.config['INPUT_FILE_PATH'],
    )

    @app.route('/api/v1/stats', methods=['GET'])
    def stats():
        logger.info(f'{time.time()} stats endpoint was called')
        attack_surface.incr_req_counter()
        requests_count = attack_surface.request_count
        avg_process_time = \
            attack_surface.cumulative_process_time / requests_count \
                if requests_count > 0 else 0

        stats_dict = {
            'request_count': requests_count,
            'vm_count': attack_surface.vms_number,
            'average_request_time': round(
                avg_process_time,
                APIConsts.ROUND_DECIMAL_COUNTER,
            ),
        }
        return stats_dict

    @app.route('/api/v1/attack', methods=['GET'])
    def attack():
        logger.info(f'{time.time()} - attack endpoint was called')
        attack_surface.incr_req_counter()
        vm_id = request.args.get('vm_id')
        start_time = time.time()
        response = attack_surface.process_request(vm_id)
        request_time_ms = ((time.time() - start_time) *
                           APIConsts.MICROSECOND_TO_MILLISECONDS_MULTIPLIER)
        attack_surface.cumulative_process_time += request_time_ms
        return response
