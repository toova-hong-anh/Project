from tkinter import *
import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pytz
import datetime
from tkinter import Tk, Button, Label
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        # Set up the window
        self.root.title("Weather App")
        self.root.geometry("780x500")
        self.color = '#B5D5FF'
        self.root.configure(bg=self.color)

        # Language selection dropdown
        self.language_var = StringVar(self.root)
        self.language_var.set("en")  # Default language
        languages = ["en", "cz", "sk"]
        self.language_dropdown = OptionMenu(self.root, self.language_var, *languages, command =self.get_weather)
        self.language_dropdown.grid(row=0, column=5, rowspan=2)
        self.language_dropdown["highlightthickness"]=0

        design_translations = {
                "en": {
                    "Write your city": "Write your city",
                    "Write your country code": "Write your country code",
                    "What's the weather?": "What's the weather?",
                    "More information": "More information",
                    "7 Day Forecast": "7 Day Forecast"
                },
                "cz": {
                    "Write your city": "Napiš své město",
                    "Write your country code": "Napiš kód své země",
                    "What's the weather?": "Jaké je počasí?",
                    "More information": "Víc informací",
                    "7 Day Forecast": "Předpověď na 7 dní"
                },
                "sk": {
                    "Write your city": "Napíš svoje mesto",
                    "Write your country code": "Napíš kód svojej krajiny",
                    "What's the weather?": "Aké je počasie?",
                    "More information": "Viac informácií",
                    "7 Day Forecast": "Predpoveď na 7 dní"
                }
            }

        language = self.language_var.get().lower()
        design_translations_dict = design_translations.get(language, design_translations["en"])

        # Labels and entry boxes
        self.city_label = Label(self.root, text=design_translations_dict["Write your city"], font=("Times New Roman", 12))
        self.city_label.grid(row=0, column=0, columnspan=2)
        self.city_label.configure(bg=self.color)
        self.city_entry = Entry(self.root, width=40)
        self.city_entry.grid(row=0, column=3,columnspan=2)
        
        self.country_label = Label(self.root, text=design_translations_dict["Write your country code"], font=("Times New Roman", 12))
        self.country_label.grid(row=1, column=0, columnspan=2)
        self.country_label.configure(bg=self.color)
        self.country_entry = Entry(self.root, width=40)
        self.country_entry.grid(row=1, column=3, columnspan=2)

        # Buttons
        self.weather_button = Button(self.root, text=design_translations_dict["What's the weather?"], font=("Times New Roman", 12),
                                     command=self.get_weather)
        self.weather_button.grid(row=2, column=0, columnspan=6, pady=10, padx=10, ipadx=260)

        self.detailed_button = Button(self.root, text=design_translations_dict["More information"], font=("Times New Roman", 12),
                                      command=self.show_detailed_weather)
        self.detailed_button.grid(row=4, column=0, columnspan=3, pady=10, padx=10, ipadx=100)

        self.seven_button = Button(self.root, text=design_translations_dict["7 Day Forecast"], font=("Times New Roman", 12),
                                      command=self.show_seven_day_weather)
        self.seven_button.grid(row=4, column=3, columnspan=3, pady=10, padx=10, ipadx=100)

        # Output with weather information
        self.output_label = Label(self.root, text="", font=("Times New Roman", 12))
        self.output_label.grid(row=3, column=2, columnspan=2)
        self.output_label.configure(bg=self.color)

        def design_language_selected(*args):        # Text changes according to the chosen language from the dropdown
            language = self.language_var.get().lower()
            design_translations_dict = design_translations.get(language, design_translations["en"])

            if hasattr(self, "weather_button"):
                self.weather_button.destroy()
            if hasattr(self, "detailed_button"):
                self.detailed_button.destroy()
            if hasattr(self, "seven_button"):
                self.seven_button.destroy()
            
            # City label and input box
            self.city_label.configure(text=design_translations_dict["Write your city"])

            # Country label and input box
            self.country_label.configure(text=design_translations_dict["Write your country code"])

            # Button to start the base weather app
            self.weather_button = Button(self.root, text=design_translations_dict["What's the weather?"], font=("Times New Roman", 12),
                                        command=self.get_weather)
            self.weather_button.grid(row=2, column=0, columnspan=6, pady=10, padx=10, ipadx=260)

            # Button to start the detailed weather app
            self.detailed_button = Button(self.root, text=design_translations_dict["More information"], font=("Times New Roman", 12),
                                        command=self.show_detailed_weather)
            self.detailed_button.grid(row=4, column=0, columnspan=3, pady=10, padx=10, ipadx=100)

            # Button to 7 days forecast
            self.seven_button = Button(self.root, text=design_translations_dict["7 Day Forecast"], font=("Times New Roman", 12), command=self.show_seven_day_weather)
            self.seven_button.grid(row=4, column=3, columnspan=3, pady=10, padx=10, ipadx=100)

            # Change language
            self.city_label.config(text=design_translations_dict["Write your city"])
            self.country_label.config(text=design_translations_dict["Write your country code"])
            self.weather_button.config(text=design_translations_dict["What's the weather?"])
            self.detailed_button.config(text=design_translations_dict["More information"])
            self.seven_button.config(text=design_translations_dict["7 Day Forecast"])

        self.language_var.trace("w", design_language_selected)

        self.root.mainloop()

    def get_weather(self):
        def go_get_weather():
            def dataDownload():    
                # API key
                api_key = "ENTER YOUR API KEY"

                # API request
                city = self.city_entry.get()
                country = self.country_entry.get()
                lang = self.language_var.get().lower()
                open_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&lang={lang}"
                response = requests.get(open_url)
            
                # Parse the JSON data
                self.weather_data = json.loads(response.text)
                return (self.weather_data)
            
            dataDownload()

            if str(self.weather_data["cod"]) == "200":          # If data is downloaded with no error
                def languageOutput():

                    def kelvin_to_celsius(kelvin):
                        celsius = str(round(kelvin - 273.15,2))
                        return celsius

                    def convert_date1(original):
                        date = str(datetime.datetime.fromtimestamp(original).strftime("%H:%M:%S %d.%m.%Y"))
                        return date 

                    def convert_date2(original):
                        timezone = int(original)
                        current_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=timezone)))
                        formatted_time = current_time.strftime("%H:%M:%S %d.%m.%Y")
                        return formatted_time

                    # Adjusting the data
                    temp = kelvin_to_celsius(self.weather_data["main"]["temp"])
                    feels_like = kelvin_to_celsius(self.weather_data["main"]["feels_like"])
                    temp_min = kelvin_to_celsius(self.weather_data["main"]["temp_min"])
                    temp_max = kelvin_to_celsius(self.weather_data["main"]["temp_max"])
                    wind = str(self.weather_data["wind"]["speed"])
                    pressure = str(self.weather_data["main"]["pressure"])
                    dataCity = str(self.weather_data["name"])
                    dataCountry = str(self.weather_data["sys"]["country"])
                    time = convert_date1(self.weather_data["dt"])
                    timezone =str(convert_date2(self.weather_data["timezone"]))
                    
                    description = str(self.weather_data["weather"][0]["description"])

                    basic_translations = {
                        "en": {
                            "Temperature: ": "Temperature: ",
                            "Description: ": "Description: ",
                            "Feels like: ": "Feels like: ",
                            "Minimum Temperature: ": "Minimum Temperature: ",
                            "Maximum Temperature: ": "Maximum Temperature: ",
                            "Wind speed: ": "Wind speed: ",
                            "Pressure: ": "Pressure: ",
                            "City: ": "City: ",
                            "Country: ": "Country: ",
                            "Data obtained at: ": "Data obtained at: ",
                            "Local time: ": "Local time: "
                        },
                        "cz": {
                            "Temperature: ": "Teplota: ",
                            "Description: ": "Popis: ",
                            "Feels like: ": "Pocitová teplota: ",
                            "Minimum Temperature: ": "Minimální teplota: ",
                            "Maximum Temperature: ": "Maximální teplota: ",
                            "Wind speed: ": "Rychlost větru: ",
                            "Pressure: ": "Tlak: ",
                            "City: ": "Město: ",
                            "Country: ": "Stát: ",
                            "Data obtained at: ": "Data získána v: ",
                            "Local time: ": "Lokální čas: "
                        },
                        "sk": {
                            "Temperature: ": "Teplota: ",
                            "Description: ": "Popis: ",
                            "Feels like: ": "Pocitová teplota: ",
                            "Minimum Temperature: ": "Minimální teplota teplota: ",
                            "Maximum Temperature: ": "Maximální teplota: ",
                            "Wind speed: ": "Rýchlosť vetra: ",
                            "Pressure: ": "Tlak: ",
                            "City: ": "Mesto: ",
                            "Country: ": "Štát: ",
                            "Data obtained at: ": "Dáta získané o: ",
                            "Local time: ": "Miestny čas : "
                        }
                    }

                    language = self.language_var.get().lower()
                    translations_dict = basic_translations.get(language, basic_translations["en"])
                    output_text = (translations_dict["Temperature: "] + temp + "°C\n"
                                + translations_dict["Description: "] + description + "\n"
                                + translations_dict["Feels like: "] + feels_like + "°C\n"
                                + translations_dict["Minimum Temperature: "] + temp_min + "°C\n"
                                + translations_dict["Maximum Temperature: "] + temp_max + "°C\n"
                                + translations_dict["Wind speed: "] + wind + " m/s\n"
                                +translations_dict["Pressure: "] + pressure + " hPa\n"
                                + translations_dict["City: "] + dataCity + "\n"
                                + translations_dict["Country: "] + dataCountry + "\n"
                                + translations_dict["Data obtained at: "] + time + "\n"
                                + translations_dict["Local time: "] + timezone)
                
                    self.output_label.config(text=output_text)
                languageOutput()

                def show_image():
                    # Create a label to display the image
                    self.picture_label1 = Label(self.root, text="", font=("Times New Roman", 12))
                    self.picture_label1.grid(row=3, column=0, columnspan=2)
                    self.picture_label1.configure(bg=self.color)

                    self.picture_label2 = Label(self.root, text="", font=("Times New Roman", 12))
                    self.picture_label2.grid(row=3, column=4, columnspan=2)
                    self.picture_label2.configure(bg=self.color)

                    code = str(self.weather_data["weather"][0]["icon"])
                    
                    #print("code is " + code)       # Checking the code of image needed

                    # Load the image using PIL
                    image1 = Image.open(f"./Weather/{code}.png")

                    # Convert the image to PhotoImage
                    photo1 = ImageTk.PhotoImage(image1)

                    # Update with the image
                    self.picture_label1.config(image=photo1)
                    self.picture_label1.image = photo1  # Keep a reference to the PhotoImage

                    # Load the image using PIL
                    image2 = Image.open(f"./Weather/{code}.png")

                    # Convert the image to PhotoImage
                    photo2 = ImageTk.PhotoImage(image2)

                    # Update with the image
                    self.picture_label2.config(image=photo2)
                    self.picture_label2.image = photo2  # Keep a reference to the PhotoImage

                show_image()

                def language_selected(*args):
                    dataDownload()
                    languageOutput()
                    show_image()
                        
                # Configure the trace method to call the language_selected function when the variable changes
                self.language_var.trace("w", language_selected)
            else:               # If data is downloaded with an error
                def remove_images():        # Delete pictures if there are any
                    if hasattr(self, "picture_label1"): 
                            self.picture_label1.destroy()
                    if hasattr(self, "picture_label2"):
                            self.picture_label2.destroy()
                remove_images()

                def errorFunction(*args):
                    error_translations = {
                    "en": {
                        "City not found": "City not found"
                    },
                    "cz": {
                        "City not found": "Město nenalezeno"
                    },
                    "sk": {
                        "City not found": "Mesto sa nenašlo"
                    }
                    }

                    language = self.language_var.get().lower()
                    error_translations_dict = error_translations.get(language, error_translations["en"])

                    output_text = error_translations_dict["City not found"]
                    self.output_label.config(text=output_text)
                errorFunction()

                # Configure the trace method to call the functions when the variable changes
                self.language_var.trace("w", remove_images)
                self.language_var.trace("w", errorFunction)
               
            print(self.weather_data)        # Check the json data downloaded using API

        go_get_weather()

    def show_detailed_weather(self):        # Button "More Information"
        try:
            city = self.city_entry.get()
            country = self.country_entry.get()
            weather_data = self.weather_data
            language = self.language_var.get().lower()
            color = self.color

            # Create a new window for the detailed weather forecast
            detailed_window = Toplevel(self.root)
            detailed_app = DetailedWeather(detailed_window, city, country, weather_data, language, color)
        except Exception:           # In case user did not enter city and country
            def errorFunction1(*args):
                    error_translations1 = {
                    "en": {
                        "Please enter the city or the country code": "Please enter the city or the country code"
                        },
                    "cz": {
                        "Please enter the city or the country code": "Prosím zadejte město nebo kód země"
                    },
                    "sk": {
                        "Please enter the city or the country code": "Prosím zadajte mesto alebo kód krajiny"
                    }
                    }

                    language = self.language_var.get().lower()
                    error_translations1_dict = error_translations1.get(language, error_translations1["en"])

                    output_text1 = error_translations1_dict["Please enter the city or the country code"]
                    self.output_label.config(text=output_text1)

                    # Delete pictures if there are any
                    if hasattr(self, "picture_label1"):    
                        self.picture_label1.destroy()
                    if hasattr(self, "picture_label2"):
                        self.picture_label2.destroy()

            errorFunction1()

            # Configure the trace method to call the function when the variable changes
            self.language_var.trace("w", errorFunction1)
                        
    def show_seven_day_weather(self):           # Button "7 Day Forecast"
        city = self.city_entry.get()
        country = self.country_entry.get()

        if not city or not country:             # In case user did not enter city and country
            def errorFunction1(*args):
                    error_translations1 = {
                    "en": {
                        "Please enter the city or the country code": "Please enter the city or the country code"
                        },
                    "cz": {
                        "Please enter the city or the country code": "Prosím zadejte město nebo kód země"
                    },
                    "sk": {
                        "Please enter the city or the country code": "Prosím zadajte mesto alebo kód krajiny"
                    }
                    }

                    language = self.language_var.get().lower()
                    error_translations1_dict = error_translations1.get(language, error_translations1["en"])

                    output_text1 = error_translations1_dict["Please enter the city or the country code"]
                    self.output_label.config(text=output_text1)

                    # Delete pictures if there are any
                    if hasattr(self, "picture_label1"): 
                        self.picture_label1.destroy()
                    if hasattr(self, "picture_label2"):
                        self.picture_label2.destroy()
            errorFunction1()
       
        weather_data = self.weather_data
        language = self.language_var.get().lower()
        color = self.color

        # Create a new window for the detailed weather forecast
        seven_day_window = Toplevel(self.root)
        seven_day_app = SevenDayWeather(seven_day_window, city, country, weather_data, language, color)

        # Configure the trace method to call the function when the variable changes
        self.language_var.trace("w", errorFunction1)

