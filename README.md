# Data Analysis — Interactive Dashboard with Dash

This project demonstrates the development of an interactive data dashboard built with Python, Plotly, and Dash. The goal is to transform raw CSV files into clear and navigable visualizations, similar to BI tools such as Power BI, while keeping full control over the code and data pipeline.

## Objective
To explore tabular data, apply basic preprocessing, and present key metrics and visual insights through a web-based interactive dashboard that supports analysis and decision-making.

## Project Structure
- `src/dashboard/app.py`: main Dash application
- `src/data/load_data.py`: data loading logic
- `src/data/cleaning.py`: basic data cleaning and standardization
- `data/raw/`: original CSV files
- `data/processed/`: cleaned data used by the dashboard
- `reports/screenshots/`: examples of generated visualizations

## Technologies Used
- Python
- Dash / Plotly
- Pandas

## Running Locally

1. Create and activate a virtual environment:
```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate



