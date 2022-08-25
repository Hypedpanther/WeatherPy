import tkinter as tk
import json
import requests
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.window()
        self.create_widgets()
        self.display_widgets()

    
    def window(self):
        self.title("Weather")
        self.geometry("400x400")
        self.resizable(False, False)
  
    def create_widgets(self):
        self.heading_label = tk.Label(self, 
                                text="Weather", 
                                font=("Sans Serif", 20),
                                fg="dark blue")
        
        self.input_label = tk.Label(self,
                                    text = "Enter a location:"
                                    )
        self.location = tk.Entry(self, width=30)
        self.enter_button = tk.Button(self, text="Enter", command=self.get_weather)
        self.reset_button = tk.Button(self, text="Reset", command=self.clear)
        
    
    def display_widgets(self):
        self.heading_label.pack(pady=3, padx=3)
        self.input_label.pack(pady=3, padx=3)
        self.location.pack(pady=3, padx=3)
        self.enter_button.pack(pady=3, padx=3)
        self.reset_button.pack(pady=3, padx=3)
       

    def clear(self):
        self.location.delete(0, tk.END)
        self.results_label.destroy()
        self.enter_button.config(state="normal")
        

    def get_weather(self): 
        self.enter_button.config(state="disabled")
        with open("src/settings.json", "r") as jsonfile:
            data = json.load(jsonfile)
            weather_api_key = data["weather_api_key"]
            base_url = data["weather_url"]
            url = f'{base_url}?q={self.location.get()}&appid={weather_api_key}&units=metric'
            with requests.get(url) as resp:
                r = resp.json()
            
        if r["cod"] != "404":
            current_temperature = r["main"]["temp"]
            current_pressure = r["main"]["pressure"]
            current_humidity = r["main"]["humidity"]
            weather_description = r["weather"][0]["description"]

            self.results_label = tk.Label(self,
                    text=f"Weather in {self.location.get()}"  + "\n" +
                    f"Temperature: {current_temperature}°C" + "\n" +
                    f"Humidity: {current_humidity}%" + "\n" +
                    f"Atmospheric Pressure: {current_pressure}hPa" + "\n" +
                    f"Description: {weather_description}"+ "\n" +
                    f"Time: {datetime.now().strftime('%H:%M:%S')}")
        elif r["cod"] == "404":
            self.results_label = tk.Label(self,
                    text="Location not found, please try again")
        else:
            self.results_label = tk.Label(self,
                    text="An error occured")
        self.results_label.pack(pady=3, padx=3)
        self.thanks_label = tk.Label(self,
                text = f"Thanks for Using WeatherPy")
        self.thanks_label.pack(pady=3, padx=3)

def main():
    application = App()
    application.mainloop()

if __name__ == "__main__":
    main()