class DetailedWeather:          # Button "More information"
    def __init__(self, root, city, country, weather_data, language, color):
        self.root = root
        self.city = city
        self.country = country
        self.weather_data = weather_data
        self.language = language
        self.color = color
        self.output_detailed_label = Label(self.root, text="", font=("Times New Roman", 12))
        self.output_detailed_label.grid(row=1, column=0)
        self.output_detailed_label.configure(text=self.get_detailed_weather())
        self.output_detailed_label.configure(bg=self.color)
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("More info")
        self.root.geometry("400x300")
        self.root.configure(bg=self.color)

    def get_detailed_weather(self):
        detailed_translations = {
                "en": {
                    "Sunrise: ": "Sunrise: ",
                    "Sunset: ": "Sunset: ",
                    "Humidity: ":"Humidity: ",
                    "Visibility: ":"Visibility: ",
                    "Cloudiness: ":"Cloudiness: ",
                    "Atmospheric pressure on the sea level: ": "Atmospheric pressure on the sea level: ",
                    "Atmospheric pressure on the ground level: ": "Atmospheric pressure on the ground level: ",
                    "Pressure data for sea level and ground level is unavailable": "Pressure data for sea level and ground level is unavailable",
                    "Rain volume for the last 1 hour: ": "Rain volume for the last 1 hour: ",
                    "Rain volume for the last 3 hours: ": "City: ",
                    "Rain data unavailable": "Rain data unavailable",
                    "Snow volume for the last 1 hour: ": "Snow volume for the last 1 hour: ",
                    "Snow volume for the last 3 hours: ":"Snow volume for the last 3 hours: ",
                    "Snow data unavailable":"Snow data unavailable",
                    "Data not found":"Data not found"
                },
                "cz": {
                    "Sunrise: ": "Východ slunce: ",
                    "Sunset: ": "Západ slunce: ",
                    "Humidity: ":"Vlhkost: ",
                    "Visibility: ":"Viditelnost: ",
                    "Cloudiness: ":"Oblačnost: ",
                    "Atmospheric pressure on the sea level: ": "Atmosférický tlak na hladině moře: ",
                    "Atmospheric pressure on the ground level: ": "Atmosférický tlak na úrovni země: ",
                    "Pressure data for sea level and ground level is unavailable": "Data o tlaku na hladině moře a na úrovni země nejsou k dispozici",
                    "Rain volume for the last 1 hour: ": "Množství deště za poslední 1 hodinu: ",
                    "Rain volume for the last 3 hours: ": "Množství deště za posledních 3 hodiny: ",
                    "Rain data unavailable": "Data o dešti nejsou k dispozici",
                    "Snow volume for the last 1 hour: ": "Množství sněhu za poslední 1 hodinu: ",
                    "Snow volume for the last 3 hours: ":"Množství sněhu za posledních 3 hodiny: ",
                    "Snow data unavailable":"Data o sněhu nejsou k dispozici",
                    "Data not found":"Data nenalezena"
                },
                "sk": {
                    "Sunrise: ": "Východ slnka: ",
                    "Sunset: ": "Západ slnka: ",
                    "Humidity: ":"Vlhkosť: ",
                    "Visibility: ":"Viditeľnosť: ",
                    "Cloudiness: ":"Oblačnosť: ",
                    "Atmospheric pressure on the sea level: ": "Atmosférický tlak na úrovni mora: ",
                    "Atmospheric pressure on the ground level: ": "Atmosférický tlak na úrovni zeme: ",
                    "Pressure data for sea level and ground level is unavailable": "Údaje o tlaku na hladine mora a na úrovni zeme nie sú k dispozícii",
                    "Rain volume for the last 1 hour: ": "Množstvo dažďa za poslednú 1 hodinu: ",
                    "Rain volume for the last 3 hours: ": "Množstvo dažďa za posledných 3 hodiny: ",
                    "Rain data unavailable": "Údaje o daždi nie sú k dispozícii",
                    "Snow volume for the last 1 hour: ": "Množstvo snehu za poslednú 1 hodinu: ",
                    "Snow volume for the last 3 hours: ":"Množstvo snehu za posledných 3 hodiny: ",
                    "Snow data unavailable":"Údaje o snehu nie sú k dispozícii",
                    "Data not found":"Dáta sa nenašla"
                }
            }

        translations_detailed_dict = detailed_translations.get(self.language, detailed_translations["en"])

        # Adjusting  data

        def sunFunction():
            def convert_time(original):
                hours = str(datetime.datetime.fromtimestamp(original).strftime("%H:%M:%S"))
                return hours
        
            sunrise = convert_time(self.weather_data["sys"]["sunrise"])
            sunset = convert_time(self.weather_data["sys"]["sunset"])

            sunrise_text = (translations_detailed_dict["Sunrise: "] + sunrise +"\n" +
                     translations_detailed_dict["Sunset: "] + sunset)
            return sunrise_text
        
        def otherInfoFunction():
            humidity = str(self.weather_data["main"]["humidity"])
            visibility = str(self.weather_data["visibility"])
            clouds = str(self.weather_data["clouds"]["all"])

            otherInfo_text = (translations_detailed_dict["Humidity: "] + humidity + "%\n"
                              + translations_detailed_dict["Visibility: "] + visibility + "m\n"
                              + translations_detailed_dict["Cloudiness: "] + clouds + "%")
            return otherInfo_text
            
        def pressureFunction():
            if "sea_level" in self.weather_data["main"]:
                # data not always available
                seaPressure = str(self.weather_data["main"]["sea_level"])
                groundPressure = str(self.weather_data["main"]["grnd_level"])
                pressure_text = (translations_detailed_dict["Atmospheric pressure on the sea level: "] + seaPressure + " hPa\n"
                            + translations_detailed_dict["Atmospheric pressure on the ground level: "] + groundPressure + "hPa")
            else:
                pressure_text = translations_detailed_dict["Pressure data for sea level and ground level is unavailable"]
            return pressure_text

        def rainFunction():
            if "rain" in self.weather_data:
                rain1h = str(self.weather_data["rain"]["1h"])
                if "3h" in self.weather_data:
                    rain3h = str(self.weather_data["rain"]["3h"])
                    rain_text = (translations_detailed_dict["Rain volume for the last 1 hour: "] + rain1h + " mm\n"
                                + translations_detailed_dict["Rain volume for the last 3 hours: "] + rain3h + " mm")
                else:
                    rain_text = (translations_detailed_dict["Rain volume for the last 1 hour: "] + rain1h + " mm")
            else:
                    rain_text = translations_detailed_dict["Rain data unavailable"]
            return rain_text
        
        def snowFunction():
            if "snow" in self.weather_data:
                snow1h = str(self.weather_data["snow"]["1h"])
                if "3h" in self.weather_data:
                    snow3h = str(self.weather_data["snow"]["3h"])
                    snow_text = (translations_detailed_dict["Snow volume for the last 1 hour: "] + snow1h + " mm\n"
                                + translations_detailed_dict["Snow volume for the last 3 hours: "] + snow3h + " mm")
                else:
                    snow_text = (translations_detailed_dict["Snow volume for the last 1 hour: "] + snow1h + " mm")
            else:
                    snow_text = translations_detailed_dict["Snow data unavailable"]
            return snow_text
        
        # In case data is downloaded with an error
        if self.weather_data["cod"] == "404":
            detailedText = translations_detailed_dict["Data not found"]
            self.output_detailed_label.config(text=detailedText)
            self.output_detailed_label.grid(row=1, column=0)
        else:
            sunText = sunFunction()
            otherinfoText = otherInfoFunction()
            pressureText = pressureFunction()
            rainText = rainFunction()
            snowText = snowFunction()

            detailedText = str(sunText)+ "\n"+ str(otherinfoText) + "\n" +  str(pressureText) +"\n"+ str(rainText) +"\n"+ str(snowText)

            self.output_detailed_label.config(text=detailedText)
            self.output_detailed_label.grid(row=1, column=0)

