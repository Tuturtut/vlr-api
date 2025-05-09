# Run the API

## Redesign

This version aims to improve the architecture of the project using a modular structure with FastAPI.
Scraping logic is kept in `services/`, and endpoints are separated into routes and controllers.

#### _Run this command in a shell at the root of the project_

```shell
python -m uvicorn api:app --reload
```
