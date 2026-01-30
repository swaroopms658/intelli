import base64
import io
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .logic import calculate_adx

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            try:
                # Read CSV
                df = pd.read_csv(csv_file)
                
                # Check columns
                required = ['High', 'Low', 'Close']
                if not all(col in df.columns for col in required):
                    # Try title case normalization if needed, or error
                    # Checking case-insensitive match
                    df.columns = [c.strip() for c in df.columns] 
                    # If still missing, maybe different case? For this assignment, match exact or loose.
                    # User file has "Open", "High", "Low", "Close".
                    pass

                # Calculate
                result_df = calculate_adx(df)
                
                # Store in session for download (convert to JSON-serializable dict)
                # storing as JSON string is often safer
                request.session['adx_data'] = result_df.to_json(date_format='iso', orient='split')
                
                # Generate Plot
                plt.figure(figsize=(10, 6))
                
                # X-axis: Use 'Unnamed: 0' or Date if exists, else index
                x_axis = result_df.index
                if 'Unnamed: 0' in result_df.columns:
                     # Attempt to parse date for better label
                     try:
                         dates = pd.to_datetime(result_df['Unnamed: 0'])
                         x_axis = dates
                     except:
                         pass
                elif 'Date' in result_df.columns:
                     x_axis = pd.to_datetime(result_df['Date'])

                plt.plot(x_axis, result_df['ADX'], label='ADX', color='black', linewidth=2)
                plt.plot(x_axis, result_df['+DI14'], label='+DI', color='green', linewidth=1)
                plt.plot(x_axis, result_df['-DI14'], label='-DI', color='red', linewidth=1)
                
                plt.title('ADX (14) Indicator')
                plt.xlabel('Date / Period')
                plt.ylabel('Value')
                plt.legend()
                plt.grid(True)
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                plt.close()
                buf.seek(0)
                image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                
                context = {
                    'chart': image_base64,
                    'form': form 
                }
                return render(request, 'adx_app/results.html', context)
                
            except Exception as e:
                form.add_error(None, f"Error searching/processing file: {str(e)}")
    else:
        form = UploadFileForm()
        
    return render(request, 'adx_app/index.html', {'form': form})

def download(request):
    data = request.session.get('adx_data')
    if not data:
        return redirect('index')
        
    df = pd.read_json(data, orient='split')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="adx_solution.csv"'
    
    df.to_csv(path_or_buf=response, index=False)
    return response
