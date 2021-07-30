from abc import ABC, abstractmethod
import json
import pickle



class SerializationInterface(ABC):

    @abstractmethod
    def serialize_data(self, data, path):
        pass

    @abstractmethod
    def deserialize_data(self, path):
        pass


class DictSerializeBIN(SerializationInterface):

    def serialize_data(self, data, path):
        if isinstance(data, dict):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError('Type of data is not a DICT')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, dict):
                return data
            else:
                raise ValueError('Type of data is not a DICT')

class ListSerializeBIN(SerializationInterface):
    
    def serialize_data(self, data, path):
        if isinstance(data, list):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError('Type of data is not a LIST')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, list):
                return data
            else:
                raise ValueError('Type of data is not a LIST')

class SetSerializeBIN(SerializationInterface):
    
    def serialize_data(self, data, path):
        if isinstance(data, set):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError('Type of data is not a SET')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, set):
                return data
            else:
                raise ValueError('Type of data is not a SET')

class DictSerializeJSON(SerializationInterface):

    def serialize_data(self, data, path):
        if isinstance(data, dict):
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError('Type of data is not a DICT')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            if isinstance(data, dict):
                return data
            else:
                raise ValueError('Type of data is not a DICT')

class ListSerializeJSON(SerializationInterface):

    def serialize_data(self, data, path):
        if isinstance(data, list):
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError('Type of data is not a LIST')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return data
            else:
                raise ValueError('Type of data is not a LIST')

class SetSerializeJSON(SerializationInterface):

    def serialize_data(self, data, path):
        if isinstance(data, set):
            data = list(data)
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError('Type of data is not a SET')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            if isinstance(data, list):
                data = set(data)
                return data
            else:
                raise ValueError('Type of data is not a LIST')

class TupleSerializeBIN(SerializationInterface):

    def serialize_data(self, data, path):
        if isinstance(data, tuple):
            with open(path, 'wb') as fh:
                pickle.dump(data, fh)
        else:
            raise ValueError('Type of data is not a TUPLE')

    def deserialize_data(self, path):
        with open(path, 'rb') as fh:
            data = pickle.load(fh)
            if isinstance(data, tuple):
                return data
            else:
                raise ValueError('Type of data is not a TUPLE')

class TupleSerializeJSON(SerializationInterface):

    def serialize_data(self, data, path):
        if isinstance(data, tuple):
            with open(path, 'w') as fh:
                json.dump(data, fh)
        else:
            raise ValueError('Type of data is not a TUPLE')

    def deserialize_data(self, path):
        with open(path, 'r') as fh:
            data = json.load(fh)
            data = tuple(data)
            if isinstance(data, tuple):
                return data
            else:
                raise ValueError('Type of data is not a TUPLE')


if __name__ == '__main__':

    dict_bin_file = 'dict.bin'
    json_dict_file = 'dict.json'
    base_dict = {'list': [1, 2, 3, 4, 5], 'dict': {'1': 'one', '2': 'two', '3': 'three'}}

    list_bin_file = 'list.bin'
    list_json_file = 'list.json'
    base_list = [1, 2, 3, "5", {3: "3"}, (1, 2, 3)]

    set_bin_file = 'set.bin'
    set_json_file = 'set.json'
    base_set = {1, 'a', 'v', '2', 5, 'a', 'j', 1, 'wqdd'}

    tuple_bin_file = 'tuple.bin'
    tuple_json_file = 'tuple.json'
    base_tuple = (1, 'a', 'v', '2', 5, 'a', 'j', 1, 'wqdd')


    DictSerializeBIN().serialize_data(base_dict, dict_bin_file)
    dict_to_bin = DictSerializeBIN().deserialize_data(dict_bin_file)

    DictSerializeJSON().serialize_data(base_dict, json_dict_file)
    dict_to_json = DictSerializeJSON().deserialize_data(json_dict_file)

    print(f'<DICT> base: {base_dict} \n  >>> bin: {dict_to_bin} \n  >>> json: {dict_to_json}\n\n')
   
    assert base_dict == dict_to_bin
    assert base_dict == dict_to_json

    ListSerializeBIN().serialize_data(base_list, list_bin_file)
    list_data_bin = ListSerializeBIN().deserialize_data(list_bin_file)

    ListSerializeJSON().serialize_data(base_list, list_json_file)
    list_data_json = ListSerializeJSON().deserialize_data(list_json_file)

    print(f'<LIST> base: {base_list} \n  >>> bin: {list_data_bin} \n  >>>> json: {list_data_json}\n\n')
  
    assert base_list == list_data_bin
    assert len(base_list) == len(list_data_json)

    SetSerializeBIN().serialize_data(base_set, set_bin_file)
    set_data_bin = SetSerializeBIN().deserialize_data(set_bin_file)

    SetSerializeJSON().serialize_data(base_set, set_json_file)
    set_data_json = SetSerializeJSON().deserialize_data(set_json_file)

    print (f'<SET> base: {base_set} \n  >>> bin: {set_data_bin} \n  >>> json: {set_data_json}\n\n')
    
    assert base_set == set_data_bin
    assert base_set == set_data_json


    TupleSerializeBIN().serialize_data(base_tuple, tuple_bin_file)
    tuple_data_bin = TupleSerializeBIN().deserialize_data(tuple_bin_file)

    TupleSerializeJSON().serialize_data(base_tuple, tuple_json_file)
    tuple_data_json = TupleSerializeJSON().deserialize_data(tuple_json_file)

    print (f'<TUPLE> base: {base_tuple} \n >>> bin: {tuple_data_bin} \n >>> json: {tuple_data_json}\n\n')
    
    assert base_tuple == tuple_data_bin
    assert base_tuple == tuple_data_json