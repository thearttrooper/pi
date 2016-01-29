# weather.py
#
# Reads the Pi weather board status:
#
# * Temperature (board and sensor 1)
# * Humidity
# * Pressure
#
# and tweets the results.
#
# Requires Python 3.x.
#
# Copyright 2014 Chris Trueman.
#

import configparser
import smbus
import time
from twython import Twython, TwythonError

# Weather board data.
ADDRESS = 0x4E
BOARD_VERSION_PORT = 0x24
BOARD_TEMP_PORT = 0x42
HUMIDITY_PORT = 0x43
PRESSURE_PORT = 0x47
TEMP_SENSOR_1 = 0x45
TEMP_SENSOR_2 = 0x46

# Safety setttings
MAX_ATTEMPTS = 10

config = configparser.ConfigParser()

config.read('/home/pi/pd/py/weather/weather.cfg')

config_twitter = config['Twitter']
consumer_key = config_twitter.get('ConsumerKey', '')
consumer_secret = config_twitter.get('ConsumerSecret', '')
access_token_key = config_twitter.get('AccessTokenKey', '')
access_token_secret = config_twitter.get('AccessTokenSecret', '')
account_name = config_twitter.get('AccountName', '')
config_general = config['General']
exception_sleep_seconds = int(config_general.get('ExceptionSleepSeconds', 10))

bus = smbus.SMBus(0)

attempts = 0
tweeted = False

while not tweeted and attempts < MAX_ATTEMPTS:
    attempts += 1
    board_version = bus.read_byte_data(ADDRESS, BOARD_VERSION_PORT)
    board_temp = bus.read_byte_data(ADDRESS, BOARD_TEMP_PORT)
    humidity = bus.read_byte_data(ADDRESS, HUMIDITY_PORT)
    pressure = bus.read_byte_data(ADDRESS, PRESSURE_PORT)
    temp_1 = bus.read_byte_data(ADDRESS, TEMP_SENSOR_1)

    tweet = "{0} {1:.2f}C {2:.2f}C {3:.0f}% {4:.0f}kPa".format(
        time.ctime(),
        0.1 * temp_1,
        board_temp,
        humidity,
        pressure)

    try:
        twitter = Twython(
            consumer_key, 
            consumer_secret, 
            access_token_key, 
            access_token_secret)
            
        twitter.update_status(status=tweet)

        print(tweet)

        with open('weather.log', 'a') as log:
            log.write(tweet);
            log.write('\n')

        tweeted = True
    except TwythonError as e:
        print(e)
        time.sleep(exception_sleep_seconds)
