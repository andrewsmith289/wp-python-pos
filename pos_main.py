from SimpleCV import Color, Camera, Display
from Tkinter import *
from Scanner import Scanner
import RPi.GPIO as GPIO
from config import CONFIG


if __name__ == "__main__":
    cam = Camera()  # starts the camera
    display = Display(resolution=(300, 200))

    posSystem = Scanner(CONFIG)

    from pos_ui.frame_order import Frame_Order

    frame_order_info = Frame_Order(None, Tk())

    try:
        while display.isNotDone():
            img = cam.getImage()  # gets image from the camera
            barcode = img.findBarcode()  # finds barcode data from image

            if barcode is not None:  # if there is some data processed
                posSystem.process_scan_event(str(barcode[0].data))
                barcode = []  # reset barcode data
            img.save(display)  # shows the image on the screen
    except (KeyboardInterrupt, SystemExit):
        print 'Received terminate signal from user or system.'
        print 'Cleaning up.'
        GPIO.cleanup()
