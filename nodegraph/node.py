import json
import importlib

from abc import ABCMeta, abstractmethod

from base import BaseObject
from plug import InputPlug, OutputPlug

import ascii_print


class BaseNode(BaseObject):

    __metaclass__ = ABCMeta

    def __init__(self, name, graph, engine=None):
        super(BaseNode, self).__init__(name)
        self._inputs = {}
        self._outputs = {}
        self._graph = graph
        if not engine:
            raise ValueError('Must specify engine')
        self._engine = engine
        self._graph.add_node(self)

    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name.endswith('__'):
                try:
                    return self.outputs[name[:-2]]
                except KeyError:
                    pass
            elif name.startswith('__'):
                try:
                    return self.inputs[name[2:]]
                except KeyError:
                    pass
            else:
                raise

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def engine(self):
        return self._engine

    @property
    def graph(self):
        return self._graph

    @property
    def upstream_nodes(self):
        upstream_nodes = []
        for input_ in self.inputs.values():
            upstream_nodes += [connection.node for connection in
                               input_.connections]
        return list(set(upstream_nodes))

    @property
    def downstream_nodes(self):
        downstream_nodes = []
        for output in self.outputs.values():
            downstream_nodes += [connection.node for connection in
                                 output.connections]
        return list(set(downstream_nodes))

    @abstractmethod
    def _compute(self, **kwargs):
        pass

    def evaluate(self):
        inputs = dict()
        for name, plug in self.inputs.items():
            if not plug.value:
                raise ValueError(
                    'Input {input} on {node} does not have a value. '
                    'Assign an input or static value.'.format(
                        input=name, node=self.identifier))
            inputs[name] = plug.value
        outputs = self._compute(**inputs) or {}
        for name, value in outputs.items():
            self.outputs[name].value = value

        print('Evaluated: {}'.format(self.name))
        return outputs

    def serialise(self):
        return {
            'module': self.__module__,
            'cls': self.__class__.__name__,
            'id': self.id,
            'name': self.name,
            'engine': self.engine,
            'inputs': {k: v.serialise() for k, v in self.inputs.items()},
            'outputs': {k: v.serialise() for k, v in self.outputs.items()}
        }

    @staticmethod
    def deserialise(data, graph):
        cls = getattr(importlib.import_module(data['module']),
                      data['cls'], None)
        static_node_inputs = {
            input_['name']: input_['value'] for input_ in
            data['inputs'].values() if not input_['connections']
        }
        node = cls(data['name'], graph, **static_node_inputs)
        node.id = data['id']
        for name, input_ in data['inputs'].items():
            node._inputs[name].value = input_['value']
        for name, output_ in data['outputs'].items():
            node._outputs[name].value = output_['value']
        return node

    def plugs_from_template(self, template, locals):
        with open(template, 'r') as fp:
            node_data = json.load(fp)
        for input_name in node_data['inputs']:
            if input_name in locals:
                InputPlug(input_name, self, locals[input_name])
            else:
                InputPlug(input_name, self)
        for output_name in node_data['outputs']:
            OutputPlug(output_name, self)
        return self

    def __repr__(self):
        return '<Node: {identifier}>'.format(identifier=self.identifier)

    def __str__(self):
        return ascii_print.print_node(self)


class PythonNode(BaseNode):
    def __init__(self, name, graph, engine='python2.7'):
        super(PythonNode, self).__init__(name, graph, engine)

    def _compute(self, **kwargs):
        return self.compute(**kwargs)
