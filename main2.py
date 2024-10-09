import requests
from bs4 import BeautifulSoup
import json

def get_gas_prices():
    url = "https://gas.didnt.work/?country=lv&brand=&city=Ogre"  # URL to scrape
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve data")
        return
    
    soup = BeautifulSoup(response.text, "lxml")
    tbody = soup.find("tbody")  # Find the tbody

    gas_stations = []

    for row in tbody.find_all("tr"):
        # Extract the gas station name and location
        station_info = row.find("td").get_text(strip=True)
        
        # Split the info based on commas
        parts = station_info.split(',')
        station_name = parts[0].strip()  # Get the name
        location = parts[1].strip() if len(parts) > 1 else "Location not available"
        
        # Extract the last update date
        update_tag = row.find("span", class_="tag")
        update_date = update_tag.get_text(strip=True) if update_tag else "Дата недоступна"

        # Extract the fuel prices
        prices = {}
        
        # Find all price elements
        price_elements = row.find_all("td")
        
        # Assuming the order of prices corresponds to diesel, 95, 98, LPG
        if len(price_elements) > 1:
            # Check diesel price
            diesel_price = price_elements[1].get_text(strip=True)
            if diesel_price != '-':
                prices['Дизель'] = diesel_price

            # Check 95 price
            price_95 = price_elements[2].get_text(strip=True)
            if price_95 != '-':
                prices['95'] = price_95

            # Check 98 price
            price_98 = price_elements[3].get_text(strip=True)
            if price_98 != '-':
                prices['98'] = price_98

            # Check LPG price
            lpg_price = price_elements[4].get_text(strip=True)
            if lpg_price != '-':
                prices['Газ'] = lpg_price

        # Create a dictionary for the gas station and its prices
        gas_station_info = {
            'Название': station_name,
            'Дата обновления': update_date
        }

        # Only add prices that are available
        gas_station_info.update(prices)

        gas_stations.append(gas_station_info)

    # Save the results as JSON to a file
    with open('gas_prices.json', 'w', encoding='utf-8') as f:
        json.dump(gas_stations, f, ensure_ascii=False, indent=4)

    print("Gas prices saved to 'gas_prices.json'")

if __name__ == "__main__":
    get_gas_prices()
