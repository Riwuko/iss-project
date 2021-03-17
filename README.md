# Inteligent Control Systems: Process Simulation Project

This project contains backend flask api with process models and frontend react app. The following processes were simulated: <br>

`Tank Filling Model` to simulate liquid flow in the tank with multiple valves <br>
`Substance Concentration Model` to simulate substance concentration in the tank with multiple valves <br>

### Steps to run app in developer mode

First you need to have a docker-compose installed. <br>
<br>
In the directory with docker-compose.yml run the following commands: <br>
`docker-compose build` to install all requirements (only first time) <br>
`docker-compose up` to run local server ("localhost:8080/" for backend, "localhost:3000/" for frontend) <br>
<b>

### Steps to install new packages
#### Back-end <br>
Add the library name to the `requirements.txt` file. Close the docker-compose if running and then build and run it again. <br>
#### Front-end <br>
In the `frontend` directory write proper instalation command inside the terminal. <br> 

### Available endpoints <br>
`/` list of available processes {GET} <br>
`/process/<process-name>` process config and simulation results for default config {GET} <br>
`/process/<process-name>` process config and simulation results for requested config {POST} <br>
