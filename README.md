# CS411 - Final Web App: Concert Chronicles
## About Our Team
* Matheus Alpha De Andrade Souza
* Brenton Babb
* Bruce Casillas
* Brian Choi

## Final Video Walkthrough:

## Launch Instructions

1. Install MySQL Workbench https://dev.mysql.com/downloads/workbench/

2. Install MySQL Server https://dev.mysql.com/downloads/mysql/

3. Setup a New Connection (e.g: Hostname: "127.0.0.1", Port: 3306, username: "root", Password: \<your MySQL password\>)

4. Initialize the database by executing the query in "schema.sql"

5. Clone repository, install virtual environment and required dependencies using command:
```
git clone git@github.com:malpha-alt/CS411.git
cd CS411/
python3 -m venv .venv  (windows: "py -3 -m venv .venv")
. .venv/bin/activate   (windows: "source .venv/Scripts/activate")
pip install --upgrade pip (windows: "py -m pip install --upgrade pip")
pip install -r "requirements.txt"
```
6. place .env file in directory

To run the application, use the command:
```
python -m flask run
```

## Required Features
Our project satisfies the following key requirements:
- [x] Two correlated API calls<br>
    -[Setlist FM](https://api.setlist.fm/docs/1.0/index.html) <br>
    -[Google Maps](https://developers.google.com/maps/documentation/javascript)

- [x] Database<br>
      -MySql 
- [x] OAuth authentication<br>
      -[Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
- [x] De-coupled Front end / Back end<br>
      - Frontend: HTML, CSS, JavaScript with jQuery+Ajax<br>
      - Backend: Flask

The following deliverables are completed:
- [x] Requirements Analysis: "requirements.md" - 2/27
- [x] Tech Stack Hello World -3/5
- [x] Alpha Milestone - 4/12


## Alpha milestone - 4/12
  - [x] Video demonstration of progress<br>
        Alpha Video Link: https://youtu.be/G-iT29oSomQ
  - [x] Code snapshot
  - [x] Updated README for launch/build instructions
  
## Tech Stack Hello World - 3/5
  - [x] Identified Flask as primary framework.
  - [x] Successfully rendered static webpage.   
  - [x] Identified mySQL as primary DB technology.
    
Video link: https://drive.google.com/file/d/1utqkpNfVl7NAhS-4Ts8Z5VqcKZtOIyWD/view?usp=drive_link

