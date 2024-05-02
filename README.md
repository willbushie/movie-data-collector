# Movie Data Collector

Obtaining more detailed information about a large list of movies using only the movie titles, would be incredibly tedious to do by hand. This simple program attempts to automate that data gathering process using the [OMDb API](https://www.omdbapi.com/).

An API key will be necessary to make requests to the API (see [here](https://www.omdbapi.com/apikey.aspx)). 

*Note: As of writing, for free use of the OMDb API, there is a daily limit of 1000 requests. This program does not keep track of requests as it processes.*

## How To Use

The current program setup is a bit unique, and may need to be modified for minor differences of input data.

### Secret Storage

The API key and other items (such as file names) are stored in a `secrets.txt` file. Upon running the program, the secrets file is read and those variables are obtained to be used inside the program. 

Here are the required items in the secrets file (values below are examples):
```
OMDb API Key=apikeyvaluehere
Master File=Master.txt
Movie List=Movies.txt
Not Found File=Not Found.txt
Clean Output=clean.txt
```

- Movie List: This file contains the titles of the movies. *Note: For this specific implementation, row contents are setup as such: `move title,index number`*. The index number is a unique number, that is unrelated to the movie data gather. 
- Master File: This file will be used as a completed list of gathered data. It will also be used to ensure repeat requests (to already existing data) are not made. 
- Not Found File: This file will be filled with any entries of movies that were not found by their title. 
- Clean Output: This is a CSV like file containing the original title, index, release year, length (min), and rating of all movies listed in the Master file. No movies included in the Not Found File, will be included in the cleaned file. 
