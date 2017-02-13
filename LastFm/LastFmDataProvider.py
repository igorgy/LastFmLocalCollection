import pylast
from pylast import WSError
from DataProvider import DataProvider
from Band import Band, Tag

class LastFmDataProvider( DataProvider ):

    def __init__(self, key, secret):
        self.API_KEY = key
        self.API_SECRET = secret
        self.network = None

    def Connect( self ):
        self.network = pylast.LastFMNetwork(api_key = self.API_KEY, api_secret = self.API_SECRET)

    def GetBand( self, name ):
        try:
            artist = self.network.get_artist(name)
            tags = artist.get_top_tags()
            result_tag = list(map(lambda val: Tag(val.item.name, val.weight), tags))
            return Band(artist.name, result_tag)
        except WSError as ex:
            print(ex)
            return None
             