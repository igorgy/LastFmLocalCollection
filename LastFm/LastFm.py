import sys
from PyQt5.QtWidgets import QApplication, QWidget
from band import Band, Tag
from ZODBRepository import ZODBRepository
from LastFmDataProvider import LastFmDataProvider
import os
import Config

dataProvider = LastFmDataProvider(Config.API_KEY, Config.API_SECRET)
dataProvider.Connect()

if not os.path.exists(Config.DB_PATH):
    os.makedirs(Config.DB_PATH)

repo = ZODBRepository(Config.DB_FILE) 
repo.Connect()

for dir in os.walk(Config.MUSIC_PATH):
    for name in dir[1]:
        try:
            band = dataProvider.GetBand(name)

            if band is not None and repo.FindBand(band.name) is None:
                repo.AddBand(band)

        except:
            print('Unexpected error:', sys.exc_info()[0])

app = QApplication(sys.argv)

w = QWidget()
w.resize(250, 150)
w.move(300, 300)
w.setWindowTitle('Simple')
w.show()
    
sys.exit(app.exec_())
