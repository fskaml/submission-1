# Dicoding Collection Dashboard (Bike-sharing-dataset) ✨

This project contains a data analysis dashboard built with Streamlit. The dashboard visualizes and analyzes data stored in CSV files.

## Project Structure


submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── Pipfile
├── Pipfile.lock
├── README.md
├── requirements.txt
└── url.txt


## Prerequisites

- Python 3.7+
- pip or pipenv

## Setup

1. Clone this repository to your local machine.

2. Navigate to the project directory:

   
   cd submission
   

3. Install the required dependencies:

   If using pip:

   
   pip install -r requirements.txt
   

   If using pipenv:

   
   pipenv install
   

## Running the Dashboard

To run the Streamlit dashboard:

1. Ensure you're in the project root directory (submission/).

2. Run the following command:

   
   streamlit run dashboard/dashboard.py
   

3. The dashboard should now be running. Open your web browser and go to the URL displayed in the terminal (usually http://localhost:8501).