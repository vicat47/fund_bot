class User:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.bot_id = data.get('bot_id')
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return self.__str__()