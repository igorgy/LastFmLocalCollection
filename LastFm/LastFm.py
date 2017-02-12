import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QTextEdit, QGridLayout, QApplication, QPushButton, QProgressBar)
from PyQt5.QtCore import (QBasicTimer, Qt)
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
'''
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

        self.timer = QBasicTimer()
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

    def timerEvent(self, e):
      
        if self.step >= 100:
            self.timer.stop()
            self.update.setText('Update')
            return
            
        self.step = self.step + 1
        self.updateProgress.setValue(self.step)
        self.updateProgress.setFormat('test' + str(self.step))

        

    def doAction(self):
      
        if self.timer.isActive():
            self.timer.stop()
            self.update.setText('Update')
        else:
            self.timer.start(100, self)
            self.update.setText('Stop')
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
