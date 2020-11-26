class Common:
    @classmethod
    def get_dict_data_by_path(cls, _dict, keys):
        return cls.get_dict_data_by_path(_dict[keys[0]], keys[1:]) \
            if keys else _dict

    @staticmethod
    def set_value_from_other_key_when_first_key_not_exist(_dict, first_key, second_key, default_value):
        if first_key not in _dict:
            _dict[first_key] = _dict.get(second_key, default_value)
        return _dict

    @staticmethod
    def logging_exceptions_and_bypass(f, *args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            print("we have a problem: {0}".format(e))
