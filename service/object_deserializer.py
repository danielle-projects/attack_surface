from collections import defaultdict

from service.virtual_machine import VirtualMachine
from service.fw_rule import FwRule
from service.api_consts import APIConsts


class ObjectDeserializer:

    @staticmethod
    def parse_vms(raw_vms_data):
        if raw_vms_data is None:
            return []
        vms = [VirtualMachine(vm[APIConsts.VM_ID],
                              vm[APIConsts.NAME],
                              vm[APIConsts.TAGS])
               for vm in raw_vms_data
               if APIConsts.VM_ID and APIConsts.NAME and APIConsts.TAGS in vm]
        return vms

    @staticmethod
    def parse_fw_rules(raw_fw_rules_data):
        if raw_fw_rules_data is None:
            return []
        fw_rules = [FwRule(fw_rule[APIConsts.FW_ID],
                           fw_rule[APIConsts.SOURCE_TAG],
                           fw_rule[APIConsts.DEST_TAG])
                    for fw_rule in raw_fw_rules_data
                    if APIConsts.FW_ID and APIConsts.SOURCE_TAG and APIConsts.DEST_TAG in fw_rule]
        return fw_rules

    @staticmethod
    def prepare_tag_vms_dict(vms_data):
        tag_vm_dict = defaultdict(list)
        for vm in vms_data:
            for tag in vm.tags:
                tag_vm_dict[tag].append(vm.vm_id)
        return tag_vm_dict
