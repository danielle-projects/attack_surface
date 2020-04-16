import json
import itertools
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


class VirtualMachine:
    def __init__(self, vm_id, vm_name, vm_tags):
        self.vm_id = vm_id
        self.name = vm_name
        self.tags = vm_tags


class FirewallRule:
    def __init__(self, fw_id, source_tag, dest_tag):
        self.fw_id = fw_id
        self.source_tag = source_tag
        self.dest_tag = dest_tag


class AttackSurfaceService:
    def __init__(self, input_file_path):
        self.origin_service_input = self.get_service_input(input_file_path)
        self.vms_data = self.parse_vms()
        self.fw_rules_data = self.parse_fw_rules()
        self.tag_vms_dict = self.prepare_tag_vms_dict()
        self.graph_edges = self.prepare_graph_edges()
        self.vms_graph = self.prepare_vms_graph()
        self.default_dict = self.process()
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

    def parse_vms(self):
        if self.origin_service_input is None:
            return []
        vms = [VirtualMachine(vm['vm_id'],
                              vm['name'],
                              vm['tags'])
               for vm in self.origin_service_input['vms']]
        return vms

    def parse_fw_rules(self):
        if self.origin_service_input is None:
            return []
        fw_rules = [FirewallRule(fw_rule['fw_id'],
                                 fw_rule['source_tag'],
                                 fw_rule['dest_tag'])
                    for fw_rule in self.origin_service_input['fw_rules']]
        return fw_rules

    def incr_req_counter(self):
        self.request_count += 1

    def prepare_tag_vms_dict(self):
        tag_vm_dict = {}
        for vm in self.vms_data:
            for tag in vm.tags:
                if tag in tag_vm_dict:
                    tag_vm_dict[tag].append(vm.vm_id)
                else:
                    tag_vm_dict[tag] = [vm.vm_id]
        return tag_vm_dict

    def prepare_graph_edges(self):
        edges = []
        for fw_rule in self.fw_rules_data:
            if (self.tag_vms_dict.get(fw_rule.source_tag) is not None) \
                    and (self.tag_vms_dict.get(fw_rule.dest_tag)):
                source_tag_vms = self.tag_vms_dict[fw_rule.source_tag]
                dest_tag_vms = self.tag_vms_dict[fw_rule.dest_tag]
                pairs_list = list(set(itertools.product(source_tag_vms, dest_tag_vms)))
                pairs_list_with_no_cycles = [pair for pair in pairs_list if pair[0] != pair[1]]
                for pair in pairs_list_with_no_cycles:
                    if pair not in edges:
                        edges.append(pair)
        return edges

    def process_request(self, vm_id):
        relevant_vms = f'{vm_id} doesn\'t exist in the data input'
        if vm_id in self.default_dict:
            relevant_vms = self.default_dict[vm_id]
        return json.dumps(relevant_vms)

    def prepare_vms_graph(self):
        vms_graph = nx.DiGraph()
        node_ids = [vm.vm_id for vm in self.vms_data]
        vms_graph.add_nodes_from(node_ids)
        vms_graph.add_edges_from(self.graph_edges)
        self.save_visual_graph(vms_graph)
        return vms_graph

    @staticmethod
    def save_visual_graph(graph):
        visual_graph = to_agraph(graph)
        visual_graph.layout('dot')
        visual_graph.draw('visual_graph.png')

    def process(self):
        default_dict = {node: [] for node in self.vms_graph.nodes}
        for node in self.vms_graph.nodes:
            self.bfs(self.vms_graph, node, default_dict)
        return default_dict

    @staticmethod
    def bfs(graph, node, default_dict):
        visited = []
        queue = [node]
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                neighbours = graph[node]
                for neighbour in neighbours:
                    queue.append(neighbour)
                    default_dict[neighbour].append(node)
        return default_dict
