# StreetViewGuessing

a web-based locations guessing game using Google Street View Panoramic images

#### Video Demo:  TO <https://youtu.be/gTKBSHZJqOg>

#### Description

This game application place visitors somewhere in the world, and the visitors need to figure out where they are. It is quite a fun and educational game.

On the left of the webpage is a google street view image randomly selected from the Google Street View Service. The first step is that get a random coordinate from API of <https://www.geonames.org/>, and then get the nearest location with street view information, using Google Street View API. There are lots of work in dealing with the APIs and coping with exceptional data since the geographic data are not too organised.

The right half is some questions with options, which are about where the location of the image is. The questions are more detailed when the visitor is moving forward. When someone gives the right answer, the page would show the "CORRECT" hint and the next question. If the visitor is right about the last question, there would be a button with the link for the next round. API of Geoname.com also processes reverse geocoding. All potential options of states and subdivisions were stored at `static/iso-3166-2.json`

Visitors can also get a random view in a certain state. The page list all available states that google street view support. It works well in most countries. However, in some tiny/Streetview lacking areas (Antarctica etc.), the resulting location may come from other places. This is a bug embedded in APIs.

The user account feature is supported in the project, which means we have `register`, `login`, `logout`, and `change password` pages. If the visitors are logged in, their viewing history would be recorded and they could also add certain locations to the My Favourites section. `Add to My Favourites` buttons could be found in the history page and the index (main) page. The data in the My Favourites pages could be edited by visitors themselves.

#### Files of this project and their function

1. `.py` file
   1. `app.py` is the main entrance of the flask framework. the file contains all the functions for each request
   2. `svProjectFunctions.py` contains the functions that have been used in the `app.py` file. These functions get random coordinates and street view data from APIs and figure out the geographical information of those places
   3. `userFunctions.py` contains the function that related to login behaviours and error messages
   4. `re.txt` is the dependency list for `pip` to establish an appropriate python virtual environment for the project
2. `database.db`
   1. the project is using a single database which is created and operated by `sqlite3`
   2. `user` table contains the user information of the web app, including usernames and hash of the passwords
   3. `favourites` table and `history` table contain the data for each user respectively
   4. more schema information of the database could be found in `schema.sql`
3. `template` directory
   1. contains all the HTML templates with jinja syntax
   2. the `layout.html` is the layout for other pages
4. `static` directory
   1. contains all the `javascript`, `.css`, and `JSON` files for scripts, styles information and static data respectively
