# Pokémon Battle Simulator

## Description
This project is a Pokémon Battle Simulator developed using Flask. It allows users to list Pokémon, start battles between them, and retrieve battle results.

## Repository
You can find the source code for this project at: [Your Repository URL](https://github.com/yourusername/your-repository)

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

## install packages
Install required packages:
psycopg2
flask
pandas
threading
uuid
pydantic
typing
#Command to install
pip3 install packageName


##Run application
python3 BuildApi.py

##Testing the Application
1- Open a new terminal and make a request to list Pokémon:
curl http://127.0.0.1:5000/pokemon

2- Open another terminal to start a battle with a POST request:
curl -X POST http://127.0.0.1:5000/battle -H "Content-Type: application/json" -d '{"pokemon_a": "Gloom", "pokemon_b": "Vileplume"}'

3- Retrieve the battle result using the battleId:
curl http://127.0.0.1:5000/battle/battleId
