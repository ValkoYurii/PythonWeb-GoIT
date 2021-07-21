from abc import ABC, abstractmethod
import json
import pickle

FILE_FORMAT = 'json'
BIN_FILE_NAME = 'сontainers.bin'
JSON_FILE_NAME = 'сontainers.json'


class SerializationInterface(ABC):
#Клас інтерфейс для класів серіалізації
    def __init__(self, data) -> None:
        self.data = data

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass


class BinSerialization(SerializationInterface):
# класс для сериализации всех контейнеров в bin
    def serialize(self):
        with open(BIN_FILE_NAME, 'wb') as f:
            pickle.dump(self.data, f)

    def deserialize(self):
        with open(BIN_FILE_NAME, 'rb') as f:
            self.data = pickle.load(f)


class SetToBinSerialization(BinSerialization):
    pass


class TupleToBinSerialization(BinSerialization):
    pass


class ListToBinSerialization(BinSerialization):
    pass


class DictToBinSerialization(BinSerialization):
    pass


class ListToJSONSerialization(SerializationInterface):
# класс для сериализации списка в JSON
    def serialize(self):
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(self.data, f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            self.data = json.load(f)


class SetToJSONSerialization(SerializationInterface):

    def serialize(self):
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(list(self.data), f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            self.data = set(json.load(f))


class TupleToJSONSerialization(SerializationInterface):

    def serialize(self):
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(list(self.data), f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            self.data = tuple(json.load(f))


class DictToJSONSerialization(SerializationInterface):

    def serialize(self):
        with open(JSON_FILE_NAME, 'w') as f:
            json.dump(self.data, f)

    def deserialize(self):
        with open(JSON_FILE_NAME, 'r') as f:
            self.data = json.load(f)
    

def define_serialization_type(container):
    
    if FILE_FORMAT == 'bin':
        if isinstance(container, set):
            cls = SetToBinSerialization
        elif isinstance(container, tuple):
            cls = TupleToBinSerialization
        elif isinstance(container, list):
            cls = ListToBinSerialization
        elif isinstance(container, dict):
            cls = DictToBinSerialization
        else:
            raise TypeError("The container has a not defined type")
    elif FILE_FORMAT == 'json':
        if isinstance(container, set):
            cls = SetToJSONSerialization
        elif isinstance(container, tuple):
            cls = TupleToJSONSerialization
        elif isinstance(container, list):
            cls = ListToJSONSerialization
        elif isinstance(container, dict):
            cls = DictToJSONSerialization
        else:
            raise TypeError("The container has a not defined type")
    return cls(container)


if __name__ == '__main__':
    
    containers = [(1, 4, 2, 6, 5), {1, 3}, [1, 22, 31, 4], {
        "one": 1, 2.0: "2", False: 3, True: 225.56, 5: None}]
    
    for FILE_FORMAT in ('json', 'bin'):
        for container in containers:
            a_object = define_serialization_type(container)
            print(a_object.__class__.__name__)
            print(f'Контейнер до серіалізації {container}')
            a_object.serialize()
            a_object.deserialize()
            print(f'Контейнер після десериалізації {a_object.data}')