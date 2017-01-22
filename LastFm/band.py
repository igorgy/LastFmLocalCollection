import persistent

class Band(persistent.Persistent):

    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class Tag(persistent.Persistent):

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight