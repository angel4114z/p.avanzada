# Technical report

# TODO 1:
-technical report with:
    -update user stories: (check)
    
- As a administrator, I want to be able to create new vehicles, so that I can add them to the catalog.
- As a administrator, I want to be able to create new engines, so that I can associate them with vehicles.
- As a user, I want to be able to view the catalog of vehicles, so that I can see the available options.
- As a user, I want to be able to view the catalog of engines, so that I can see the available options.
- As a user, I want to be able to view the details of a vehicle, so that I can make an informed decision.
- As a user, I want to be able to view the details of an engine, so that I can understand its capabilities.


# Communication Data Structures

## Add a Vehicle

Request:
{
  "type": "string",
  "engine": "string",
  "chassis": "string",
  "model": "string",
  "year_of_manufacture": "string",
  "fuel_consumption": "string"
}

Response:
{
  "message": "string"
}

## View All Vehicles

Response:
{
  "vehicles": [
    {
      "type": "string",
      "engine": "string",
      "chassis": "string",
      "model": "string",
      "year_of_manufacture": "string",
      "fuel_consumption": "string"
    },
    ...
  ]
}

## Add an Engine

Request:
{
  "type": "string",
  "potency": "string",
  "weight": "string"
}

Response:
{
  "message": "string"
}

## View All Engines

Response:
{
  "engines": [


    {
      "type": "string",
      "potency": "string",
      "weight": "string"
    },
    ...
  ]
}



-Design the web services req from front to back at form:(check)
    HTTP meyhod, URL request, Expected response, Name

        - Add a new engine:
            - HTTP method: POST
            - URL request: /api/engines
            - Expected response: 200 OK if successful, 400 Bad Request if there are validation errors
        - Add a new vehicle:
            - HTTP method: POST
            - URL request: /api/vehicles
            - Expected response: 200 OK if successful, 400 Bad Request if there are validation errors
        - Get all engines:
            - HTTP method: GET
            - URL request: /api/engines
            - Expected response: 200 OK with a list of engines
        - Get all vehicles:
            - HTTP method: GET
            - URL request: /api/vehicles
            - Expected response: 200 OK with a list of vehicles
