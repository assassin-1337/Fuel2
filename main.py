import requests
from bs4 import BeautifulSoup
import json
import telebot

# Set up the bot with your token
TOKEN = "6069114933:AAFW6whjfkU2qH09Sr7WO9De8zsSKFvxGPQ"
bot = telebot.TeleBot(TOKEN)

# Function to scrape gas prices
def get_gas_prices():
    url = "https://gas.didnt.work/?country=lv&brand=&city=Ogre"  # URL to scrape
    response = requests.get(url)

    if response.status_code != 200:
        return "Failed to retrieve data"
    
    soup = BeautifulSoup(response.text, "lxml")
    tbody = soup.find("tbody")  # Find the tbody

    gas_stations = []

    for row in tbody.find_all("tr"):
        # Extract the gas station name and location
        station_info = row.find("td").get_text(strip=True)
        parts = station_info.split(',')
        station_name = parts[0].strip()  # Get the name
        
        # Extract the last update date
        update_tag = row.find("span", class_="tag")
        update_date = update_tag.get_text(strip=True) if update_tag else "Дата недоступна"

        # Extract the fuel prices
        prices = {}
        price_elements = row.find_all("td")
        
        if len(price_elements) > 1:
            diesel_price = price_elements[1].get_text(strip=True)
            if diesel_price != '-':
                prices['Дизель'] = diesel_price

            price_95 = price_elements[2].get_text(strip=True)
            if price_95 != '-':
                prices['95'] = price_95

            price_98 = price_elements[3].get_text(strip=True)
            if price_98 != '-':
                prices['98'] = price_98

            lpg_price = price_elements[4].get_text(strip=True)
            if lpg_price != '-':
                prices['Газ'] = lpg_price

        # Create a string for the station's prices
        gas_station_info = f"Название: {station_name}\nДата обновления: {update_date}\n"
        for fuel_type, price in prices.items():
            gas_station_info += f"{fuel_type}: {price}\n"
        
        gas_stations.append(gas_station_info.strip())

    return "\n\n".join(gas_stations)

# Command handler for /check
@bot.message_handler(commands=['check'])
def handle_check(message):
    prices = get_gas_prices()
    bot.send_message(message.chat.id, prices)

# Handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.lower() == "чек":
        prices = get_gas_prices()
        bot.send_message(message.chat.id, prices)

# Start polling
bot.polling()
