import serial
serPort = serial.Serial('/dev/cu.usbmodem1421')  # open serial port


quadUp  =   ['X','Y','C','N','E','A','R','W','V']
quadRight = ['Q','P','U','S',' ','O','D','F','K']
quadDown =  ['Z','B','M','H','T','I','L','G','J']
quadLeft =  ['%','@','!','?',chr(8),'.',',','#','/']

xDisp = 0
yDisp = 0


global fullString

def main() :

	#######################################
	XYcoordSTR = serPort.readline()		  # This code segment reads and parses
	XYcoord = XYcoordSTR.split(",")		  # joystick coordinates from the Arduino.
	xDisp = int(XYcoord[0])				  # Will be needed in a few places throughout.
	yDisp = int(XYcoord[1]) * -1	  	  #
	#######################################
	fullString = ""

	while (isMovingJoystick( xDisp , yDisp ) == False) :
		#######################################
		XYcoordSTR = serPort.readline()		  # This code segment reads and parses
		XYcoord = XYcoordSTR.split(",")		  # joystick coordinates from the Arduino.
		xDisp = int(XYcoord[0])				  # Will be needed in a few places throughout.
		yDisp = int(XYcoord[1])	* -1	  	  #
		#######################################

		if (isMovingJoystick( xDisp , yDisp ) == True):
			init = getQuadrant(xDisp , yDisp)
			fullString = letterSelect(init , fullString)

		xDisp = 0
		yDisp = 0


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
		return -123.0							# This line if for the special case x == 0 in which case return value in quadUp and quadRight
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
	elif y < 0 and (m > 1 or m < -1) :		
		return 'C'		

# This def will return either a value between -4 and 4
# If return > 0, move up the list to higher index element (rotate clockwise)
# If return < 0, move down the list to lower index element (rotate counterclockwise)
# If 0, joystick returned to origin (letter done)
def displacementValue( x , y, initalZone ) :

	listPlace = 0;
	currentQuad = initalZone
	newQuad = initalZone

	while (currentQuad is 'A' or currentQuad is 'B' or currentQuad is 'C' or currentQuad is 'D') :

		#######################################
		XYcoordSTR = serPort.readline()		  # This code segment reads and parses
		XYcoord = XYcoordSTR.split(",")		  # joystick coordinates from the Arduino.
		x = int(XYcoord[0])				  	  # Will be needed in a few places throughout.
		y = int(XYcoord[1])	* -1		  	  #
		#######################################
		newQuad = getQuadrant( x , y )

		if currentQuad is None or newQuad is None :
			doNothing = -1

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

	return listPlace

def letterSelect( initalArea , currStr ):
	entryQuadrant = initalArea
	listDisplacement = displacementValue( xDisp , yDisp, entryQuadrant )

	if entryQuadrant is 'B':
		print quadRight[4 + listDisplacement],
		# currStr = currStr + quadRight[4 + listDisplacement]
	elif entryQuadrant is 'D':
		print quadLeft[4 + listDisplacement],
		# if(listDisplacement == 0):
		# 	currStr = currStr[:-1]
		# else:
		# 	currStr = currStr + quadLeft[4 + listDisplacement]
	elif entryQuadrant is 'A':
		print quadUp[4 + listDisplacement],
		# currStr = currStr + quadUp[4 + listDisplacement]
	elif entryQuadrant is 'C':
		print quadDown[4 + listDisplacement],
		# currStr = currStr + quadDown[4 + listDisplacement]	

	# print('\n' * 5) # a quick hack for now
	# print(currStr)
	return currStr


if __name__ == '__main__' : main()
