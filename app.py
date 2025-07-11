%%writefile app.py
import configparser
import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

@app.route('/')
def home():
    return render_template('weather_form.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'London')
    try:
        api_key = config['openweathermap']['api_key']
        if api_key == "YOUR_API_KEY_HERE":
            return render_template('error.html', 
                                message="API key not configured - please create config.ini")
            
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return render_template('weather_result.html',
                               city=city,
                               temp=data['main']['temp'],
                               humidity=data['main']['humidity'],
                               description=data['weather'][0]['description'])
        return render_template('error.html', message=data['message'])
    except Exception as e:
        return render_template('error.html', message="Weather service error")
