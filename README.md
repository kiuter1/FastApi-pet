# FastAPI-pet

## Description

FastApi-pet is a learning project showcasing the use of FastAPI for building web applications.

If you want to use the frontend for this project, you can find it in this repository: [Frontend Repository](https://github.com/kiuter1/FastApi-pet-frontend).
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/kiuter1/FastApi-pet.git
   cd FastApi-pet  
2. First of all, rename .env_example to .env and fill in your data 
3. Run docker: 
   ```bash
   docker-compose up --build -d 
3. OR create and activate a virtual environment:
   ```bash
   pip install poetry
   poetry install
4. Activate the virtual environment:
   ```bash
   poetry shell
5. Create db and tables.
   ```bash
   alembic revision --autogenerate -m 'initial' && alembic upgrade head
6. Generate JWT keys:
   Create a folder named certs in the root directory of the project.
   Place your JWT private and public keys in the certs folder.
7. Start the application:
   ```bash
   uvicorn src.main:app --reload
