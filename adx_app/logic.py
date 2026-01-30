import pandas as pd
import numpy as np

def calculate_adx(df):
    """
    Calculate ADX, +DI, -DI matching the reference Excel logic.
    Assumes df has columns: 'High', 'Low', 'Close'.
    
    Logic inferred from specific Excel file:
    1. TR, +DM1, -DM1 calculated for all rows (start index 1).
    2. TR14, +DM14, -DM14 (Smoothed Sums):
       - First value (at index 14): Sum of first 14 values (indices 1 to 14).
       - Subsequent: Prev_Sum - (Prev_Sum / 14) + Current_Val.
    3. +DI14, -DI14:
       - +DI14 = 100 * (+DM14 / TR14)
       - -DI14 = 100 * (-DM14 / TR14)
    4. DX:
       - 100 * abs(+DI14 - -DI14) / (+DI14 + -DI14)
    5. ADX (Smoothed Average):
       - First value (at index 27): Mean of DX values from index 14 to 27 (14 values).
       - Subsequent: (Prev_ADX * 13 + Current_DX) / 14.
    """
    
    # Ensure columns exist and numeric
    high = df['High'].astype(float)
    low = df['Low'].astype(float)
    close = df['Close'].astype(float)
    
    # Initialize implementation columns with NaNs
    n = len(df)
    tr = np.zeros(n)
    dm_plus = np.zeros(n)
    dm_minus = np.zeros(n)
    
    # 1. TR, +DM, -DM (row by row, starting at 1)
    # TR matches Excel: max(H-L, |H-Cp|, |L-Cp|)
    # +DM: H-Hp if H-Hp > Lp-L and > 0
    # -DM: Lp-L if Lp-L > H-Hp and > 0
    
    # We can use vectorization for speed for step 1
    # Shifted values
    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)
    
    # TR Vectorized
    tr_1 = high - low
    tr_2 = (high - prev_close).abs()
    tr_3 = (low - prev_close).abs()
    tr_series = pd.DataFrame({'a': tr_1, 'b': tr_2, 'c': tr_3}).max(axis=1)
    # Ensure index 0 is 0 or NaN as per Excel (Excel usually blank, we can leave nan)
    # But for calculation of Sum, we strictly use indices 1..14.
    
    # DM Vectorized
    up_move = high - prev_high
    down_move = prev_low - low
    
    plus_dm_series = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm_series = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    
    # Force first row used for diffs to NaN to match Excel (which usually starts calc at row 2)
    # Excel Index 0 is just raw data, Index 1 has first TR? 
    # Wait, check verification again. Excel Row 2 (Index 0) TR is NaN.
    # Excel Row 3 (Index 1) TR is valid.
    tr_series.iloc[0] = np.nan
    plus_dm_series[0] = np.nan
    minus_dm_series[0] = np.nan
    
    # Convert to standard lists/arrays for iterative smoothing (Wilder's is recursive)
    # Or implement recursive loop carefully. 
    # Since we need exact match, loop is safer for the "Prev" dependence.
    
    tr14 = np.full(n, np.nan)
    plus_dm14 = np.full(n, np.nan)
    minus_dm14 = np.full(n, np.nan)
    
    # Initialization at index 14 (15th row, if 0-based index)
    # Sum of indices 1 to 14 (inclusive)
    # Note: df is 0-indexed. 
    # Excel Index 14 (row 15) uses Sum(Row 1..14).
    # Pandas Index 1..14 (14 values).
    
    # Check if we have enough data
    if n < 15:
        return df # logic fail if too short
        
    initial_slice = slice(1, 15) # 1 to 14 inclusive
    
    tr14[14] = tr_series[initial_slice].sum()
    plus_dm14[14] = plus_dm_series[initial_slice].sum()
    minus_dm14[14] = minus_dm_series[initial_slice].sum()
    
    # Smoothing Loop starting from 15
    for i in range(15, n):
        # Smoothed Sum: Prev - (Prev/14) + Curr
        # TR
        prev = tr14[i-1]
        curr = tr_series[i]
        tr14[i] = prev - (prev/14.0) + curr
        
        # +DM
        prev = plus_dm14[i-1]
        curr = plus_dm_series[i]
        plus_dm14[i] = prev - (prev/14.0) + curr
        
        # -DM
        prev = minus_dm14[i-1]
        curr = minus_dm_series[i]
        minus_dm14[i] = prev - (prev/14.0) + curr
        
    # Calculate DI and DX
    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        plus_di14 = 100 * (plus_dm14 / tr14)
        minus_di14 = 100 * (minus_dm14 / tr14)
        
        di_sum = plus_di14 + minus_di14
        di_diff = np.abs(plus_di14 - minus_di14)
        dx = 100 * (di_diff / di_sum)
        
    # ADX Logic
    adx = np.full(n, np.nan)
    
    # Initialization at index 27
    # Mean of DX from index 14 to 27 (14 values)
    # Range 14..27 inclusive is 14 values.
    # Pandas slice 14:28 (end exclusive)
    if n > 27:
        adx[27] = np.mean(dx[14:28])
        
        # Smoothing Loop starting from 28
        for i in range(28, n):
            # Smoothed Average: (Prev * 13 + Curr) / 14
            prev = adx[i-1]
            curr = dx[i]
            adx[i] = (prev * 13 + curr) / 14.0
            
    # Create result DataFrame
    # Preserve original indices and structure
    result = df.copy()
    result['TR'] = tr_series
    result['+DM 1'] = plus_dm_series
    result['-DM 1'] = minus_dm_series
    result['TR14'] = tr14
    result['+DM14'] = plus_dm14
    result['-DM14'] = minus_dm14
    result['+DI14'] = plus_di14
    result['-DI14'] = minus_di14
    result['DX'] = dx
    result['ADX'] = adx
    
    return result
