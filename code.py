import RPi.GPIO as GPIO
import firebase_admin, time, requests, Adafruit_DHT
from firebase_admin import db
from firebase_admin import credentials
from threading import Thread

# init the firebase
cred = credentials.Certificate('/home/pi/Desktop/project/DHT11_firebase_pi3/serviceAccountKey')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://temperature-measurement-app.firebaseio.com/'})
ref = db.reference('app')

# init the GPIO pins and sensor pin
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
sensor = Adafruit_DHT.DHT11
pin_sensor = 4

# temperature and humidity variable
temperature_in_home = 0
humidity_in_home = 0
temperature_out_side = 0
humidity_out_side = 0


# update data from sensor in home to firebase 
def update_in_home():
    while True:
        humidity_in_home, temperature_in_home = Adafruit_DHT.read_retry(sensor, pin_sensor)
        if humidity_in_home is not None and temperature_in_home is not None:
            print('Temperature in home', temperature_in_home)
            print('Humidity in home', humidity_in_home)
            users_ref = ref.child('In Home')
            users_ref.set({
            'Temperature': temperature_in_home ,
            'Humidity': humidity_in_home
            })
        else:
            print('Failed to get reading. Try again!')
    time.sleep(5)

# update data collect from openweathermap to firebase
def update_out_side():
    while True:
        response_from_url = requests.get('https://api.openweathermap.org/data/2.5/weather?id=1581130&appid=188c14a7e495bef60410a28dbdfa5ab8&units=metric')
        data_collect = response_from_url.json()
        temperature_out_side = data_collect['main']['temp']
        humidity_out_side = data_collect['main']['humidity']
        print('Temperature out side: ', temperature_out_side)
        print('Humidity out side: ', humidity_out_side)
        users_ref = ref.child('Out Side')
        users_ref.set({
        'Temperature': temperature_out_side ,
        'Humidity': humidity_out_side
        })
        time.sleep(10)

if __name__ == "__main__":
    thread_in_home = Thread(target = update_in_home, args = ())
    thread_out_side = Thread(target = update_out_side, args = ())
    thread_in_home.start()
    thread_out_side.start()
