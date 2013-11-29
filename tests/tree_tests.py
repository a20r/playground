#!/usr/bin/env python
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import playground.config as config
from playground.tree import Tree
from playground.tree import TreeNode
from playground.tree import TreeNodeType
from playground.tree import TreeNodeBranch
from playground.tree import TreeParser

# SETTINGS
config_fp = os.path.join(os.path.dirname(__file__), "config/tree.json")


class TreeNodeTests(unittest.TestCase):
    def setUp(self):
        self.left_node = TreeNode(TreeNodeType.TERM, value=1.0)
        self.left_node_2 = TreeNode(TreeNodeType.TERM, value=1.0)

        self.right_node = TreeNode(TreeNodeType.TERM, value=2.0)
        self.right_node_2 = TreeNode(TreeNodeType.TERM, value=2.0)

        self.binary_node = TreeNode(
            TreeNodeType.BINARY_OP,
            left_branch=self.left_node,
            right_branch=self.right_node
        )

    def test_has_value_node(self):
        # assert left branch
        res = self.binary_node.has_value_node(self.left_node)
        self.assertEquals(res, TreeNodeBranch.LEFT)

        # assert right branch
        res = self.binary_node.has_value_node(self.right_node)
        self.assertEqual(res, TreeNodeBranch.RIGHT)

        # assert fail left branch
        res = self.binary_node.has_value_node(self.left_node_2)
        self.assertFalse(res)

        # assert fail right branch
        res = self.binary_node.has_value_node(self.right_node_2)
        self.assertFalse(res)


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.config = config.load_config(config_fp)
        self.t_parser = TreeParser()
        self.tree = Tree()

        node_x = TreeNode(TreeNodeType.INPUT, name="x")
        node_y = TreeNode(TreeNodeType.INPUT, name="y")
        node_z = TreeNode(TreeNodeType.INPUT, name="z")

        self.tree.input_nodes.append(node_x)
        self.tree.input_nodes.append(node_y)
        self.tree.input_nodes.append(node_z)

    def test_valid(self):
        # assert valid
        res = self.tree.valid(self.config["input_nodes"])
        self.assertTrue(res)

        # assert fail valid
        self.tree.input_nodes.pop()
        res = self.tree.valid(self.config["input_nodes"])
        self.assertFalse(res)

    def test_get_linked_node(self):
        # setup
        del self.tree.input_nodes[:]
        left_node = TreeNode(TreeNodeType.INPUT, name="x")
        right_node = TreeNode(TreeNodeType.INPUT, name="y")
        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=left_node,
            right_branch=right_node
        )
        self.tree.root = add_func
        self.tree.program = self.t_parser.post_order_traverse(self.tree.root)

        # pass test
        linked_node = self.tree.get_linked_node(left_node)
        self.assertTrue(linked_node is add_func)
        linked_node = self.tree.get_linked_node(right_node)
        self.assertTrue(linked_node is add_func)

        # fail test
        random_node = TreeNode(TreeNodeType.INPUT, name="z")
        linked_node = self.tree.get_linked_node(random_node)
        self.assertFalse(linked_node is add_func)

    def test_equal(self):
        # create nodes
        left_node_1 = TreeNode(TreeNodeType.TERM, value=1.0)
        right_node_1 = TreeNode(TreeNodeType.TERM, value=2.0)

        left_node_2 = TreeNode(TreeNodeType.TERM, value=3.0)
        right_node_2 = TreeNode(TreeNodeType.TERM, value=4.0)

        cos_func_1 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node_1,
        )
        sin_func_1 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node_1,
        )

        cos_func_2 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="COS",
            value_branch=left_node_2,
        )
        sin_func_2 = TreeNode(
            TreeNodeType.UNARY_OP,
            name="SIN",
            value_branch=right_node_2,
        )

        add_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="ADD",
            left_branch=cos_func_1,
            right_branch=sin_func_1
        )

        sub_func = TreeNode(
            TreeNodeType.BINARY_OP,
            name="SUB",
            left_branch=sin_func_2,
            right_branch=cos_func_2
        )

        # create tree_1
        tree_1 = Tree()
        tree_1.root = add_func
        tree_1.update_program()
        tree_1.update_func_nodes()
        tree_1.update_term_nodes()

        # create tree_2
        tree_2 = Tree()
        tree_2.root = sub_func
        tree_2.update_program()
        tree_2.update_func_nodes()
        tree_2.update_term_nodes()

        self.assertTrue(tree_1.equals(tree_1))
        self.assertFalse(tree_1.equals(tree_2))
        self.assertTrue(tree_2.equals(tree_2))
        self.assertFalse(tree_2.equals(tree_1))


if __name__ == '__main__':
    unittest.main()