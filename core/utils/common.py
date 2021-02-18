import requests


def update_account_status(social_network: str, account_id: str,
                          status_code: int, message: str = None):
    """Update status after collection process is Done"""
    payload = {
        "api_type": "UPDATE_STATUS",
        "api_body": {
            "social_network": social_network.upper(),
            "account_ID": account_id,
            "data": {
                "status_code": status_code,
                "message": message
            }
        }
    }
    requests.post(url="http://44.229.239.146:9099/update_status", json=payload)


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
