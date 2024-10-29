import os
import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape data and save it into the specified folder
# Function to scrape data and save it into the specified folder
def scrape_nfl_stats(stat_type, year, every_year):
    if every_year:
        for year in range(int(FIRST_YEAR), int(CURRENT_YEAR) + 1):
            scrape_single_year(stat_type, year)
    else:
        scrape_single_year(stat_type, year)

def scrape_single_year(stat_type, year):
    # Create folder if it doesn't exist
    if not os.path.exists(stat_type):
        os.makedirs(stat_type)

    # Set the URL based on the stat type and year
    url = f'https://www.pro-football-reference.com/years/{year}/{stat_type}.htm'

    # Send a GET request
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing stats
        #table = soup.find('table', {'id': stat_type})
        table = soup.find('div', {'id': True, 'class': 'table_wrapper'})  # Find div with class 'table_wrapper'
        if table is None:
            print(f"Table for '{stat_type}' not found for the year {year}. Please check the stat type and year.")
            return


        if stat_type in ('scrimmage', 'defense', 'defense_advanced', 'kicking', 'punting', 'returns'):
            # Extract table headers and skip the first row of th
            table_rows = table.find_all('tr')
            if len(table_rows) > 1:  # Ensure there are enough rows to skip
                headers = [th.text.strip() for th in table_rows[1].find_all('th')]  # Extract from the second row of th
            else:
                headers = []
        else:
            # Extract table headers
            headers = [th.text for th in table.find_all('th')] 

        # Extract rows
        rows = []
        if stat_type in ('scrimmage', 'defense', 'defense_advanced', 'kicking', 'punting', 'returns'):
            for row in table.find_all('tr')[2:]:  # Skip first row (headers)
                cells = [cell.text for cell in row.find_all(['th', 'td'])]
                rows.append(cells)
        else:
            for row in table.find_all('tr')[1:]:  # Skip first row (headers)
                cells = [cell.text for cell in row.find_all(['th', 'td'])]
                rows.append(cells)
        # Save to CSV in the appropriate folder
        with open(f'{stat_type}/{stat_type}_{year}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"Data has been saved to {stat_type}/{stat_type}_{year}.csv")
    else:
        print("Failed to retrieve the page")

# Main script execution
TYPE_OPTIONS = ['passing', 'passing_advanced', 'rushing', 'rushing_advanced', 
                'receiving', 'receiving_advanced', 'scrimmage', 'defense', 
                'defense_advanced', 'kicking', 'punting', 'returns']

FIRST_YEAR = '1932'
CURRENT_YEAR = '2024'    

# Display options with numbers
print("Choose a stat type from the following options:")
for i, option in enumerate(TYPE_OPTIONS, start=1):
    print(f"{i}. {option}")

# User input for stat type
try:
    choice = int(input("Enter the number corresponding to your choice:\n").strip())
    if 1 <= choice <= len(TYPE_OPTIONS):
        stat_type = TYPE_OPTIONS[choice - 1]
    else:
        print("Invalid selection.")
        exit()
except ValueError:
    print("Please enter a valid number.")
    exit()

# User input for every year or a specific year
every_year = input("Do you want to scrape data for every year from 1932 to 2024? (yes/no)\n").strip().lower() == 'yes'

if every_year:
    scrape_nfl_stats(stat_type, None, every_year)
else:
    year = input(f"Enter a specific year between {FIRST_YEAR} and {CURRENT_YEAR}:\n").strip()
    if FIRST_YEAR <= year <= CURRENT_YEAR:
        scrape_nfl_stats(stat_type, year, every_year)
    else:
        print("Invalid year entered.")
