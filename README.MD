# Hire A Musician
Hire A Musician is an app targeting for self-managing session musicians, who are looking for a job or other fellow 
musician for the job. It features a simple chat and star rating system.

## Tech Stack
- Django
- Bootstrap
- PostgreSQL
- Docker

## Requirements
Hire A Musician requires the following to run:
- Python 3.10 or newer
- latest version of Docker
- latest version of docker-compose

## How to run?

1. Clone this GitHub repository (use one of the following commands, depending on what method you use)  
**HTTPS:**  
`git clone https://github.com/maciejpiszczek/hire-musician.git`  
**SSH:**  
`git clone git@github.com:maciejpiszczek/hire-musician.git`
2. Go to the project directory:  
`cd donate-stuff`
3. Provide .env file with necessary environmental variables (see env/.env-default for reference).
4. Start the server:  
`docker compose up --build`

## Usage

A logged-in user can add and browse job offers, of which there are three types - concert, tour and studio session.
One can also apply for available offers, rate fellow musicians and send messages to them (simple asynchronous chat included).
