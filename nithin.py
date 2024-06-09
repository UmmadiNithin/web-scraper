import requests
from bs4 import BeautifulSoup
import csv
import os
import datetime

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue"
try:
    # Send a GET request to the page
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successfull

    # Get the current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content,'html.parser')


    # Find the table containing the data
    table = soup.find('table', {'class': 'wikitable'})


    if table is None:
        raise ValueError("Table not found on the page")

    # Extract the headers
    headers = [header.text.strip() for header in table.find_all('th')]
    headers = headers[0:11]

    if not headers:
        raise ValueError("No headers found in the table")

    # Extract the rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all(['td', 'th'])
        cells = [cell.text.strip() for cell in cells]
        if cells:  # Ensure the row is not empty
            rows.append(cells)


    if not rows:
        raise ValueError("No rows found in the table")

    # Save to CSV file
    format = '%Y-%m-%d %H:%M:%S'
    filename = f'largest_companies_by_revenue_{timestamp}.csv'
    if os.path.exists(filename):
        os.remove(filename)  # Remove the file if it already exists

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)  # Write headers
        csvwriter.writerows(rows)  # Write data rows

    print(f"Data has been saved to {filename}")

except requests.RequestException as e:
    print(f"Network error: {e}")
except ValueError as e:
    print(f"Parsing error: {e}")
except PermissionError as e:
    print(f"Permission error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")



