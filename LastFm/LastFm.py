import sys
import pylast
from pylast import WSError
from PyQt5.QtWidgets import QApplication, QWidget
from band import Band, Tag
from ZODBRepository import ZODBRepository
import os

API_KEY = "0ee0a0129dde72e07c362c8d02e9a0f9" # this is a sample key
API_SECRET = "b8c775442739058326fde7929fbcb3f2"

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

if not os.path.exists('DB'):
    os.makedirs('DB')

repo = ZODBRepository('DB\mydata.fs') 

repo.Connect()

for dir in os.walk('..\Music'):
    for name in dir[1]:
        try:
            artist = network.get_artist(name)
            tags = artist.get_top_tags()
            result_tag = list(map(lambda val: Tag(val.item.name, val.weight), tags))
            band = Band(artist.name, result_tag)
            if repo.FindBand(band.name) is None:
                repo.AddBand(band)
        except WSError as ex:
            print(ex)
        except:
            print('Unexpected error:', sys.exc_info()[0])

app = QApplication(sys.argv)

w = QWidget()
w.resize(250, 150)
w.move(300, 300)
w.setWindowTitle('Simple')
w.show()
    
sys.exit(app.exec_())
