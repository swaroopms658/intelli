# ADX Indicator Analyzer

A Django web application to calculate and visualize the ADX (Average Directional Index) from stock data CSVs, matching standard Wilder's Logic.

## Features
- **Upload**: CSV files with Open, High, Low, Close.
- **Calculate**: Computes TR, DM, Smoothed TR/DM, DI, DX, and ADX.
- **Visualize**: Interactive ADX, +DI, -DI chart.
- **Export**: Download the full calculation results as CSV.

## Requirements
- Python 3.6+
- Django 3.x
- Pandas, Numpy, Matplotlib

## Setup & Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python manage.py runserver
   ```

3. Open browser at `http://127.0.0.1:8000/`.

4. Upload the provided `assignment1-data.csv`.

## Verification
- To check logic against the provided `assignment1-Solution.xlsx`:
  ```bash
  python verify_logic.py
  ```
  (Requires `openpyxl` installed: `pip install openpyxl`).

## Logic Details
- **TR/DM**: Standard definitions.
- **Smoothing (TR/DM)**: Wilder's Smoothed Sum (Initialized with Sum of first 14).
- **ADX**: Smoothed Average (Initialized with Mean of first 14 DX).
