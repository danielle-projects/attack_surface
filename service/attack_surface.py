import json

from service.object_deserializer import ObjectDeserializer
from service.vms_graph import VMGraph
from service.api_consts import APIConsts


class AttackSurfaceService:
    def __init__(self, input_file_path):
        self.origin_service_input = self.get_service_input(input_file_path)
        vms_data = ObjectDeserializer.parse_vms(self.origin_service_input[APIConsts.VMS])
        fw_rules_data = ObjectDeserializer.parse_fw_rules(self.origin_service_input[APIConsts.FW_RULES])
        self.vm_potentials_attackers_dict = VMGraph(vms_data, fw_rules_data).vm_potentials_attackers_dict
        self.request_count = 0
        self.cumulative_process_time = 0
        self.vms_number = len(vms_data)

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
