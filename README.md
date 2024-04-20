# CS411 - Group Project
## About Our Team
* Matheus Alpha De Andrade Souza
* Brenton Babb
* Bruce Casillas
* Brian Choi

## Alpha milestone - 4/12
  - [x] Video demonstration of progress
        Alpha Video: https://youtu.be/G-iT29oSomQ
  - [x] Code snapshot
  - [x] Updated README for launch/build instructions

## Launch Instructions

1. Install MySQL Workbench https://dev.mysql.com/downloads/workbench/

2. Install MySQL Server https://dev.mysql.com/downloads/mysql/

3. Setup a New Connection (e.g: Hostname: "127.0.0.1", Port: 3306, username: "root", Password: \<your MySQL password\>)

4. Initialize the database by executing the query in "schema.sql"

5. Clone repository, install virtual environment and required dependencies using command:
```
git clone --branch Integration-Test git@github.com:malpha-alt/CS411.git
cd CS411/
python3 -m venv .venv  (or on windows: "py -3 -m venv .venv")
. .venv/bin/activate   (or on windows:.venv\Scripts\activate)
pip -r install requirements.txt
```

To run the application, use the command:
```
python -m flask run
```

## Required Features

The following is completed:
- [x] Requirements Analysis: requirements.md
- [x] Tech Stack Hello World
- [x] Third-party authentication via Google OAuth 2.0   
  
## Tech Stack Hello World - 3/5
  - [x] Identified Flask as primary framework.
  - [x] Successfully rendered static webpage.   
  - [x] Identified mySQL as primary DB technology.
    
Video link: https://drive.google.com/file/d/1utqkpNfVl7NAhS-4Ts8Z5VqcKZtOIyWD/view?usp=drive_link

