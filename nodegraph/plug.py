from abc import ABCMeta, abstractmethod

from base import BaseObject


class BasePlug(BaseObject):

    __metaclass__ = ABCMeta

    def __init__(self, name, node, valid_plugs):
        super(BasePlug, self).__init__(name)
        self._node = node
        self._value = None
        self._valid_plugs = valid_plugs
        self._connections = []

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        if self._node:
            raise ValueError('Node is immutable once set')
        self._node = value

    @property
    def connections(self):
        return self._connections

    @property
    def is_connected(self):
        return bool(self.connections)

    @abstractmethod
    def connect(self, plug):
        pass

    def disconnect(self, plug):
        if plug in self.connections:
            self.connections.pop(self.connections.index(plug))
        if self in plug.connections:
            plug.connections.pop(plug.connections.index(self))
        self.node.graph.remove_edge(self.node, plug.node)

    def serialise(self):
        return {
            'name': self.name,
            'value': self.value,
            'connections': {connection.node.identifier:
                            connection.name for connection in self.connections}
        }


class OutputPlug(BasePlug):
    def __init__(self, name, node):
        super(OutputPlug, self).__init__(name, node, (InputPlug, ))
        self.node.outputs[self.name] = self

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        for plug in self.connections:
            plug.value = value

    def connect(self, plug):
        if plug.node is self.node:
            raise Exception('Cannot connect plugs on the same node')

        if plug not in self._connections:
            self._connections.append(plug)
            plug.value = self.value
        if self not in plug._connections:
            plug._connections = [self]
        self.node.graph.add_edge(self.node, plug.node)

    def __rshift__(self, plug):
        if isinstance(plug, self._valid_plugs):
            self.connect(plug)

    def __floordiv__(self, plug):
        if isinstance(plug, self._valid_plugs):
            self.disconnect(plug)


class InputPlug(BasePlug):
    def __init__(self, name, node, value=None):
        super(InputPlug, self).__init__(name, node, (OutputPlug, ))
        self.node.inputs[self.name] = self
        self.value = value

    def connect(self, plug):
        self.connections = [plug]
        if self not in plug.connections:
            plug.connections.append(self)
