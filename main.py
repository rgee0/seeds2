import picamera
import io
import os
import sys
import time
import tweepy

from config import config
from PIL import Image, ImageFont, ImageDraw
from tweeter import Tweeter
from smbus import SMBus
from bme280 import BME280
from datetime import datetime

def read_image():
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.vflip = config["camera"]["verticalflip"]
        camera.hflip = config["camera"]["horizontalflip"]
        camera.resolution = (config["camera"]["width"], config["camera"]["height"])
        # Camera warm-up time
        time.sleep(config["camera"]["preview_time"])
        camera.capture(stream, format=config["camera"]["encoding"], quality=config["camera"]["image_quality"])
    return stream

def watermark(filename, msg):
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('roboto/Roboto-Regular.ttf', config["text"]["size"])
    draw.text((10, 10), msg, config["text"]["colour"], font=font)
    img.save(filename) 

def formatEnv(temp, pressure, humid):
    degree_symbol=u"\u00b0"
    return "Current environmental readings:\n Temperature: {:05.2f}{}C \n Pressure: {:05.2f}hPa \n Humidity: {:05.2f}% \n".format(temperature, degree_symbol, pressure, humidity)

if(__name__=="__main__"):

    #need to check that the target iamge path exists
    if not os.path.exists(config["camera"]["image_directory"]):
        pwd=os.getcwd()
        sys.exit("Error: Please ensure that " + pwd + config["camera"]["image_directory"][1:] + " exists.")

    # Initialise the BME280
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)
    for x in range(2):
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        time.sleep(2)

    stream = read_image()
    
    #use unix timestamp for filename to ease sorting in case timelapse is also enabled
    filename = config["camera"]["image_directory"] + str(int(time.time())) + "." + config["camera"]["encoding"]
    with open(filename, 'wb') as file:
        file.write(stream.getvalue())
    if config["text"]["enabled"] == True:
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M")
        watermark(filename, "{} Date: {}\n".format(formatEnv(temperature, pressure, humidity), date_time))

    
    if config["twitter"]["enabled"] == True:
        msg = formatEnv(temperature, pressure, humidity) + config["twitter"]["message"]
        tweeter = Tweeter(config["twitter"], tweepy)
        tweeter.send(filename, msg)

    #if we arent timelapsing no need to keep the file
    if config["timelapse"] != True:
        os.remove(filename)