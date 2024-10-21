# Weather Monitoring System

The Weather Monitoring System is a real-time data processing application that retrieves and monitors weather data for major cities in India using the OpenWeatherMap API. The system calculates daily summaries, triggers alerts based on user-defined thresholds, and provides visual insights into weather conditions.

## Features
1.Fetches real-time weather data for Indian metros (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad) from the OpenWeatherMap API.   
2.Converts temperature from Kelvin to Celsius.    
3.Provides daily weather summaries, including:    
Average Temperature     
Maximum and Minimum Temperatures    
Dominant Weather Condition  
4.Configurable threshold-based alerts (e.g., notify when temperature exceeds a certain value).    
5.Data is stored locally using SQLite for further analysis.        
6.Displays basic visualizations of daily summaries and alerts.

## Prerequisites
#### Before running the application, ensure you have the following installed:

Python 3.x  
pip (Python package manager)    
SQLite3

## Python Packages

You can install the necessary Python libraries by running:

```bash
 pip install requests matplotlib

```
## OpenWeatherMap API Key
You need an API key from OpenWeatherMap to run this project. You can obtain one from the    
[Get your OpenWeatherMap API key](https://home.openweathermap.org/users/sign_up)

After acquiring the key, set the value in the code:
```bash
 API_KEY = 'your_api_key_here'

```
Replace 'your_api_key_here' with your actual API key.

# How to Run

### 1.Clone the repository
```bash
 git clone https://github.com/nidhihey1/Weather-Monitoring-System.git
cd Weather-Monitoring-System

```
### 2.Set up your environment:
Ensure that Python and the required packages (e.g., requests, matplotlib) are installed.

### 3.Run the script:
Start the weather monitoring system by running:
```bash
 python weather_monitoring.py

```
The system will begin retrieving weather data at the configured intervals (e.g., every 5 minutes)

### 4.Check the Database:

The weather data is stored in a local SQLite database (weather.db). You can use SQLite tools to view and analyze the stored data

### 5.View Alerts and Visualizations:

Alerts will be printed to the console when a user-defined threshold is breached.
Visualizations of daily weather summaries and alerts can be generated through the system.

## Configuration

You can configure the following aspects of the system:
#### Weather update interval: 
Set how frequently the system retrieves data from the OpenWeatherMap API.
#### Thresholds: 
Define temperature thresholds that trigger alerts (e.g., temperature exceeding 35°C for two consecutive updates).
## Testing
#### Test Cases

#### 1.System Setup:   
Verify successful connection to the OpenWeatherMap API.     
#### 2.Data Retrieval:     
Simulate API calls at configurable intervals.   
Ensure accurate parsing of weather data.
#### 3.Temperature Conversion:     
Validate temperature conversion from Kelvin to Celsius.     
#### 4.Daily Summaries:    
Verify correct calculations for average, maximum, minimum temperatures, and dominant weather condition.     
#### 5.Alerts:     
Simulate weather data exceeding defined thresholds.     
Verify alert functionality when thresholds are breached.
