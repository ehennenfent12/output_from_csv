import pandas as pd
import argparse
from datetime import datetime

# Load the CSV file
df = pd.read_csv('C:/Users/Trader/Documents/python/key_research/BI_summaries.csv')  # Change to where your summaries file is located
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')  # Adjust the format to match the date format in your CSV

# HTML color codes for headers
header_colors = {
    'Article': 'brown',
    'Article Title': 'red',
    'Date': 'blue',
    'Key Words': 'green',
    'Scraped Sentences': 'cyan',
    'Summary': 'magenta'
}

# Function to search and filter the articles
def search_and_filter(keywords=None, start_date=None, end_date=None, output_file='output.html'):
    # Filter by keyword(s)
    if keywords:
        keyword_list = keywords.split(',')
        filtered_df = df[df['Key_Words'].str.contains('|'.join(keyword_list), case=False, na=False)]
    else:
        filtered_df = df

    # Filter by date if start_date and end_date are provided
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df['Date'] >= start_date]
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        filtered_df = filtered_df[filtered_df['Date'] <= end_date]

    # Open the output file with UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as file:
        # Write the results in the specified format
        file.write("<html><body style='font-family: Arial, sans-serif;'>\n")
        for index, row in filtered_df.iterrows():
            file.write(f"<div style='color:black; margin-bottom: 20px;'>\n")
            file.write(f"<p style='margin: 0;'><span style='color:{header_colors['Article']};'><b>Article:</b></span> {index + 1}</p>\n")
            file.write(f"<p style='margin: 0;'><span style='color:{header_colors['Article Title']};'><b>Article Title:</b></span> {row['Title']}</p>\n")
            file.write(f"<p style='margin: 0;'><span style='color:{header_colors['Date']};'><b>Date:</b></span> {row['Date'].strftime('%Y-%m-%d')}</p>\n")
            file.write(f"<p style='margin: 0;'><span style='color:{header_colors['Key Words']};'><b>Key Words:</b></span> {row['Key_Words']}</p>\n")
            file.write(f"<p style='margin: 0;'><span style='color:{header_colors['Scraped Sentences']};'><b>Scraped Sentences:</b></span> {row['Summary']}</p>\n")
            file.write(f"<p style='margin: 0;'><span style='color:{header_colors['Summary']};'><b>Summary:</b></span> {row['AI Overview']}</p>\n")
            file.write("</div>\n<br><br>\n")  # Two line breaks after each article
        file.write("</body></html>")
    
    print(f"Results have been written to {output_file}")

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Search and filter articles by keyword and date range.')
parser.add_argument('--keywords', type=str, help='The keywords to search for, separated by commas', default=None)
parser.add_argument('--start_date', type=str, help='The start date (YYYY-MM-DD)', default=None)
parser.add_argument('--end_date', type=str, help='The end date (YYYY-MM-DD)', default=None)
parser.add_argument('--output_file', type=str, help='The output HTML file name', default='output.html')

args = parser.parse_args()

# Call the function with command-line arguments
search_and_filter(args.keywords, args.start_date, args.end_date, args.output_file)
