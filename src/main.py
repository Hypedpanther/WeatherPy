import json
import tkinter as tk
from datetime import datetime

import requests


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.location = tk.Entry(self, width=30)
        self.reset_button = tk.Button(self, text="Reset", command=self.clear)
        self.enter_button = tk.Button(self, text="Enter", command=self.get_weather)
        self.input_label = tk.Label(self,
                                    text="Enter a location:"
                                    )
        self.heading_label = tk.Label(self,
                                      text="Weather",
                                      font=("Sans Serif", 20),
                                      fg="dark blue")
        self.thanks_label = tk.Label(self,
                                     text=f"Thanks for Using WeatherPy")
        self.results_label = tk.Label(self,
                                      text="An error occurred")
        self.window()
        self.display_widgets()
        self.bind('<Return>', lambda event: self.get_weather())

    def window(self):
        self.title("Weather")
        self.geometry("400x400")
        self.resizable(False, False)

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
        self.thanks_label.destroy()

    def get_weather(self):
        self.enter_button.config(state="disabled")
        with open("settings.json", "r") as jsonfile:
            data = json.load(jsonfile)
            weather_api_key = data["weather_api_key"]
            base_url = data["weather_url"]
            url = f'{base_url}?q={self.location.get()}&appid={weather_api_key}&units=metric'
            with requests.get(url) as resp:
                resp = resp.json()

        if resp["cod"] != "404":
            current_temperature = resp["main"]["temp"]
            current_pressure = resp["main"]["pressure"]
            current_humidity = resp["main"]["humidity"]
            weather_description = resp["weather"][0]["description"]

            self.results_label = tk.Label(self,
                                          text=f"Weather in {self.location.get()}" + "\n" +
                                               f"Temperature: {current_temperature}°C" + "\n" +
                                               f"Humidity: {current_humidity}%" + "\n" +
                                               f"Atmospheric Pressure: {current_pressure}hPa" + "\n" +
                                               f"Description: {weather_description}" + "\n" +
                                               f"Time: {datetime.now().strftime('%H:%M:%S')}")
        elif resp["cod"] == "404":
            self.results_label = tk.Label(self,
                                          text="Location not found, please try again")

        self.results_label.pack(pady=3, padx=3)
        self.thanks_label.pack(pady=3, padx=3)


def main():
    application = App()
    application.mainloop()


if __name__ == "__main__":
    main()
