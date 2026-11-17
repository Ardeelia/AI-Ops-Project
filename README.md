All the required documentation files can be found in the files folder. It contains the block diagram as well as the low level and high level documentation files
which also serve the purpose of reporting all the work that has been done and how it neatly ties in everything that has been taught in the course so far.


The code files can be found outside the folders as well as the tests in the tests folder. The important files are clean_data.py, train.py, app.py and ui.py. The 
transformed datasets are present in the data folder. Other files such as docker compose and prometheus.yml are the configuration files for allowing us to use prometheus
and docker containers. 

The final code has been dockerized as a container and pushed to dockerhub. It allows for it to be run on any machine with docker hub with this terminal command
"docker run -d -p 8501:8501 -p 8000:8000 ardeelia/ai-ops-project:latest".


A demo video of the same showing the ease of using the app and its features can be found at
"https://drive.google.com/drive/folders/1SccX9rW6o63DIcSaLy1H9gzPFcEoNj-i?usp=sharing".
