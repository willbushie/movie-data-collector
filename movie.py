
class Movie:
    def __init__(self, title: str) -> None:
        """
        Create a Movie object with two required attributes.
        """
        self.title = title
        self.newTitle = ''
        self.year = ''
        self.imdbID = ''
        self.runtime = ''
        self.rating = ''
        self.apiResponse = ''
    
    def setAPIResponse(self, response: dict) -> None:
        """
        Set the API response attribute of the object.
        """
        self.apiResponse = response
        self.newTitle = self.apiResponse.get('Title','')
        self.year = self.apiResponse.get('Year','')
        self.imdbID = self.apiResponse.get('imdbID','')
        self.rating = self.apiResponse.get('Rated','')
        self.runtime = self.apiResponse.get('Runtime',' min').strip(' min')
        print(self.getAllString(','))
    
    def setOthers(self, year: int, rating: str, runtime: int) -> None:
        """
        Set object variables where needed.
        """
        self.year = year
        self.rating = rating
        self.runtime = runtime

    def getTitle(self) -> str:
        """
        Get user input movie title.
        """
        return self.title

    def getNewTitle(self) -> str:
        """
        Get correct movie title.
        """
        return self.newTitle
    
    def getAPIResponse(self) -> dict:
        """
        Get the API Response.
        """
        return self.apiResponse
    
    def getAllString(self, delim: str = '\t') -> str:
        """
        Return string format for output CSV.

        NOTE: The default delimiter is a tab (python `'\t'`) for easy copy/pasting into a spreadsheet.
        If a CSV output is desired, this layout may need to be modified.
        """
        returnStr = f"{self.title}{delim}{self.year}{delim}{self.imdbID}{delim * 2}{self.runtime}{delim}{self.rating}"
        return returnStr    
