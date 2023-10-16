## Table of contents
* [General information](#general-infomation)
* [Technologies](#technologies)
* [Setup](#setup)

## General information
This project is about a remote control application.
The application is designed for remote control and includes several features such as keylogger, screen capture, registry editing, etc. We emphasize on threading and communication between two computers in the same network.
	
## Technologies
Project is written in Python with:
* pillow 10.0.0
* pynput 1.7.6
* psutil 5.9.5
* pygetwindow 0.0.9 
* socket, threading and required libraries

## Setup
To run this project, you will need two computer connected to the same network. One will serve as the server, and the other one will act as the client. If necessary, you can use virtual machines for this purpose.

### Prerequisites
Make sure both machines have the necessary dependencies installed. The required libraries are listed in the `requirements.txt` file. You can install them using the following command:
```
pip install -r requirements.txt
```
### Server setup
Run
```
cd ./server
python main_server.py
````

### Client setup
Run
```
cd./client
python main_client.py
```


