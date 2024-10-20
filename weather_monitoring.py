import requests
import time
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt

# Constants
API_KEY = '117d184eb2f0aa05b8567c2586065da4'  # Your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=' + API_KEY
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 60 * 5  # Interval of 5 minutes between API calls
THRESHOLD_TEMP = 35.0  # Temperature threshold for alerts (in Celsius)
DATABASE = 'weather_data.db'  # SQLite database for storing weather data

# Set up SQLite database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Drop the table if it exists (to ensure the schema is correct)
    cursor.execute('DROP TABLE IF EXISTS weather')
    
    # Create the table with the correct columns
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        city TEXT,
                        temp REAL,
                        feels_like REAL,
                        main TEXT,
                        timestamp INTEGER
                    )''')
    conn.commit()
    conn.close()


# Function to get weather data for a city
def get_weather(city):
    url = BASE_URL.format(city)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        feels_like = data['main']['feels_like'] - 273.15
        main_weather = data['weather'][0]['main']
        timestamp = data['dt']
        return {'city': city, 'temp': temp, 'feels_like': feels_like, 'main': main_weather, 'timestamp': timestamp}
    else:
        print(f"Failed to retrieve data for {city}. Status Code: {response.status_code}")
        return None

# Function to store weather data in SQLite database
def store_weather(data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO weather (city, temp, feels_like, main, timestamp) VALUES (?, ?, ?, ?, ?)',
                   (data['city'], data['temp'], data['feels_like'], data['main'], data['timestamp']))
    conn.commit()
    conn.close()

# Function to roll up daily weather data and calculate aggregates
def daily_summary():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    summaries = {}
    
    for city in CITIES:
        cursor.execute('''SELECT AVG(temp), MAX(temp), MIN(temp), main 
                          FROM weather WHERE city=? AND date(timestamp, 'unixepoch')=date('now')''', (city,))
        result = cursor.fetchone()
        if result[0] is not None:
            avg_temp = result[0]
            max_temp = result[1]
            min_temp = result[2]
            dominant_condition = result[3]  # Simplified logic for dominant weather condition
            summaries[city] = {'avg_temp': avg_temp, 'max_temp': max_temp, 'min_temp': min_temp, 'dominant': dominant_condition}
    
    conn.close()
    return summaries

# Function to send alert if temperature exceeds threshold
def check_alerts(data):
    if data['temp'] > THRESHOLD_TEMP:
        send_alert(data['city'], data['temp'])

# Function to send email alerts
def send_alert(city, temp):
    sender_email = "youremail@example.com"
    recipient_email = "recipient@example.com"
    subject = f"Weather Alert: {city} Temperature Exceeds {THRESHOLD_TEMP}°C"
    body = f"The temperature in {city} is {temp:.2f}°C, exceeding the threshold of {THRESHOLD_TEMP}°C."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, "your_password")
        server.sendmail(sender_email, recipient_email, msg.as_string())
    
    print(f"Alert sent for {city}: Temperature {temp:.2f}°C")

# Function to visualize weather data
def visualize_summary(summaries):
    for city, summary in summaries.items():
        plt.bar(['Avg Temp', 'Max Temp', 'Min Temp'], [summary['avg_temp'], summary['max_temp'], summary['min_temp']])
        plt.title(f"Weather Summary for {city}")
        plt.ylabel('Temperature (°C)')
        plt.show()

# Main function to continuously fetch weather data and monitor
def run_weather_monitor():
    init_db()
    
    while True:
        for city in CITIES:
            data = get_weather(city)
            if data:
                store_weather(data)
                check_alerts(data)
        
        print("Sleeping until next interval...")
        time.sleep(INTERVAL)

        # Generate daily summary and visualize
        summaries = daily_summary()
        if summaries:
            print(f"Daily Summary: {summaries}")
            visualize_summary(summaries)

# Run the weather monitoring system
if __name__ == "__main__":
    run_weather_monitor()
