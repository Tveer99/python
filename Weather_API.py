import sys
import requests
from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget,
                             QLabel, QVBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.city_label = QLabel("Enter City Name:",self)  # Label for city input
        self.city_label.setAlignment(Qt.AlignCenter)  # Center align the text in label
        
        self.city_input = QLineEdit(self)  # Input field for city name
        self.city_input.setPlaceholderText("Type Here")  # Placeholder text for input field
        self.city_input.setAlignment(Qt.AlignCenter)  # Center align the text in input field
        
        self.get_weather_button = QPushButton("Get Weather",self)  # Button to fetch weather data
        
        self.temperature_label = QLabel(self)  # Label for temperature display
        self.temperature_label.setAlignment(Qt.AlignCenter)  # Center align the text in temperature label
        
        self.emoji_label = QLabel(self)  # Label for weather emoji display
        self.emoji_label.setAlignment(Qt.AlignCenter)  # Center align the text in emoji label
        
        self.description_label = QLabel(self)  # Label for weather description
        self.description_label.setAlignment(Qt.AlignCenter)  # Center align the text in description label
        
        self.init()
        
    def init(self):
        self.setWindowTitle("Weather")     # Set the window title
        #self.setFixedSize(550, 610)  # Set fixed window size
        
        vbox = QVBoxLayout()  # Create a vertical box layout
        vbox.addWidget(self.city_label)  # Add city label to layout
        vbox.addWidget(self.city_input)  # Add city input field to layout
        vbox.addWidget(self.get_weather_button)  # Add weather button to layout
        vbox.addWidget(self.temperature_label)  # Add temperature label to layout
        vbox.addWidget(self.emoji_label)  # Add emoji label to layout
        vbox.addWidget(self.description_label)  # Add description label to layout
        
        self.setLayout(vbox)  # Set the layout for the main window
        
        self.city_label.setObjectName("city_label")  # Set object name for city label
        self.city_input.setObjectName("city_input")  # Set object name for city input field
        self.get_weather_button.setObjectName("get_weather_button")  # Set object name for weather button
        self.temperature_label.setObjectName("temperature_label")  # Set object name for temperature label
        self.emoji_label.setObjectName("emoji_label")  # Set object name for emoji label
        self.description_label.setObjectName("description_label")  # Set object name for description label
        
        self.setStyleSheet("""
            QWidget{
                background-color: #aea8ba;
            }
            QLabel,QPushButton{
                font-family: Arial;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: bold;
            }                   
            QLineEdit#city_input{
                font-size: 40px;
                border: 2px solid #000000;
                border-radius: 7px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
                background-color: #00865f;
                border-radius: 7px;
                color: white;
                padding: 10px;
            }
            QPushButton#get_weather_button:hover{
                background-color: #005031;
                }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather)  # Connect button click to get_weather method

    def get_weather(self):
        api_key="b0b0c0c83c01e8d4b24a166b51ca2c41"
        city=self.city_input.text()
        url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        #https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
        
        try:    
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            print(response.status_code)
            
            if data["cod"]==200:
                self.display_weather(data)
        
        except requests.exceptions.HTTPError as error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check the city name")   
                case 401:
                    self.display_error("Invalid API key:\nPlease check your API key")
                case 403:
                    self.display_error("Access denied")                
                case 404:
                    self.display_error("City not found")
                case 500:
                    self.display_error("Internal server error:\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway:\n Invalid response from the server")
                case 503:
                    self.display_error("Service unavailable:\n Server is down")
                case 504:
                    self.display_error("Gateway timeout: \nServer is taking too long to respond")              
                case _:
                    self.display_error(f"An error occurred:\n {error}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Network error, please check your connection")            
        except requests.exceptions.Timeout:
            self.display_error("Request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException:
            self.display_error("An error occurred:")

             
    def display_error(self, message):
        self.emoji_label.setStyleSheet("font-size: 35px;")
        self.temperature_label.clear()  # Clear emoji label
        self.description_label.clear()  # Clear description label
        self.emoji_label.setText(message)  # Clear temperature label

    def display_weather(self,data):
        weather_id=data["weather"][0]["id"]
        self.emoji_label.setStyleSheet("font-size: 100px;")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))  # Set weather emoji
        temp=data["main"]["temp"]
        self.temperature_label.setText(f"{temp:.0f}°C")
        weather=data["weather"][0]["description"]
        self.description_label.setText(weather.title())
        
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""

def main():
    app = QApplication(sys.argv)
    Weather_App = WeatherApp()
    Weather_App.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()



