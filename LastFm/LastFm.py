import sys
import pylast
import persistent
import ZODB, ZODB.FileStorage, transaction
import BTrees.OOBTree
from PyQt5.QtWidgets import QApplication, QWidget

class Band(persistent.Persistent):

    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class Tag(persistent.Persistent):

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "0ee0a0129dde72e07c362c8d02e9a0f9" # this is a sample key
API_SECRET = "b8c775442739058326fde7929fbcb3f2"

# In order to perform a write operation you need to authenticate yourself
username = "_psycho_"
password_hash = pylast.md5("123456")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)

# Now you can use that object everywhere
artist = network.get_artist("Mastodon")
tags = artist.get_top_tags()
res1 = list(map(lambda val: Tag(val.item.name, val.weight), tags))
band = Band(artist.name, res1)

storage = ZODB.FileStorage.FileStorage('mydata.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

#val = root.bands.iteritems()
#val = root.bands[band.name]
#root[band.name] = band
root.bands = BTrees.OOBTree.BTree()
root.bands[band.name] = band

transaction.commit()

connection.close()
db.close()
storage.close()

app = QApplication(sys.argv)

w = QWidget()
w.resize(250, 150)
w.move(300, 300)
w.setWindowTitle('Simple')
w.show()
    
sys.exit(app.exec_())
# print(band)
# res = list(map(lambda val: val.weight + " - " + val.item.name, tags))
# print('\n'.join(res))
#for val in tags:
#    print(val.weight + " - " + val.item.name)

# artist.shout("<3")


# track = network.get_track("Iron Maiden", "The Nomad")
# track.love()
# track.add_tags(("awesome", "favorite"))

# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter to get more help
# about anything and see examples of how it works