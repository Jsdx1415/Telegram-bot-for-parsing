class Singleton:
    _instance = None

    def new(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).new(cls)
        return cls._instance

    def init(self):
        pass
