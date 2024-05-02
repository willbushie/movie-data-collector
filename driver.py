import requests

from movie import Movie

def readSecrets(filename):
	"""
	Read secrets file.
	@param filename - Filename of the secrets file.
	@return dict
	"""
	secrets = {}
	try:
		secretsFile = open(filename,'r')
		for line in secretsFile:
			splitLine = line.split('=')
			secrets.update({splitLine[0]:splitLine[1].strip('\n')})
	except (FileNotFoundError):
		raise FileNotFoundError
	return secrets

def readMovieList(filename):
	"""
	Read the movies list.
	@param filename - Filename of the movie list file.
	@return dict
	"""
	movies = {}
	try:
		movieFile = open(filename,'r')
		for line in movieFile:
			splitLine = line.split(',')
			currMovie = Movie(splitLine[0],splitLine[1].strip('\n'))
			movies.update({currMovie.getTitle:currMovie})
	except (FileNotFoundError):
		raise FileNotFoundError
	return movies

def readMaster(filename):
	"""
	Read master file, getting titles and returning them as a list.
	@param filename - Filename of the master file.
	@return list
	"""
	titles = []
	file = open(filename,'r')
	for line in file:
		splitLine = line.split('=')
		titles.append(splitLine[0])
	return titles

def createMoviesFromMaster(filename):
	"""
	Create Movie objects from reading the master file.
	@param filename - Filename of the master file.
	@return list
	"""
	movies = []
	file = open(filename,'r')
	for line in file:
		splitLine = line.split('=')
		title = splitLine[0]
		summary = splitLine[1].split(',')
		index = summary[1]
		year = summary[2]
		rating = summary[4]
		runtime = summary[3]
		currMovie = Movie(title,index)
		currMovie.setOthers(year,rating,runtime)
		movies.append(currMovie)
	return movies

def createMoviesFromNotFound(filename):
	"""
	Create Movie objects from reading the not found file. 
	@param filename - Filename of the not found file. 
	@return list
	"""
	movies = []
	file = open(filename,'r')
	for line in file:
		summary = line.split('=')[1].split(',')
		title = summary[0]
		index = summary[1]
		movies.append(Movie(title,index))
	return movies

def writeToMaster(filename, movie):
	"""
	Write to the end of the master file.
	@param filename - Filename of the master file.
	@param movie - Movie object with writeable data.
	"""
	with open(filename,'a+') as file:
		writeStr = f"{movie.getTitle()}={movie.getAllString()}={movie.getAPIResponse()}\n"
		file.seek(0,2)
		file.write(writeStr)
	file.close()

def writeCleanOutput(cleanFile, masterFile, notFoundFile):
	"""
	Write a clean CSV like output to the Clean file.
	@param cleanFile - Filename of the clean file.
	@param masterFile - Filename of the master file.
	"""
	cleanWrites = 0
	completedMovies = createMoviesFromMaster(masterFile)
	notFoundMovies = createMoviesFromNotFound(notFoundFile)
	with open(cleanFile,'w') as file:
		file.write('Movie Name,Index,Release Year,Length (Min),Rating\n')
		cleanWrites += 1
		for movie in completedMovies:
			file.write(f"{movie.getAllString()}\n")
			cleanWrites += 1
		for movie in notFoundMovies:
			file.write(f"{movie.getAllString()}\n")
			cleanWrites += 1
	file.close()
	print(f"Writes to clean file: {cleanWrites}")

def callAPI(APIKey, title):
	"""
	Call the OMDb API.
	@param APIKey - API Key, should be stored in secrets.
	@param title - Basic title of movie
	@return dict
	"""
	requestObj = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={APIKey}")
	if requestObj.status_code != 200:
		print(f"Failed {title} - response {requestObj.status_code}: {requestObj.json()}")
	elif requestObj.status_code == 200:
		return requestObj.json()

def process(APIKey, filename, master, movies, notFoundFile, notFound):
	"""
	Process all of the movies, requesting the API where necessary.
	@param APIKey - API Key, should be store in secrets.
	@param filename - filename of the master file.
	@param master - List of titles obtained from master file (prevents duplicate requests).
	@param movies - Dictionary of movies, searchable by title.
	@param notFoundFile - filename of the 'Not Found' file.
	@param notFound - List of movies that were previously not found (stops duplicate requests).
	@return list
	"""
	returnList = []
	masterWrites = 0
	notFoundWrites = 0
	movieList = movies.values()
	for movie in movieList:
		currTitle = movie.getTitle()
		if (currTitle not in master and currTitle not in notFound):
			response = callAPI(APIKey, movie.getTitle())
			movie.setAPIResponse(response)
			if (response.get('Error') == 'Movie not found!'):
				writeToMaster(notFoundFile,movie)
				notFoundWrites += 1
			elif (response.get('Error') != 'Movie not found!'):
				writeToMaster(filename, movie)
				masterWrites += 1
			returnList.append(movie)
	print(f"Writes to master file: {masterWrites} | Writes to not found file: {notFoundWrites}")
	return returnList

def main():
	print('begin processing...')

	secrets = readSecrets('secrets.txt')
	APIKey = secrets.get('OMDb API Key')
	movieListFile = secrets.get('Movie List')
	masterFile = secrets.get('Master File')
	notFoundFile = secrets.get('Not Found File')
	cleanFile = secrets.get('Clean Output')

	movies = readMovieList(movieListFile)
	masterList = readMaster(masterFile)
	notFound = readMaster(notFoundFile)

	resultList = process(APIKey, masterFile, masterList, movies, notFoundFile, notFound)
	writeCleanOutput(cleanFile, masterFile, notFoundFile)

	print('processing complete')

if __name__ == "__main__":
	main()
