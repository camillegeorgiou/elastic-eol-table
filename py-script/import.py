import requests
from bs4 import BeautifulSoup
import csv
import json

url = "https://www.elastic.co/support/eol"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    target_table = soup.find('table', class_='table-responsive table-left-text')

    if target_table:
        rows = target_table.find_all('tr')

        table_data = []

        for row in rows:
            if row.th and 'colspan' in row.th.attrs and row.th['colspan'] == '3':
                continue

            columns = row.find_all(['td', 'th'])
            row_data = [col.get_text(strip=True) for col in columns]

            table_data.append(row_data)

        csv_file = 'csv_eol.csv'
        json_file = 'json_eol.json'

        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(table_data)

        print(f"EOL data saved to {csv_file}")

        with open(json_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(table_data, jsonfile, ensure_ascii=False, indent=2)

        print(f"EOL data saved to {json_file}")
    else:
        print("Table not found")
else:
    print(f"Failed to process. Status code: {response.status_code}")
