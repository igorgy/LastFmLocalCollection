class DataProvider( object ):

    def Connect( self ):
        raise NotImplementedError( "Not Implemented" )

    def GetBand( self, name ):
        raise NotImplementedError( "Not Implemented" )
