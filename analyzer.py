import pandas as pd
import os
import time

def process_data(file_path, context, output_folder):
    """
    This function processes a single uploaded file and returns analysis results.
    USER: You can modify this file to implement your specific financial logic.
    """
    
    # Simulate processing time
    time.sleep(1.5)
    
    # Check file extension to read correctly
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    else:
        # Fallback for text files or others - just make a dummy dataframe
        df = pd.DataFrame({'Data': ['Item 1', 'Item 2'], 'Value': [100, 200]})

    # ---------------------------------------------------------
    # YOUR ANALYSIS LOGIC HERE
    # ---------------------------------------------------------
    # Example: Calculate a simple mean of the numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    
    analysis_summary = {
        'total_rows': len(df),
        'numeric_columns': len(numeric_df.columns),
        'avg_values': numeric_df.mean().to_dict() if not numeric_df.empty else {}
    }

    # Generate Output Excel
    output_filename = f"Analysis_Report_{int(time.time())}.xlsx"
    output_path = os.path.join(output_folder, output_filename)
    
    # Create an extensive report with multiple sheets
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name='Original Data', index=False)
        
        # Create a summary sheet
        summary_df = pd.DataFrame([analysis_summary])
        summary_df.to_excel(writer, sheet_name='Summary Metrics', index=False)
        
        # Maybe add a "calculated" sheet
        if not numeric_df.empty:
             (numeric_df * 1.1).to_excel(writer, sheet_name='Projected Growth', index=False)

    # Prepare data for the frontend table
    # We'll just take the first 5 rows of the original data to show as a preview
    preview_data = df.head(5).fillna('').to_dict(orient='records')
    headers = df.columns.tolist()

    return {
        'status': 'success',
        'metrics': {
            'savings': '$85,200', # You can calculate this dynamically
            'roi': '12.5%',
            'risk': 'Low',
            'breakeven': '14 Months'
        },
        'recommendation': {
            'type': 'approved', # or 'review'
            'text': f"Based on the analysis of {len(df)} records, we recommend proceeding. (Context: {context[:30]}...)"
        },
        'table_data': {
            'headers': headers,
            'rows': preview_data
        },
        'download_url': f"/download/{output_filename}"
    }


def process_multiple_files(files_info, context, output_folder):
    """
    Process multiple uploaded files and return combined analysis results.
    
    Args:
        files_info: List of dicts with 'filename', 'filepath', 'original_name'
        context: User-provided scenario context
        output_folder: Folder to save output files
    
    Returns:
        dict with analysis results, table data, and download URL
    """
    
    # Simulate processing time
    time.sleep(1.0)
    
    all_dataframes = []
    file_summaries = []
    
    # Process each file
    for file_info in files_info:
        filepath = file_info['filepath']
        filename = file_info['original_name']
        
        try:
            # Read file based on extension
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
                df = pd.read_excel(filepath)
            else:
                # Skip unsupported files (like PDF - you can add PDF parsing later)
                continue
            
            all_dataframes.append({
                'name': filename,
                'data': df
            })
            
            # Calculate file summary
            numeric_df = df.select_dtypes(include=['number'])
            file_summaries.append({
                'file': filename,
                'rows': len(df),
                'columns': len(df.columns),
                'numeric_columns': len(numeric_df.columns)
            })
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    if not all_dataframes:
        raise ValueError("No valid data files could be processed")
    
    # ---------------------------------------------------------
    # YOUR CUSTOM ANALYSIS LOGIC HERE
    # Combine and analyze all dataframes as needed
    # ---------------------------------------------------------
    
    # For demo: combine all dataframes (if they have same columns) or use first one
    combined_df = all_dataframes[0]['data']
    
    # Try to combine dataframes with same columns
    for df_info in all_dataframes[1:]:
        if set(df_info['data'].columns) == set(combined_df.columns):
            combined_df = pd.concat([combined_df, df_info['data']], ignore_index=True)
    
    # Calculate overall metrics
    total_rows = sum(s['rows'] for s in file_summaries)
    numeric_df = combined_df.select_dtypes(include=['number'])
    
    # Calculate dynamic metrics (customize these based on your needs)
    if not numeric_df.empty:
        total_sum = numeric_df.sum().sum()
        avg_value = numeric_df.mean().mean()
        savings_estimate = f"${total_sum * 0.12:,.0f}" if total_sum > 0 else "$0"
        roi_estimate = f"{(avg_value / 100 * 12.5):.1f}%" if avg_value > 0 else "N/A"
    else:
        savings_estimate = "$0"
        roi_estimate = "N/A"
    
    # Generate Output Excel with all data
    output_filename = f"Analysis_Report_{int(time.time())}.xlsx"
    output_path = os.path.join(output_folder, output_filename)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary sheet
        summary_df = pd.DataFrame(file_summaries)
        summary_df.to_excel(writer, sheet_name='Files Summary', index=False)
        
        # Combined data sheet
        combined_df.to_excel(writer, sheet_name='Combined Data', index=False)
        
        # Individual file sheets
        for df_info in all_dataframes:
            sheet_name = df_info['name'][:31]  # Excel sheet name limit
            sheet_name = sheet_name.replace('/', '-').replace('\\', '-')
            df_info['data'].to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Analysis results sheet
        if not numeric_df.empty:
            analysis_df = pd.DataFrame({
                'Metric': ['Total Rows', 'Total Columns', 'Sum', 'Average', 'Min', 'Max'],
                'Value': [
                    total_rows,
                    len(combined_df.columns),
                    numeric_df.sum().sum(),
                    numeric_df.mean().mean(),
                    numeric_df.min().min(),
                    numeric_df.max().max()
                ]
            })
            analysis_df.to_excel(writer, sheet_name='Analysis Results', index=False)
    
    # Prepare table data for frontend display
    # Show preview of combined data (first 10 rows)
    preview_df = combined_df.head(10).fillna('')
    
    # Convert all values to strings to avoid JSON serialization issues
    preview_data = []
    for _, row in preview_df.iterrows():
        row_dict = {}
        for col in preview_df.columns:
            value = row[col]
            if pd.isna(value):
                row_dict[col] = ''
            else:
                row_dict[col] = str(value)
        preview_data.append(row_dict)
    
    headers = combined_df.columns.tolist()
    
    # Determine recommendation based on analysis
    risk_level = 'Low' if total_rows < 1000 else ('Medium' if total_rows < 10000 else 'High')
    recommendation_type = 'approved' if risk_level == 'Low' else 'review'
    
    return {
        'status': 'success',
        'files_processed': len(all_dataframes),
        'metrics': {
            'savings': savings_estimate,
            'roi': roi_estimate,
            'risk': risk_level,
            'breakeven': '14 Months'
        },
        'recommendation': {
            'type': recommendation_type,
            'text': f"Analyzed {len(files_info)} file(s) with {total_rows} total records. {context[:50]}..." if context else f"Analyzed {len(files_info)} file(s) with {total_rows} total records."
        },
        'table_data': {
            'headers': headers,
            'rows': preview_data,
            'total_rows': total_rows
        },
        'file_summaries': file_summaries,
        'download_url': f"/download/{output_filename}"
    }
