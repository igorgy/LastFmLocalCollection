import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QPushButton, QProgressBar)
from PyQt5.QtCore import (QBasicTimer, Qt, QThread, pyqtSignal)
from band import Band, Tag
from ZODBRepository import ZODBRepository
from LastFmDataProvider import LastFmDataProvider
import os
import Config
import Helper.Folder

'''
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

it = repo.IterBand()
for b in it:
     print(b[1].name)
'''

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.update = QPushButton("Update", self)
        self.update.clicked.connect(self.doAction)

        self.step = 0

        author = QLabel('Author')
        review = QLabel('Review')

        self.updateProgress = QProgressBar(self)
        self.updateProgress.setAlignment(Qt.AlignCenter)

        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.update, 1, 0)
        grid.addWidget(self.updateProgress, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')    
        self.show()


    def doAction(self):
        count = Helper.Folder.fcount(Config.MUSIC_PATH)
        self.updateProgress.setMaximum(count)
        self.myThread = YourThreadName(self.add_band, self.done_addinf_band)
        self.myThread.start()
        self.update.setText('Stop')

    def add_band(self, name):
        self.step = self.step + 1
        self.updateProgress.setFormat(name)
        self.updateProgress.setValue(self.step)

    def done_addinf_band(self):
        self.updateProgress.reset() 
        self.update.setText('Update')

class YourThreadName(QThread):
    sig_add = pyqtSignal(str)
    sig_done = pyqtSignal()

    def __init__(self, add_band, done_addinf_band):
        QThread.__init__(self)
        self.sig_add.connect(add_band)
        self.sig_done.connect(done_addinf_band)

    def __del__(self):
        self.wait()

    def run(self):
            dataProvider = LastFmDataProvider(Config.API_KEY, Config.API_SECRET)
            dataProvider.Connect()

            if not os.path.exists(Config.DB_PATH):
                os.makedirs(Config.DB_PATH)

            repo = ZODBRepository(Config.DB_FILE) 
            repo.Connect()

            for dir in os.walk(Config.MUSIC_PATH):
                for name in dir[1]:
                    try:
                        
                        self.sig_add.emit(name)

                        band = dataProvider.GetBand(name)

                        if band is not None and repo.FindBand(band.name) is None:
                            repo.AddBand(band)

                    except:
                        print('Unexpected error:', sys.exc_info()[0])
            self.sig_done.emit()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
