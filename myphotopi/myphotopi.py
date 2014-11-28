# myphotopi.py
#
# Copyright 2014 Chris Trueman.
#

from twython import Twython
import time
import picamera

CONSUMER_KEY = 'CONSUMER_KEY_GOES_HERE'
CONSUMER_SECRET = 'CONSUMER_SECRET_GOES_HERE'
ACCESS_TOKEN = 'ACCESS_TOKEN_GOES_HERE'
ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET_GOES_HERE'

while True:
    try:
        twitter = Twython(
            CONSUMER_KEY, 
            CONSUMER_SECRET, 
            ACCESS_TOKEN, 
            ACCESS_TOKEN_SECRET)

        # print twitter.verify_credentials()

        with picamera.PiCamera() as camera:
            camera.resolution = (800, 600)
            time.sleep(2)
            camera.capture('./status.jpg')
            image = open('./status.jpg', 'rb')
            text = time.ctime() + " " + "My view."
            twitter.update_status_with_media(status=text, media=image)

            with open('myphotopi.log', 'a') as log:
                log.write(text)
                log.write('\n')
    except:
        pass

    time.sleep(3600)
