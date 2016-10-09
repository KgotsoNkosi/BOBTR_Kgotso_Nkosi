# BOBTR_Kgotso_Nkosi
Break the rules application for Business Optics.
I made use of requests and flask as recommended, as it was not speccified how to handle the database, I used sqlite3.
This README will also serve as a short instructional manual for the project.

To run:
Navigate to the same folder this README file is located.
Open Comand Prompt (because I used windows, should be fine in terminal).
Activate the virtual environment venv (venv\scrpits\activate)
set FLASK_APP=BOBTR_WebServer
set FLASK_DEBUG=1
(export not set for UBUNTU and MAC)
python -m flask initdb (if first time running)
python -m flask run
(The above steps were necessary in windows - on my machine, it may be possible on your own machine to use flask initdb and flask run)
Open a browser at localhost:5000.
Username = admin
Password = default

