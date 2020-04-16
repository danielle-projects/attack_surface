import itertools

import networkx as nx


class VMGraph:
    def __init__(self, vms_data, fw_rules_data):
        self.vm_graph = self.create_graph(vms_data, fw_rules_data)
        self.vm_potentials_attackers_dict = self.prepare_vm_potentials_attackers_dict(self.vm_graph)

    def prepare_graph_edges(self, vms_data, fw_rules_data):
        """
        This method does...
        :param vms_data: list of 'virtual_machine' objects.
        :param fw_rules_data: list of 'fw_rule' objects.
        :return: list of virtual machines pairs.
        """
        tag_vms_dict = self.prepare_tag_vms_dict(vms_data)
        edges = []
        for fw_rule in fw_rules_data:
            if (tag_vms_dict.get(fw_rule.src_tag) is not None) \
                    and (tag_vms_dict.get(fw_rule.dst_tag) is not None):
                source_tag_vms = tag_vms_dict[fw_rule.src_tag]
                dest_tag_vms = tag_vms_dict[fw_rule.dst_tag]
                pairs_list = list(itertools.product(source_tag_vms, dest_tag_vms))
                pairs_list_with_no_cycles = [pair for pair in pairs_list if pair[0] != pair[1]]
                for pair in pairs_list_with_no_cycles:
                    if pair not in edges:
                        edges.append(pair)
        return edges

    def prepare_tag_vms_dict(self, vms_data):
        """
        This method..
        :param vms_data: ist of 'virtual_machine' objects.
        :return: dictionary which all its keys are tags and theirs value is a list of all vms with this tag
        """
        tag_vms_dict = {}
        for vm in vms_data:
            for tag in vm.tags:
                if tag in tag_vms_dict:
                    tag_vms_dict[tag].append(vm.vm_id)
                else:
                    tag_vms_dict[tag] = [vm.vm_id]
        return tag_vms_dict

    def create_graph(self, vms_data, fw_rules_data):
        """
        Create the VM graph - the nodes are VM ids and the edges are FW rules connecting
        between VMs if they have the corresponding tags.
        :param vms_data:
        :param fw_rules_data:
        :return:
        """
        nodes = [vm.vm_id for vm in vms_data]
        edges = self.prepare_graph_edges(vms_data, fw_rules_data)
        vms_graph = nx.DiGraph()
        vms_graph.add_nodes_from(nodes)
        vms_graph.add_edges_from(edges)
        return vms_graph

    def prepare_vm_potentials_attackers_dict(self, vm_graph):
        """

        :param vm_graph:
        :return:
        """
        attack_surface_by_vm_dict = {node: [] for node in vm_graph.nodes}
        for node in vm_graph.nodes:
            self.bfs(vm_graph, node, attack_surface_by_vm_dict)
        return attack_surface_by_vm_dict

    @staticmethod
    def bfs(graph, start_node, vm_potentials_attackers_dict):
        """
        Executes a BFS to find all nodes that start_node can 'attack' (reach).
        :param graph: the vm graph
        :param start_node: the node to check on
        :param vm_potentials_attackers_dict: mutable dict that maps vms and who can reach them
        :return:
        """
        visited = []
        next_to_visit_queue = [start_node]
        while next_to_visit_queue:
            node = next_to_visit_queue.pop(0)
            if node not in visited:
                visited.append(node)
                neighbours = graph[node]
                for neighbour in neighbours:
                    next_to_visit_queue.append(neighbour)
                    vm_potentials_attackers_dict[neighbour].append(start_node)
        return vm_potentials_attackers_dict
