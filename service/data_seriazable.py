from service.virtual_machine import VirtualMachine
from service.fw_rules import FirewallRule


class DataSerializable:

    @staticmethod
    def parse_vms(raw_vms_data):
        if raw_vms_data is None:
            return []
        vms = [VirtualMachine(vm['vm_id'],
                              vm['name'],
                              vm['tags'])
               for vm in raw_vms_data]
        return vms

    @staticmethod
    def parse_fw_rules(raw_fw_rules_data):
        if raw_fw_rules_data is None:
            return []
        fw_rules = [FirewallRule(fw_rule['fw_id'],
                                 fw_rule['source_tag'],
                                 fw_rule['dest_tag'])
                    for fw_rule in raw_fw_rules_data]
        return fw_rules

    @staticmethod
    def prepare_tag_vms_dict(vms_data):
        tag_vm_dict = {}
        for vm in vms_data:
            for tag in vm.tags:
                if tag in tag_vm_dict:
                    tag_vm_dict[tag].append(vm.vm_id)
                else:
                    tag_vm_dict[tag] = [vm.vm_id]
        return tag_vm_dict
