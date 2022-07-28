# StreetViewGuessing

a web-based locations guessing game using Google Street View Panoramic images

#### Video Demo:  TO <URL HERE>

#### Description

This game application place visiters to somewhere in the world, and the visiters need to figure out where they are. It is a quite fun and educational game.

The left of the webpage is a google street view image randomly selected from the Google Street View Service. The right half is some questions with options, which are about where the location of image is.

Visiters can also get a random view in a certain state.

The user account feature is supported in the project. If the visiters are logged in, their viewing history would be recorded and they could also add some certain locations into the My Favourites section.

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