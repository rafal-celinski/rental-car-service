# Rental Car Service

Data Bases 2 [Bazy danych 2] project on WUT.

## Authors

- [Rafał Celiński](https://github.com/rafal-celinski)
- Mateusz Łukasiewicz
- Błażej Michalak
- Jakub Śledź
- [Przemysław Walecki](https://github.com/przemyslaw-walecki)

## Getting Started

To get the project up and running on your local machine, follow these steps:

### Prerequisites

Ensure you have Docker and Docker Compose installed on your system. You can download them from:

- Docker: [https://www.docker.com/get-started](https://www.docker.com/get-started)
- Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Running the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rafal-celinski/rental-car-service.git
   cd rental-car-service
   ```

2. **Setup environment variables:**\
Edit a '.env' file in the root directory of the project and set the environment variables

2. **Start the application:**\
Use Docker Compose to build and start the services
   ```bash
   docker-compose up -d
   ```