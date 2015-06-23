import RPi.GPIO as GPIO
import time

def updateTray(type, tray, forceClear = 0):
	pinTray = ledTrayTopBottom
	if type == 2:
		pinTray = ledTrayMiddle

	pinTrayIndex = -1
	for ledTray in tray:
		pinTrayIndex += 1
		pinIndex = -1
		for ledValue in ledTray:
			pinIndex += 1
			pin = pinTray[pinTrayIndex][pinIndex]
			value = ledValue
			if forceClear:
				value = 0
				
			GPIO.output(pin, value)
				
	return True

text = [#PIE
	[1,1,1,1,1],
	[0,0,1,0,1],
	[0,0,1,0,1],
	[0,0,0,1,0],
	[0,0,0,0,0],
	[0,0,0,0,0],
	[1,1,1,1,1],
	[0,0,0,0,0],
	[0,0,0,0,0],#
	[1,1,1,1,1],
	[1,0,1,0,1],
	[1,0,1,0,1],
	[1,0,0,0,1],
]

currentPins = [
	[17,18,21,16,20],
	[6,19,13,24,5],
	[22,26,23,27,12],
	[2,3,4,14,15]
]

ledTrayMiddle = currentPins[1:3]
ledTrayTopBottom = currentPins[0:1] + currentPins[3:4]

currentLeds = [
	[0,0,0,0,0],
	[0,0,0,0,0],
	[0,0,0,0,0],
	[0,0,0,0,0]
]

pinLines = 2
pinLinesTime = 0.01
animationNextTrayTime = 0.1

currentLedsTmp = currentLeds
textTray = currentLeds + text
textTrayLen = len(textTray) - 1

try:
	GPIO.setmode(GPIO.BCM)
	for pins in currentPins:
		for pin in pins:
			GPIO.setup(pin, GPIO.OUT)

	while True:
		textTrayFirst = textTray[0]
		textTray = textTray[1:] + [textTrayFirst]
	
		animationTrayTime = 0
		ledTextTrayTopBottom = textTray[0:1] + textTray[3:4]
		ledTextTrayMiddle = textTray[1:3]
		while animationTrayTime < animationNextTrayTime:
			animationTrayTime += pinLinesTime
			updateTray(2, ledTextTrayMiddle, 1)
			updateTray(1, ledTextTrayTopBottom)
			time.sleep(pinLinesTime)
			updateTray(1, ledTextTrayTopBottom, 1)
			updateTray(2, ledTextTrayMiddle)
			time.sleep(pinLinesTime)
finally:
	print('Clean up')
	for pins in currentPins:
		for pin in pins:
			GPIO.output(pin, 0)
		
	GPIO.cleanup()
