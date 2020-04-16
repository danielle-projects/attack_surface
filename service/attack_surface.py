import json

from service.data_seriazable import DataSerializable
from service.graph_utils import GraphUtils


class AttackSurfaceService:
    def __init__(self, input_file_path):
        self.origin_service_input = self.get_service_input(input_file_path)
        self.vms_data = DataSerializable.parse_vms(self.origin_service_input['vms'])
        self.fw_rules_data = DataSerializable.parse_fw_rules(self.origin_service_input['fw_rules'])
        self.vm_potentials_attackers_dict = GraphUtils().handle_graph(vms_data=self.vms_data, fw_rules_data=self.fw_rules_data)
        self.request_count = 0
        self.cumulative_process_time = 0
        self.vms_number = len(self.vms_data)

    @staticmethod
    def get_service_input(input_file_path):
        try:
            with open(input_file_path) as json_file:
                service_data = json.load(json_file)
                return service_data
        except OSError:
            print('cannot open', input_file_path)
            return None
        else:
            print(input_file_path, 'has', len(f.readlines()), 'lines')
            return None

    def incr_req_counter(self):
        self.request_count += 1

    def process_request(self, vm_id):
        relevant_vms = f'{vm_id} doesn\'t exist in the data input'
        if vm_id in self.vm_potentials_attackers_dict:
            relevant_vms = self.vm_potentials_attackers_dict[vm_id]
        return json.dumps(relevant_vms)
