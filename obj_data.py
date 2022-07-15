
import pyTikZ.cls_points
import copy

class _clsdata(object):

    def __init__(self, type = None):

        self.__dict__['_data'] = dict()
        self._version = 0
        self.type = type

    def __deepcopy__(self, memo):
        obj = _clsdata()
        obj.__dict__['_data'] = copy.deepcopy(self.__dict__['_data'])
        return obj

    def __len__(self):
        return len(self._data)- 2

    def __getattr__(self, name):
        if name == "keys":
            lst = []
            for val in self.__dict__['_data'].keys():
                if val not in ["_version","type"]:
                    lst.append(val)
            return lst
        else:
            return self._data.get(name, None)

    def __setattr__(self, name, value):
        if self.type == type(value):
            pass
        else:
            self._data[name] = value
            pass

    def __getitem__(self, name):
        return self._data.get(name, None)

    def __setitem__(self, name, value):
        if self.type == type(value):
            pass
        else:
            self._data[name] = value
            pass

    def __delitem__(self, name):
        self._data.pop(name, None)

    def check_key(self, key):

        for _key in self._data.keys:

            if key == _key: return True

        return False

    def save_data(self, file_path):
        ### Save file
        """
        opt = wmcimgtools.load_options_files()

        opt.save_option_file(file_path, self._data, header = "\n")
        """
        pass

    def read_data(self, file_path):
        ### Read file
        """
        opt = wmcimgtools.load_options_files()

        dict = opt.read_option_file(file_path)

        self.__dict__['_data'] = dict

        return dict
        """
        pass
