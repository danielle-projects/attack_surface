import time

from flask import Flask, request

from attack_surface import AttackSurfaceService
from consts import AttackSurfaceConsts, ApiConsts

app = Flask(__name__)

attack_surface = AttackSurfaceService(input_file_path=AttackSurfaceConsts.FILE_PATH_INPUT)


@app.route('/api/v1/stats', methods=['GET'])
def stats():
    avg_process_time = 0
    if attack_surface.requests_count > 0:
        avg_process_time = attack_surface.cumulative_process_time / attack_surface.requests_count
    stats_dict = {
        'request_count': attack_surface.requests_count,
        'vm_count': attack_surface.vms_number,
        'average_request_time': round(avg_process_time,
                                      ApiConsts.ROUND_DECIMAL_NUMBER),
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


if __name__ == '__main__':
    #AttackSurfaceService(input_file_path='src/input-0.json')
    app.run(debug=True)

