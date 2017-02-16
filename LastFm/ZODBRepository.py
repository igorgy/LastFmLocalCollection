from Repository import Repository
import ZODB, ZODB.FileStorage, transaction
import BTrees.OOBTree
from Band import Band, Tag
import os

class ZODBRepository( Repository ):

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.storage = None
        self.db = None
        self.connection = None
        self.root = None

    def Connect( self ):
        dirname, __, file = self.dbPath.rpartition('\\')
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.storage = ZODB.FileStorage.FileStorage(self.dbPath)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()
        
        if hasattr(self.root, 'bands') is False:
            self.root.bands = BTrees.OOBTree.BTree()

    def AddBand( self, band ):
        self.root.bands[band.name] = band
        transaction.commit()

    def FindBand( self, name ):
        return self.root.bands.get(name, None)
        #return None if name not in self.root.bands else self.root.bands[name]

    def IterBand( self ):
        return self.root.bands.iteritems()

    def __del__(self):
        #transaction.commit()
        self.connection.close()
        self.db.close()
        self.storage.close()