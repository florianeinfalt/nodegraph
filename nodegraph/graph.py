import importlib
import subprocess

import networkx as nx

from base import BaseObject
from node import PythonNode


class DAG(BaseObject, nx.DiGraph):
    def __init__(self, name):
        super(DAG, self).__init__(name=name)
        self.graph['graph'] = {
            'rankdir': 'LR',
            'label': 'DAG: {name}'.format(name=self.name),
            'fontname': 'Ubuntu Mono derivative Powerline'
        }
        self.graph['node'] = {
            'shape': 'box',
            'fontname': 'Ubuntu Mono derivative Powerline'
        }
        self.graph['edges'] = {'arrowsize': '8.0'}

    @property
    def is_dag(self):
        return nx.algorithms.dag.is_directed_acyclic_graph(self)

    def to_dot(self, filename):
        nx.drawing.nx_pydot.write_dot(self, filename)

    def to_png(self, filename, dot_executable='/usr/local/bin/dot'):
        dot_filename = filename.replace('.png', '.dot')
        self.to_dot(dot_filename)
        subprocess.check_call([
            '{dot_executable} -Tpng {dot_filename} -o {png_filename}'.format(
                dot_executable=dot_executable,
                dot_filename=dot_filename,
                png_filename=filename)],
            shell=True)

    def evaluate(self):
        order = list(nx.topological_sort(self))
        for node in order:
            node.evaluate()
        return order[-1]

    def serialise(self):
        return {
            'module': self.__module__,
            'cls': self.__class__.__name__,
            'id': self.id,
            'name': self.name,
            'nodes': [node.serialise() for node in self.nodes]
        }

    @staticmethod
    def deserialise(data):
        cls = getattr(importlib.import_module(data['module']),
                      data['cls'], None)
        graph = cls(data['name'])
        graph.id = data['id']

        for node_data in data['nodes']:
            PythonNode.deserialise(node_data, graph)
        for node_data in data['nodes']:
            current_node = [node for node in graph.nodes
                            if node.id == node_data['id']][0]
            for name, input_ in node_data['inputs'].items():
                for identifier, plug in input_['connections'].items():
                    upstream = [node for node in graph.nodes
                                if node.identifier == identifier][0]
                    upstream.outputs[plug] >> current_node.inputs[name]
        return graph
