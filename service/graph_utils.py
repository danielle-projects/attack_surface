import itertools

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


class GraphUtils:

    def handle_graph(self, vms_data, fw_rules_data):
        nodes = [vm.vm_id for vm in vms_data]
        edges = self.prepare_graph_edges(vms_data, fw_rules_data)
        vms_graph = self.create_graph(nodes=nodes, edges=edges)
        self.create_graph_visualization(vms_graph)
        prepare_vm_potentials_attackers_dict = self.prepare_vm_potentials_attackers_dict(vms_graph)
        return prepare_vm_potentials_attackers_dict

    def prepare_graph_edges(self, vms_data, fw_rules_data):
        tag_vms_dict = self.prepare_tag_vms_dict(vms_data)
        edges = []
        for fw_rule in fw_rules_data:
            if (tag_vms_dict.get(fw_rule.source_tag) is not None) \
                    and (tag_vms_dict.get(fw_rule.dest_tag)):
                source_tag_vms = tag_vms_dict[fw_rule.source_tag]
                dest_tag_vms = tag_vms_dict[fw_rule.dest_tag]
                pairs_list = list(set(itertools.product(source_tag_vms, dest_tag_vms)))
                pairs_list_with_no_cycles = [pair for pair in pairs_list if pair[0] != pair[1]]
                for pair in pairs_list_with_no_cycles:
                    if pair not in edges:
                        edges.append(pair)
        return edges

    @staticmethod
    def prepare_tag_vms_dict(vms_data):
        tag_vms_dict = {}
        for vm in vms_data:
            for tag in vm.tags:
                if tag in tag_vms_dict:
                    tag_vms_dict[tag].append(vm.vm_id)
                else:
                    tag_vms_dict[tag] = [vm.vm_id]
        return tag_vms_dict

    @staticmethod
    def create_graph(nodes, edges):
        vms_graph = nx.DiGraph()
        vms_graph.add_nodes_from(nodes)
        vms_graph.add_edges_from(edges)
        return vms_graph

    @staticmethod
    def create_graph_visualization(graph):
        visual_graph = to_agraph(graph)
        visual_graph.layout('dot')
        visual_graph.draw('visual_graph.png')

    def prepare_vm_potentials_attackers_dict(self, graph):
        vm_potentials_attackers_dict = {node: [] for node in graph.nodes}
        for node in graph.nodes:
            self.bfs(graph, node, vm_potentials_attackers_dict)
        return vm_potentials_attackers_dict

    @staticmethod
    def bfs(graph, node, vm_potentials_attackers_dict):
        visited = []
        queue = [node]
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                neighbours = graph[node]
                for neighbour in neighbours:
                    queue.append(neighbour)
                    vm_potentials_attackers_dict[neighbour].append(node)
        return vm_potentials_attackers_dict
