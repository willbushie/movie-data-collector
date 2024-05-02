
class Movie:
    def __init__(self, title, index):
        """
        Create a Movie object with two required attributes.
        """
        self.title = title
        self.index = index
        self.newTitle = ''
        self.year = ''
        self.rating = ''
        self.runtime = ''
        self.apiResponse = ''
    
    def setAPIResponse(self, response):
        """
        Set the API response attribute of the object.
        @param response - JSON response from the API.
        """
        self.apiResponse = response
        self.newTitle = self.apiResponse.get('Title','')
        self.year = self.apiResponse.get('Year','')
        self.rating = self.apiResponse.get('Rated','')
        self.runtime = self.apiResponse.get('Runtime',' min').strip(' min')
        print(self.getAllString())
    
    def setOthers(self, year, rating, runtime):
        """
        Set object variables where needed.
        @param year - Release year.
        @param rating - Movie rating.
        @param runtime - Movie runtime.
        """
        self.year = year
        self.rating = rating
        self.runtime = runtime

    def getTitle(self):
        """
        Get movie title.
        @return str
        """
        return self.title
    
    def getAPIResponse(self):
        """
        Get the API Response
        @return dict
        """
        return self.apiResponse
    
    def getAllString(self):
        """
        Get everything (except API Response).
        @return str
        """
        return f"{self.title},{self.index},{self.year},{self.runtime},{self.rating}"
