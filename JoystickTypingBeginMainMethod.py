
import serial
serPort = serial.Serial('/dev/cu.usbmodem1421')  # open serial port


quadA = ['g','f','e','a','b','c','d','0','1']
quadB = ['n','m','l','h','i','j','k','2','3']
quadC = ['u','t','s','o','p','q','r','4','5']
quadD = ['z','v','w','x','y','6','7','8','9']

xDisp = 7
yDisp = -4

def main() :

	#######################################
	XYcoordSTR = serPort.readline()		  # This code segment reads and parses
	XYcoord = XYcoordSTR.split(",")		  # joystick coordinates from the Arduino.
	xDisp = int(XYcoord[0])				  # Will be needed in a few places throughout.
	yDisp = int(XYcoord[1]) 		  	  #
	#######################################

	while (isMovingJoystick( xDisp , yDisp ) == False) :
		#######################################
		XYcoordSTR = serPort.readline()		  # This code segment reads and parses
		XYcoord = XYcoordSTR.split(",")		  # joystick coordinates from the Arduino.
		xDisp = int(XYcoord[0])				  # Will be needed in a few places throughout.
		yDisp = int(XYcoord[1])			  	  #
		#######################################

		if (isMovingJoystick( xDisp , yDisp ) == True):
			displacementValue(xDisp, yDisp)


def letterPrinter() :
	initalQuad = getQuadrant( xDisp , yDisp )
	print initalQuad


# This def will determine if the 
# joystick is at the origin.
# Will return FALSE IF AT ORIGIN
def isMovingJoystick( x , y ) :

	if x is 0 and y is 0 :
		return False
	else :
		return True

# This def will isolate and compute 
# the current slope of the line
# from the joystick to the center.
def getSlope( x , y ) :
	if x == 0 :
		return -123.0							# This line if for the special case x == 0 in which case return value in quadA and quadB
	return float(y) / float(x) 

# This def will determine the 
# current location (quadrant) of
# the joystick.
# Returns char A, B, C, or D
def getQuadrant( x , y ) :
	m = getSlope( x, y )

	# If in quadrant B
	if x > 0 and (m <= 1 and m >= -1) :
		return 'B' 

	# If in quadrant D
	elif x < 0 and (m <= 1 and m >= -1) :
		return 'D'

	# If in quadrant A
	elif y > 0 and (m > 1 or m < -1) :
		return 'A'

	# If in quadrantC
	elif y < 0 and (m > 1 or m < -1) :			# Could be removed
		return 'C'		

# This def will return either a value between -4 and 4
# If return > 0, move up the list to higher index element (rotate clockwise)
# If return < 0, move down the list to lower index element (rotate counterclockwise)
# If 0, joystick returned to origin (letter done)
def displacementValue( x , y ) :

	listPlace = 0;
	currentQuad = getQuadrant( x , y )
	newQuad = currentQuad

	print "Initial quadrant = " + currentQuad

	while (currentQuad is 'A' or currentQuad is 'B' or currentQuad is 'C' or currentQuad is 'D') :

		#######################################
		XYcoordSTR = serPort.readline()		  # This code segment reads and parses
		XYcoord = XYcoordSTR.split(",")		  # joystick coordinates from the Arduino.
		x = int(XYcoord[0])				  # Will be needed in a few places throughout.
		y = int(XYcoord[1])			  	  #
		#######################################
		newQuad = getQuadrant( x , y )

		if currentQuad is None or newQuad is None :
			print ""
		else : 
			print "currentQuad = " + currentQuad
			print "newQuad = " + newQuad
			print listPlace


		if currentQuad == newQuad :
			listPlace += 0

		elif currentQuad is 'B' :
			if newQuad is 'A' :
				listPlace -= 1
			if newQuad is 'C' :
				listPlace += 1

		elif currentQuad is 'D' :
			if newQuad is 'C' :
				listPlace -= 1
			if newQuad is 'A' :
				listPlace += 1

		elif currentQuad is 'A' :
			if newQuad is 'D' :
				listPlace -= 1
			if newQuad is 'B' :
				listPlace += 1

		elif currentQuad is 'C' :
			if newQuad is 'B' :
				listPlace -= 1
			if newQuad is 'D' :
				listPlace += 1

		currentQuad = newQuad

	print "End Loop"
	return listPlace


if __name__ == '__main__' : main()
