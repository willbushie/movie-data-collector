import requests
import json

from movie import Movie

def readSecrets(filename: str) -> dict:
	"""
	Read secrets file.
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

def readInput(filename: str) -> dict:
	"""
	Read the input file & return dict of movie objects.
	"""
	movies = {}
	try:
		movieFile = open(filename,'r')
		for line in movieFile:
			currMovie = Movie(line.strip('\n'))
			movies.update({currMovie.getTitle():currMovie})
	except (FileNotFoundError):
		raise FileNotFoundError
	return movies

def readLocalDB(filename: str) -> list:
	"""
	Read local DB file into memory.
	"""
	titles = []
	file = open(filename,'r')
	for line in file:
		splitLine = line.split('=')
		titles.append(splitLine[0])
	return titles

def createMoviesFromLocalDB(filename: str) -> list:
	"""
	Create Movie objects from reading the local DB file.
	"""
	movies = []
	file = open(filename,'r')
	for line in file:
		lineDict = json.loads(line)
		currMovie = Movie(lineDict.get('Title',''))
		currMovie.setAPIResponse(lineDict)
		movies.append(currMovie)
	return movies

def writeToLocalDB(filename: str, movie: Movie) -> None:
	"""
	Write to the end of the local DB file.
	"""
	with open(filename,'a+') as file:
		writeStr = f"{movie.getAPIResponse()}\n"
		file.seek(0,2)
		file.write(writeStr)
	file.close()

def writeOutput(output: str, movieList: list[Movie]) -> None:
	"""
	Write a clean CSV like output to the Clean file.
	"""
	cleanWrites = 0
	with open(output,'w') as file:
		file.write('Movie Name,Release Year,imdbid,Format On NAS,Length (Min),'
			 'Rating,Disc Type,Date Ripped,Receipt,Cost,Note\n')
		cleanWrites += 1
		for movie in movieList:
			file.write(f"{movie.getAllString()}\n")
			cleanWrites += 1
	file.close()
	print(f"Writes to clean file: {cleanWrites}")

def callAPI(APIKey: str, title: str) -> dict:
	"""
	Call the OMDb API.
	"""
	requestObj = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={APIKey}")
	if requestObj.status_code != 200:
		print(f"Failed {title} - response {requestObj.status_code}: {requestObj.json()}")
	elif requestObj.status_code == 200:
		return requestObj.json()

def process(APIKey: str, localDBFile: str, movies: list) -> list:
	"""
	Process all of the movies, requesting the API where necessary.
	"""
	returnList = []
	moviesFound = 0
	moviesNotFound = 0
	movieList = movies.values()
	for movie in movieList:
		response = callAPI(APIKey, movie.getTitle())
		movie.setAPIResponse(response)
		if (response.get('Error') == 'Movie not found!'):
			moviesNotFound += 1
		elif (response.get('Error') != 'Movie not found!'):
			writeToLocalDB(localDBFile, movie)
			moviesFound += 1
		returnList.append(movie)
	print(f"Movies Found: {moviesFound} | Movies Not Found: {moviesNotFound}")
	return returnList

def main() -> None:
	print('begin processing...')

	# set file paths
	inputFile = 'input.txt'
	localDBFile = 'localMovieDB.txt'
	outputFile = 'output.txt'

	# read in api key
	secrets = readSecrets('secrets.txt')
	APIKey = secrets.get('OMDb API Key')

	# read input & local movie DB files
	inputMovies = readInput(inputFile)

	# process records & write output
	resultList = process(APIKey, localDBFile, inputMovies)
	writeOutput(outputFile, resultList)

	print('processing complete')

if __name__ == "__main__":
	main()
