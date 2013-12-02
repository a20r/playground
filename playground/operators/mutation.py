#!/usr/bin/env python
from random import random
from random import sample

from playground.tree import TreeNode
from playground.tree import TreeNodeType


class TreeMutation(object):
    def __init__(self, config):
        self.config = config

    def _gen_func_node(self, func_type, name):
        func_node = TreeNode(
            func_type,
            name=name
        )
        return func_node

    def _gen_term_node(self, name, value):
        term_node = TreeNode(
            TreeNodeType.TERM,
            name=name,
            value=value
        )
        return term_node

    def _gen_input_node(self, name):
        input_node = TreeNode(
            TreeNodeType.INPUT,
            name=name
        )
        return input_node

    def _gen_new_node(self, details):
        if details["type"] == TreeNodeType.UNARY_OP:
            return self._gen_func_node(details["type"], details["name"])
        elif details["type"] == TreeNodeType.BINARY_OP:
            return self._gen_func_node(details["type"], details["name"])
        elif details["type"] == TreeNodeType.TERM:
            name = getattr(details, "name", None)
            value = getattr(details, "value", None)
            return self._gen_term_node(name, value)
        elif details["type"] == TreeNodeType.INPUT:
            return self._gen_input_node(details["name"])

    def _get_new_node(self, node):
        # determine what kind of node it is
        t = node.node_type
        nodes = []
        if t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP:
            func_nodes = "function_nodes"
            nodes.extend(self.config[func_nodes])
        elif t == TreeNodeType.TERM or t == TreeNodeType.INPUT:
            term_nodes = "terminal_nodes"
            input_nodes = "input_nodes"
            nodes.extend(self.config[term_nodes])
            nodes.extend(self.config[input_nodes])

        # check the node and return
        while True:

            # obtain a new node
            new_node_details = sample(nodes, 1)[0]
            new_node = self._gen_new_node(new_node_details)

            if node.equals(new_node) is False:
                return new_node_details

    def point_mutation(self, tree, mutate_index=None):
        # mutate node
        node = sample(tree.program, 1)[0]
        new_node = self._get_new_node(node)

        t = node.node_type
        if t == TreeNodeType.UNARY_OP or t == TreeNodeType.BINARY_OP:
            node.name = new_node["name"]
        elif t == TreeNodeType.TERM or t == TreeNodeType.INPUT:
            node.name = new_node.get("name", None)
            node.value = new_node.get("value", None)

    def mutate(self, tree):
        method = self.config["mutation"]["method"]
        mutation_prob = self.config["mutation"]["probability"]
        prob = random()

        if mutation_prob >= prob:
            if method == "POINT_MUTATION":
                self.point_mutation(tree)
            else:
                raise RuntimeError("Undefined mutation method!")
