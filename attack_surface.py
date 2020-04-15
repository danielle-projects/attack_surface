import json
import itertools
from flask import Flask


class VirtualMachine:
    def __init__(self, vm_id, name, tags):
        self.vm_id = vm_id
        self.name = name
        self.tags = tags


class FirewallRule:
    def __init__(self, fw_id, source_tag, dest_tag):
        self.fw_id = fw_id
        self.source_tag = source_tag
        self.dest_tag = dest_tag


class AttackSurfaceService(Flask):
    def __init__(self, input_file_path):
        self.origin_service_input = self.get_service_input(input_file_path)
        self.vms_data = self.parse_vms()
        self.fw_rules_data = self.parse_fw_rules()
        self.edges = self.prepare_data_graph()
        self.requests_count = 0
        self.cumulative_process_time = 0
        self.vms_number = len(self.vms_data)

    @staticmethod
    def get_service_input(input_file_path):
        with open(input_file_path) as json_file:
            service_data = json.load(json_file)
            return service_data

    def parse_vms(self):
        vms = list()
        for vm in self.origin_service_input['vms']:
            vm_id = vm['vm_id']
            vm_name = vm['name']
            tags = vm['tags']
            vm = VirtualMachine(vm_id, vm_name, tags)
            vms.append(vm)
        return vms

    def parse_fw_rules(self):
        fw_rules = list()
        for fw_rule in self.origin_service_input['fw_rules']:
            fw_id = fw_rule['fw_id']
            source_tag = fw_rule['source_tag']
            dest_tag = fw_rule['dest_tag']
            rule = FirewallRule(fw_id, source_tag, dest_tag)
            fw_rules.append(rule)
        return fw_rules

    def incr_req_counter(self):
        self.requests_count += 1

    def prepare_data_graph(self):
        tag_vm_dict = {}
        for vm in self.vms_data:
            for tag in vm.tags:
                if tag in tag_vm_dict:
                    tag_vm_dict[tag].append(vm.vm_id)
                else:
                    tag_vm_dict[tag] = [vm.vm_id]
        edges = []
        for fw_rule in self.fw_rules_data:
            if (tag_vm_dict.get(fw_rule.source_tag) is not None) and (tag_vm_dict.get(fw_rule.dest_tag)):
                source_tag_vms = tag_vm_dict[fw_rule.source_tag]
                dest_tag_vms = tag_vm_dict[fw_rule.dest_tag]
                for src_vm in source_tag_vms:
                    for dst_vm in dest_tag_vms:
                        if not (src_vm, dst_vm) in edges:
                            edges.append((src_vm, dst_vm))
        return edges

    def process_request(self, vm_id):
        relevant_vms_pair = [vm_pair for vm_pair in self.edges if vm_id in vm_pair]
        nested_relevant_vms = list(set(itertools.chain.from_iterable(relevant_vms_pair)))
        nested_vms_json = json.dumps(nested_relevant_vms)
        return nested_vms_json



