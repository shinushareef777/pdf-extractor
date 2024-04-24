
## Getting Started

To get started with this project, follow these steps:

### Prerequisites

- Docker: Ensure you have Docker installed on your system. You can download and install Docker from [here](https://www.docker.com/get-started).

### Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project-directory>
    ```

3. Build the Docker image:

    ```bash
    docker-compose up --build
    ```

4. Run the Docker containers:

    ```bash
    docker-compose up
    ```

## Usage

Once the Docker containers are up and running, you can access the following endpoints:

- **File Upload Endpoint**: `POST /api/upload`
  - Description: Endpoint for adding data from lookup.csv to database. This takes the file as a query params, if not given it will automatically get the file from task directory.
  - Example: `curl -X POST  http://localhost:8000/api/upload`

- **Entries List Endpoint**: `POST /api/entries`
  - Description: Endpoint for uploading mapToProducts.csv data to entry table.
  - Example: `curl http://localhost:8000/api/entries`

- **Entries List Endpoint**: `GET /api/entries`
  - Description: Endpoint for getting all the data from entry table.
  - Example: `curl http://localhost:8000/api/entries`

- **Entry Detail Endpoint**: `GET /entries/<bg>`
  - Description: Endpoint for retrieving details of a specific entry with respect to the belegnumber given as a path parameter.
  - Example: `curl http://localhost:8000/api/entries/12100024`