class SevenDayWeather:          # Button "7 Day Forecast"
    def __init__(self, master, city, country, weather_data, language, color):
        self.master = master
        self.city = city
        self.country = country
        self.weather_data = weather_data
        self.output_graph_label = Label(self.master, text="", font=("Times New Roman", 12))
        self.language = language
        self.color = color
        self.setup_ui()
        self.seven_day_graph()
    
    def setup_ui(self):
        self.master.title("7 Day Weather")
        self.master.geometry("700x500")
        self.master.configure(bg=self.color)
                
    def seven_day_graph(self):
        graph_translations = {
                    "en": {
                        "Days": "Days",
                        "Temperatures °C": "Temperatures °C",
                        "Next 7 days":"Next 7 days",
                        "Visibility: ":"Visibility: ",
                        "Cloudiness: ":"Cloudiness: ",
                        "Data not found":"Data not found"
                    },
                    "cz": {
                        "Days": "Dny",
                        "Temperatures °C": "Teploty °C",
                        "Next 7 days":"Následujících 7 dnů",
                        "Visibility: ":"Viditelnost: ",
                        "Cloudiness: ":"Oblačnost: ",
                        "Data not found":"Data nenalezena"
                    },
                    "sk": {
                        "Days": "Dni",
                        "Temperatures °C": "Teploty °C",
                        "Next 7 days":"Nasledujúcich 7 dní",
                        "Visibility: ":"Viditeľnosť: ",
                        "Cloudiness: ":"Oblačnosť: ",
                        "Data not found":"Dáta sa nenašla"
                    }
                }
        translations_graph_dict = graph_translations.get(self.language, graph_translations["en"])
        
        def Meteo_data_download():                          # Meteo API offers weather data for the next 7 days
            lat = self.weather_data["coord"]["lat"]         # It is needed to use lat and lon from the first API to get the right data from the second API
            lon = self.weather_data["coord"]["lon"]
            first_timezone = self.weather_data["timezone"]

            def offset_to_timezone(offset):
                offset_timedelta = datetime.timedelta(seconds=offset)       # Convert the offset to a timedelta object
                all_timezones = pytz.all_timezones                          # Get a list of all available time zones

                # Iterate over each time zone
                for timezone in all_timezones:
                    current_offset = pytz.timezone(timezone).utcoffset(datetime.datetime.now())     # Get the current time zone's offset
                    if current_offset == offset_timedelta:                                          # Found the matching time zone
                        return timezone
                return None         # If no match is found, return None or handle the case as needed

            offset = first_timezone  # Time offset in seconds
            timezone_identifier = offset_to_timezone(offset)

            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,windspeed_10m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&timezone={timezone_identifier}"
            response = requests.get(url)

            meteo_data = json.loads(response.text)
            return meteo_data

        def Graph_it():             # Creates a graph for the next 7 days
            max_temperatures = newData["daily"]["temperature_2m_max"]
            min_temperatures = newData["daily"]["temperature_2m_min"]
            not_formatted = newData["daily"]["time"]
            days = [datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.') for date in not_formatted]

            def hat_graph(ax, xlabels, values, group_labels):
                def label_bars(heights, rects):
                    for height, rect in zip(heights, rects):            #Attach a text label on top of each bar
                        ax.annotate(f'{height}',
                                    xy=(rect.get_x() + rect.get_width()/3 , height),
                                    xytext=(0, 4),  # 4 points vertical offset.
                                    textcoords='offset points',
                                    ha='center', va='bottom')

                values = np.asarray(values)
                x = np.arange(values.shape[1])
                ax.set_xticks(x, labels=xlabels)
                spacing = 0.3  # Spacing between hat groups
                width = (1 - spacing) / values.shape[0]
                heights0 = values[0]
                for i, (heights, group_label) in enumerate(zip(values, group_labels)):
                    style = {'fill': False} if i == 0 else {'edgecolor': 'black'}
                    rects = ax.bar(x - spacing/2 + i * width, heights - heights0,
                                width, bottom=heights0, label=group_label, **style)
                    label_bars(heights, rects)

            # Range of the graph table
            minMin = min(min_temperatures) - 5          
            maxMax = max(max_temperatures) + 5

            fig, ax = plt.subplots()
            fig.patch.set_facecolor(self.color)
            hat_graph(ax, days, [min_temperatures, max_temperatures], ['Minimum', 'Maximum'])

            translations_graph_dict = graph_translations.get(self.language, graph_translations["en"])

            # Text for labels, title, x-axis
            ax.set_xlabel(translations_graph_dict["Days"])
            ax.set_ylabel(translations_graph_dict["Temperatures °C"])
            ax.set_ylim(minMin, maxMax)
            ax.set_title(translations_graph_dict["Next 7 days"])

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0)
            canvas.configure(bg=self.color)

        # In case data is downloaded with an error
        if self.weather_data["cod"] == "404":           
            detailedText = translations_graph_dict["Data not found"]
            self.output_graph_label.config(text=detailedText)
            self.output_graph_label.grid(row=1, column=0)
            self.output_graph_label.configure(bg=self.color)
        else:
            newData = Meteo_data_download() 
            Graph_it()
            
root = Tk()
weather_app = WeatherApp(root)  # Base weather app
root.mainloop()