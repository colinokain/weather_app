#Colin O'Kain
#October 2019

from tkinter import *
from PIL import Image, ImageTk
import requests, json, math, json

class Application(Frame):

    city = "";
    pic = 'sun.gif'
    img = Image.open(pic)
    temp = 0;
    humidity = 0;
    pressure = 0;
    description = "";
    
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.make_canvas()


    #Builds the application window
    def make_canvas(self):
        self.parent.title("The Weather")
        canvas = Canvas(self, width = 1000, height = 45, background = 'black', highlightthickness = 0)
        canvas.pack(expand = NO, fill = NONE)
        canvas.image = ImageTk.PhotoImage(self.img)
        canvas.create_image(0,1, image = canvas.image, anchor = NW)
        
        quitButton = Button(canvas, text = "Quit", command = self.quit)
        quitButton.configure(width = 10, background = "#33B5E5", relief = FLAT)
        quitButton.window = canvas.create_window(900,10,anchor = NW,window=quitButton)
        
        temperature = StringVar()
        temperatureLabel = Label(canvas, textvariable = temperature, fg = "white", background = "black", font =("arial", 16))
        temperatureLabel.config(width = 6, anchor = NW)
        canvas.create_window(80,8,anchor=NW,window = temperatureLabel)

        cityLabel = Label(canvas,text = "City: ", fg = "white", background = "black", font = ("arial", 16))
        canvas.create_window(600,8, anchor = NW, window = cityLabel)

        cityEntry = Entry(canvas)
        cityEntry.grid(row=0, column = 1)
        canvas.create_window(650,15,anchor=NW,window = cityEntry)

        cityButton = Button(canvas, text = "Go", command = lambda:[self.getInfo(cityEntry.get(), canvas), temperature.set((str(self.temp)+"°F")),
                                                                  humidity.set((str(self.humidity)+"% Humidity")),atmosphericPressure.set(str(self.pressure) + " HPA")])
        cityButton.configure(width = 7, background = "blue", relief = FLAT)
        cityButton.window = canvas.create_window(800,10,anchor = NW, window = cityButton)

        humidity = StringVar()
        humidityLabel = Label(canvas, textvariable = humidity, fg = "white", background = "black", font = ("arial", 16))
        canvas.create_window(200, 8, anchor = NW, window = humidityLabel)

        atmosphericPressure = StringVar()
        pressureLabel = Label(canvas, textvariable = atmosphericPressure, fg = "white", background = "black", font = ("arial", 16))
        canvas.create_window(400, 8, anchor = NW, window = pressureLabel)

    def getInfo(self, var, canvas):
        self.city = var
        self.getWeather()
        self.img = Image.open(self.pic)
        canvas.image = ImageTk.PhotoImage(self.img)
        canvas.create_image(0,1, image = canvas.image, anchor = NW)

        print(self.pic)
        print(self.description)
        print(self.city)

    def getWeather(self):

        with open('api.json') as f:
            data = json.load(f)

        apiKey = data['token']
        baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
        city = str(self.city)

        completeUrl = baseUrl + "appid=" + apiKey + "&q=" + city 

        response = requests.get(completeUrl)
        responseJson = response.json()

        if responseJson["cod"] != "404":
            x = responseJson["main"]

            current_temp = x["temp"]

            current_temp = (int(current_temp) - 273.15) * 9/5 + 32

            current_temp = math.ceil(current_temp)
            print(current_temp)
            self.temp = current_temp

            current_pressure = x["pressure"]
            self.pressure = current_pressure

            current_humidity = x["humidity"]
            self.humidity = current_humidity

            y = responseJson["weather"]

            weather_description = y[0]["description"]
            self.description = weather_description

            storm = ["thunderstorm with light rain", "thunderstorm with rain", "thunderstorm with heavy rain", "light thunderstorm", "thunderstorm", "heavy thunderstorm", "ragged thunderstorm",  "thunderstorm with light drizzle", "thunderstorm with drizzle", "thunderstorm with heavy drizzle"]
            drizzle = ["light intensity drizzle""drizzle", "heavy intensity drizzle", "light intensity drizzle", "drizzle rain", "heavy intensity drizzle rain", "shower rain and drizzle", "heavy shower rain and drizzle", "shower drizzle"]
            rain = ["light rain", "moderate rain", "heavy intensity rain", "very heavy rain", "extreme rain"]
            snow = ["freezing rain", "light snow", "snow", "heavy snow", "sleet", "light shower sleet", "shower sleet", "light rain and snow", "rain and snow", "light shower snow", "shower snow", "heavy shower snow"]
            shower = ["light intensity shower rain", "shower rain", "heavy intensity shower rain", "ragged shower rain"]
            mist = ["mist", "smoke" , "haze", "sand/ dust whirls", "fog", "sand" , "dust", "volcanic ash", "squalls", "tornado"]
            clear = ["clear sky"]
            few_clouds = ["few clouds"]
            scattered = ["scattered clouds"]
            overcast = ["broken clouds", "overcast clouds"]


            if(weather_description in storm):
                self.pic = "thunderstorm.gif"
            elif(weather_description in drizzle):
                self.pic = "shower_rain.gif"
            elif(weather_description in rain):
                self.pic = "rain.gif"
            elif(weather_description in snow):
                self.pic = "snow.gif";
            elif(weather_description in shower):
                self.pic = "shower_rain.gif"
            elif(weather_description in mist):
                self.pic = "mist.gif"
            elif(weather_description in clear):
                self.pic = "sun.gif"
            elif(weather_description in few_clouds):
                self.pic = "few_clouds.gif"
            elif(weather_description in scattered):
                self.pic = "cloudy.gif"
            elif(weather_description in overcast):
                self.pic = "overcast.gif"


        
if __name__ == '__main__':
    root = Tk()
    Application(root).pack(fill='both',expand = True)
    app = Application(root)
    app.mainloop()
