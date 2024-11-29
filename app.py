from flask import Flask, render_template, request, jsonify
import openai
import requests
from eliza_chatbot import eliza_response

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "6d9a135a6a34c5bdfae8a21d4f909ac1"

# Replace with your OpenAI API key
openai.api_key = "T7JFff6gsXxoXB1NpRwe6EPXZBNDNeHMBwqorqNA2iIoQbcUZie0JTbfX3XFj4eBm2Rb_nXzJZT3BlbkFJYRBzJOBgcdPJUQbSDr3gtdDt9iLhVacU4h4yyhdZSRuXZw1rR7VIjxd_txibD5Vd2O301A7tQA"

# Function to fetch weather data
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            return f"The weather in {city} is {weather} with a temperature of {temperature}°C. It feels like {feels_like}°C."
        elif response.status_code == 404:
            return "City not found. Please check the name and try again."
        else:
            return "Unable to fetch weather data. Please try later."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate OpenAI response using the latest API
def generate_openai_response(user_input):
    try:
        # Using ChatCompletion API for GPT-3.5 or GPT-4 models
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to "gpt-4" if preferred
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150  # Adjust tokens as necessary
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")

    # Check if the input contains a weather query
    if "weather" in user_input.lower():
        # Extract city name from user input
        city = user_input.split("weather in")[-1].strip()
        if city:
            response = get_weather(city)
        else:
            response = "Bangalore"  # Default city if no city is provided
    else:
        # Check if the input is directed to OpenAI for advanced queries
        if "openai" in user_input.lower():
            response = generate_openai_response(user_input)
        else:
            # Use the default Eliza chatbot response for non-weather and non-OpenAI queries
            response = eliza_response(user_input)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
