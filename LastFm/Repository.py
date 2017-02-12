class Repository( object ):

    def Connect( self ):
        raise NotImplementedError( "Not Implemented" )

    def AddBand( self, band ):
        raise NotImplementedError( "Not Implemented" )

    def FindBand( self, name ):
        raise NotImplementedError( "Not Implemented" )

    def IterBand( self ):
        raise NotImplementedError( "Not Implemented" )