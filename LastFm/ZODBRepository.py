from Repository import Repository
import ZODB, ZODB.FileStorage, transaction
import BTrees.OOBTree
from band import Band, Tag

class ZODBRepository( Repository ):

    def __init__(self, dbPath):
        self.dbPath = dbPath
        self.storage = None
        self.db = None
        self.connection = None
        self.root = None

    def Connect( self ):
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
        return None if self.root.bands.has_key(name) is 0 else self.root.bands[name]

    def __del__(self):
        self.connection.close()
        self.db.close()
        self.storage.close()