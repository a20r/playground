#1/usr/bin/env python
from random import randint

from playground.tree import TreeNodeType


class TreeMutation(object):
    def __init__(self, config):
        self.config = config

    def _get_new_node(self, node):
        t = node.node_type
        if (t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP):
            config_index = "function_nodes"
        elif t == TreeNodeType.TERM:
            config_index = "terminal_nodes"
        elif t == TreeNodeType.INPUT:
            config_index = "input_nodes"

        index = randint(0, len(self.config[config_index]) - 1)
        new_node = self.config[config_index][index]

        loop = True
        while loop:
            index = randint(0, len(self.config[config_index]) - 1)
            new_node = self.config[config_index][index]

            if new_node["type"] == TreeNodeType.TERM:
                if new_node["type"] == t and new_node["value"] != node.value:
                    loop = False
            else:
                if new_node["type"] == t and new_node["name"] != node.name:
                    loop = False

        return new_node

    def point_mutation(self, tree, mutate_index=None):
        # check mutation index
        if mutate_index is None:
            mutate_index = randint(0, len(tree.program) - 1)

        node = tree.program[mutate_index]
        if node.node_type == TreeNodeType.UNARY_OP:
            new_node = self._get_new_node(node)
            node.name = new_node["name"]
        elif node.node_type == TreeNodeType.BINARY_OP:
            new_node = self._get_new_node(node)
            node.name = new_node["name"]
        elif node.node_type == TreeNodeType.TERM:
            new_node = self._get_new_node(node)
            node.name = new_node["name"]
            node.value = new_node["value"]
        elif node.node_type == TreeNodeType.INPUT:
            new_node = self._get_new_node(node)
            node.name = new_node["name"]