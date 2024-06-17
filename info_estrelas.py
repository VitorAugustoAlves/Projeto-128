from bs4 import BeautifulSoup
import pandas as pd

html_content = 'wikitable'
soup = BeautifulSoup(html_content, 'html.parser')

def scraped_data(soup):
    bright_star_table = soup.find("table", attrs={"class": "wikitable"})
    table_body = bright_star_table.find("tbody")
    table_rows = table_body.find_all("tr")

    for row in table_rows:
        table_cols = row.find_all('td')
        temp_list = []

        for col_data in table_cols:
            data = col_data.text.strip()
            temp_list.append(data if data else None)
        scraped_data.append(temp_list)

scraped_data(soup)
stars_data = []
for data in scraped_data:
    if len(data) == 5 and all(data):
        stars_data.append(data)

headers = ['Star_name', 'Distance', 'Mass', 'Radius', 'Luminosity']
scraped_df = pd.DataFrame(stars_data, columns=headers)

scraped_df['Radius'] = scraped_df['Radius'].astype(float) * 0.102763
scraped_df['Mass'] = scraped_df['Mass'].astype(float) * 0.0000954588
scraped_df = scraped_df.dropna()
initial_df = pd.read_csv('scraped_data.csv', index_col='id')
combined_df = pd.concat([initial_df, scraped_df], ignore_index=True)
combined_df.to_csv('combined_scraped_data.csv', index=True, index_label="id")

print(combined_df)
