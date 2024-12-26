# Allowance Payment Discrepancy Finder

This project is a Data Engineering challenge focused on identifying discrepancies in Allowance Payment Days. It processes allowance data, payment schedules, and event information to pinpoint instances where payments might not align with expected timelines.

## Project Structure

The project is organized as follows:

├── assets/                 # Static assets (if any)
├── backup/                 # Backup data (if applicable)
├── data/
│   ├── input/             # Input data files
│   │   ├── allowance_backend_table.csv    # Allowance data
│   │   ├── allowance_events.json        # Allowance event data
│   │   └── payment_schedule_backend_table.csv # Payment schedule data
│   └── output/            # Output data and results
├── notebooks/             # Jupyter notebooks for exploration (if any)
├── results/              # Final results and reports
├── src/
│   ├── helpers/           # Helper functions and modules
│   │   ├── 00_data_download.py # Script for downloading or generating data
│   │   ├── 01_data_analysis.py # Main analysis script
│   │   └── 02_data_results.py # Script for generating results and reports
├── .DS_Store              # macOS metadata file (can be ignored)
├── Dockerfile              # Docker configuration for containerization
├── README.md               # This README file
├── app.py                  # Main application entry point (if applicable)
└── requirements.txt        # Python dependencies

## Data Files

*   `data/input/allowance_backend_table.csv`: Contains detailed information about allowances, including allowance IDs, amounts, and other relevant details. This files automatically downloads when yoy run the app.
*   `data/input/allowance_events.json`: Stores event data related to allowances, such as creation, modification, or cancellation events, along with timestamps. It also downdloads automatically.
*   `data/input/payment_schedule_backend_table.csv`: Provides the planned payment schedule for allowances, including expected payment dates. It also downdloads automatically.

## Scripts

*   `src/helpers/00_data_download.py`: This script is responsible for obtaining the necessary data. It downloads data from external sources (Github Gist).
*   `src/helpers/01_data_analysis.py`: This is the core script that performs the analysis to detect discrepancies in allowance payment days. It reads the input data, processes it, and identifies instances that are suspicious.
*   `src/helpers/02_data_results.py`: This script takes the output of the analysis script and generates a PDF which shows the result, hypotheses and possible ideas to solve this issue.

## Modifications

Trying to discover the discrepancies in the Next Payments Days I added a new column to the event's JSON adding the day of the allowance payment, to do so, I calculated based on the timestamp, the frequency and day, what was the number of the next payment day, and compared it to the one that appears on the backend data.

## Dockerization (not mandatory)

This project includes a `Dockerfile` for containerization using Docker. This allows for consistent and reproducible execution of the project across different environments.

### Docker Requirements

*   Docker Engine must be installed on your system. You can download it from the official Docker website: [https://www.docker.com/get-docker](https://www.docker.com/get-docker)

### Running the app with Docker

First you should clone this repo!

Then, to build the Docker image, navigate to the project root directory in your terminal and run the following command:

```bash
docker build -t allowance-analysis .
```

This command builds an image named allowance-analysis.

### Running the Docker Container
To run the Docker container, use the following command:

```
docker run -v $(pwd)/data:/app/data allowance-analysis
```

This command mounts the data directory from your local machine to the /app/data directory inside the container. This allows the container to access the input data and write the output data to your local machine. This is important to ensure data persistence, otherwise data generated inside the docker container will be lost after the container stops running.

## Local Setup (Without Docker)

### Python Requirements
The project uses Python and requires the following packages, listed in requirements.txt:
* pandas
* json
* requests
* fpdf
* matplotlib

You can install these dependencies using pip:

```
pip install -r requirements.txt
```

If you prefer to run the project locally without Docker, follow these steps:

1. Clone the repository.
2. Install Python 3.9 or higher.
3. Install the required Python packages: pip install -r requirements.txt
4. Navigate to the src/helpers directory.
5. Run the desired script: python 01_data_analysis.py

## Results 
The output and results will be available in the result folder.
