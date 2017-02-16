import persistent
import itertools

class Band(persistent.Persistent):

    def __init__(self, name, tags):
        self.name = name 
        self.tags = tags   
    
    def GetTopTags(self, count):
        return itertools.islice(self.tags, count)

    def GetTopTagsString(self, count):
        return ', '.join(str(tag.name) for tag in self.GetTopTags(count))

class Tag(persistent.Persistent):

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight