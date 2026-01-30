import pandas as pd
import numpy as np
from adx_app.logic import calculate_adx

# Load Data
data = pd.read_csv('Assignment1-data.csv')
solution = pd.read_excel('Assignment1-Solution.xlsx')

# Calculate
result = calculate_adx(data)

# Compare ADX column
# Allow floating point tolerance
# Check first few calculated ADX values (index 27 onwards)
start_idx = 27
end_idx = 50

print("--- Comparison ---")
print(f"{'Index':<5} | {'Calc ADX':<15} | {'Ref ADX':<15} | {'Diff':<15}")

mismatches = 0
for i in range(start_idx, end_idx):
    calc = result.loc[i, 'ADX']
    ref = solution.loc[i, 'ADX']
    diff = abs(calc - ref)
    print(f"{i:<5} | {calc:<15.6f} | {ref:<15.6f} | {diff:<15.6f}")
    if diff > 1e-4:
        mismatches += 1

print(f"\nTotal Mismatches in viewed range: {mismatches}")

# Check +DI, -DI
print("\n--- +DI Comparison ---")
for i in range(14, 20):
    calc = result.loc[i, '+DI14']
    ref = solution.loc[i, '+DI14']
    print(f"{i:<5} | {calc:<15.6f} | {ref:<15.6f}")
