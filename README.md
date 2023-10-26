# Anime API

A RESTful API to manage and retrieve information about anime series, built using Flask and MySQL.

# Feature
1. Fetch all anime data.
2. Fetch details of a specific anime by ID.
3. Search for anime by name or genre.
4. Get anime recommendations based on genre and size.
5. Update the details of a specific anime.
6. Delete an anime record.


# API Endpoints
- Fetch All Anime: GET /anime
- Fetch Anime by ID: GET /anime/<anime_id>
- Search Anime: GET /anime/search?name=<name>&genre=<genre>
- Get Recommendations: GET /recommendations?genre=<genre>&size=<size>
- Update Anime: PUT /anime/<anime_id> with request body containing anime details.
- Delete Anime: DELETE /anime/<anime_id>

# Steps
Clone the Repository:

git clone [your-repository-link]
cd [repository-name]

# Install Dependencies:

pip install Flask mysql-connector-python

# Database Setup:
Make sure you have created a database using mySQL. You can use animeCSVtoMySQL for conversion.
Update the config dictionary in anime_api.py with your MySQL credentials (username, password, database name).

# Run the API:
python anime_api.py
The server will start on http://127.0.0.1:5000/.
