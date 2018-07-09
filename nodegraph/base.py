import uuid


class BaseObject(object):
    def __init__(self, name):
        super(BaseObject, self).__init__()
        self._id = uuid.uuid4().hex
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def identifier(self):
        return '{name}-{id}'.format(name=self.name, id=self.id)

    def __repr__(self):
        return '<{class_}: {identifier}>'.format(
            class_=self.__class__.__name__,
            identifier=self.identifier)
