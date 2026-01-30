import pandas as pd
import numpy as np

# Load data
df = pd.read_excel('Assignment1-Solution.xlsx')

# Inspect values around row 13-16
print("--- Rows 12 to 16 ---")
print(df.loc[12:16, ['TR', 'TR14', '+DM 1', '+DM14', 'DX', 'ADX']])

# Inspect values where ADX starts
# Find first non-null ADX
first_adx_idx = df['ADX'].first_valid_index()
print(f"\nFirst ADX Index: {first_adx_idx}")
if first_adx_idx is not None:
    print(df.loc[first_adx_idx-2:first_adx_idx+2, ['DX', 'ADX']])

# Check Smoothing Logic for TR14 at index 14 (assuming it's the first one)
# Standard Wilder: First = Sum(TR[1:15])? Or Sum(TR[0:14])?
# Let's check Sum(TR[1:15]) vs TR14[14]
tr_slice = df.loc[1:14, 'TR']
print(f"\nSum TR[1:14]: {tr_slice.sum()}") 
# (Note: DataFrame index 1 is usually the second row if header is row 0)

# Check Wilder's Smoothing for next row
# TR14[i] = (TR14[i-1] * 13 + TR[i]) / 14
idx = 15
prev_tr14 = df.loc[idx-1, 'TR14']
curr_tr = df.loc[idx, 'TR']
calc_tr14 = (prev_tr14 * 13 + curr_tr) / 14
actual_tr14 = df.loc[idx, 'TR14']
print(f"\nCheck Smoothing at idx={idx}:")
print(f"Prev TR14: {prev_tr14}, Curr TR: {curr_tr}")
print(f"Calc: {calc_tr14}, Actual: {actual_tr14}")
print(f"Match? {np.isclose(calc_tr14, actual_tr14)}")

# Check ADX Smoothing
# ADX[i] = (ADX[i-1] * 13 + DX[i]) / 14
if first_adx_idx:
    idx = first_adx_idx + 1
    prev_adx = df.loc[idx-1, 'ADX']
    curr_dx = df.loc[idx, 'DX']
    calc_adx = (prev_adx * 13 + curr_dx) / 14
    actual_adx = df.loc[idx, 'ADX']
    print(f"\nCheck ADX Smoothing at idx={idx}:")
    print(f"Prev ADX: {prev_adx}, Curr DX: {curr_dx}")
    print(f"Calc: {calc_adx}, Actual: {actual_adx}")
    print(f"Match? {np.isclose(calc_adx, actual_adx)}")

    # Check First ADX Calculation
    # Is it Average of first 14 DX?
    # DX starts at... check start of DX
    first_dx_idx = df['DX'].first_valid_index()
    print(f"First DX Index: {first_dx_idx}")
    dx_slice = df.loc[first_dx_idx : first_adx_idx-1, 'DX'] # usually 14 values?
    print(f"Mean of DX slice size {len(dx_slice)}: {dx_slice.mean()}")
    print(f"Actual First ADX: {df.loc[first_adx_idx, 'ADX']}")
