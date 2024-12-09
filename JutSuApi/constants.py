import requests

class SessionSingleton:
    _instance = None

    def __new__(cls):
        raise NotImplementedError("Instantiation through the constructor is not allowed. Use 'get_instance'.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = super(SessionSingleton, cls).__new__(cls)
            cls._instance._session = requests.Session()
            cls._instance._session.headers = {"User-Agent": "Mozilla/5.0"}
        return cls._instance._session