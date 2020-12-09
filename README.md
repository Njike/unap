# unap
# Requirements
Python
    min python version python3.6.x 
Pip
    version pip3

# Installation
Run pip3 install -r requirements.txt

# Configuration
    rename the config.example.py to config.py
        configure the config.py file with your desirable configuration


# Running
To run the app, 
        After the configuration, run python3 run.py 
    to create the database and the respective tables

    if you are on Linux:
        in your project directory, run the follwing command in your terminal:
            export FLASK_APP=run.py
            export FLASK_DEBUG=1 --if you are running in debug mode 
    if you are on Windows:
        in your project directory, run the following command in your cmd:
            set FLASK_APP=run.py
            set FLASK_DEBUG=1 --if you are running in debug mode
