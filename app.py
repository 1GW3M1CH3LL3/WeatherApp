# Import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import ttkbootstrap

# Function to get weather
def get_weather(user_city):
    api_key = 'c617d18c3394203b87b7f1d1b844a091'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={user_city}&units=imperial&appid={api_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    # Parse the response json to get weather info
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temperature = weather["main"]["temp"]
    weather_des = weather["weather"][0]["description"]
    user_city = weather['name']
    country = weather['sys']['country']

    # Get icon URL and return all weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, weather_des, user_city, country)

# Function to search for weather in a city
def search():
    user_city = city_entry.get()
    result = get_weather(user_city)
    if result is None:
        return 

    # If the city is found, unpack the weather info    
    icon_url, temperature, weather_des, user_city, country = result
    location_label.configure(text=f"{user_city}, {country}")

    try:
        # Get the weather icon image from the URL and update the icon label
        response = requests.get(icon_url, stream=True)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        
        image = Image.open(response.raw)
        icon = ImageTk.PhotoImage(image)
        icon_label.configure(image=icon)
        icon_label.image = icon

    except (requests.exceptions.RequestException, UnidentifiedImageError) as e:
        messagebox.showerror("Error", "Failed to retrieve weather icon")

    # Update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°F")
    weather_label.configure(text=f"Description: {weather_des}")

# Set up the main window
root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

# Entry widget to enter city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Button widget to search for weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label widget to show the city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Label widget to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget to show the temperature
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# Label widget to show the weather description
weather_label = tk.Label(root, font="Helvetica, 20")
weather_label.pack()

# Run the main event loop
root.mainloop()
