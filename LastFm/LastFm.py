import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QPushButton, QProgressBar, QTableWidget, 
    QTableWidgetItem, QComboBox)
from PyQt5.QtCore import (QBasicTimer, Qt, QThread, pyqtSignal)
from Band import Band, Tag
from ZODBRepository import ZODBRepository
from LastFmDataProvider import LastFmDataProvider
import os
import Config
import Helper.Folder

header = ['Band Name', 'Top Tags']

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.update = QPushButton("Update", self)
        self.update.clicked.connect(self.doAction)

        self.step = 0
        self.genres = set()

        genreLabel = QLabel('Genre')
        review = QLabel('')

        self.updateProgress = QProgressBar(self)
        self.updateProgress.setAlignment(Qt.AlignCenter)

        self.genre = QComboBox()
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(header)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.update, 1, 0)
        grid.addWidget(self.updateProgress, 1, 1)

        grid.addWidget(genreLabel, 2, 0)
        grid.addWidget(self.genre, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(self.table, 3, 1, 5, 1)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 800, 640)
        self.setWindowTitle('Review')    
        self.show()

    def doAction(self):
        self.step = 0
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
        repo = ZODBRepository(Config.DB_FILE) 
        repo.Connect()

        self.updateProgress.reset() 
        self.update.setText('Update')

        for count, band in enumerate(repo.IterBand()):
            self.table.setRowCount(count + 1) 
            self.table.setItem(count, 0, QTableWidgetItem(band.name))
            self.table.setItem(count, 1, QTableWidgetItem(band.GetTopTagsString(10)))
            self.genres |= set(map(lambda val: val.name, band.GetTopTags(10)))


        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()  
        self.genre.addItems(sorted(self.genres))



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
            repo = ZODBRepository(Config.DB_FILE) 
            repo.Connect()

            dataProvider = LastFmDataProvider(Config.API_KEY, Config.API_SECRET)
            dataProvider.Connect()

            for dir in os.walk(Config.MUSIC_PATH):
                for name in dir[1]:
                    try:
                        self.sig_add.emit(name)

                        band = dataProvider.GetBand(name)

                        if band is not None and repo.FindBand(band.name) is None:
                            repo.AddBand(band)

                    except:
                        print('Unexpected error:', sys.exc_info()[0])
                break
            self.sig_done.emit()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
