import sys

# This function converts the airfoil string coordinates it receives from airfoil file to float numbers.
# However, some restrictions are provided in airfoil text file:
# Airfoil coordinates begin from trailing edge coordinates and goes to upper side, then come back to lower side.
def airfoil_coordinates(filename):
	filehandle = open(str(filename),"r")
	try:
		filehandle = open(str(filename),"r")
	except FileNotFoundError:
		print("Error: File cannot be found!")
		sys.exit()


	# Airfoil coordinates read from airfoil text file and store in airfoil_data list.
	airfoil_data = []
	for line in filehandle:
		if line[0] == 	" ":  	
			line = line.strip()
		if line[-1] == "\n":
			line = line.rstrip()

		airfoil_data.append(line)

	# Airfoil coordinates convert string to float numbers.
	coordinates = []
	for string in airfoil_data:
		string = string.split()	
		try:
			coordinates.append([float(string[0]),float(string[1])])
		except ValueError:
			pass	
	return coordinates

# This function is to find camberline coordinates.
# The method for finding camberline:
# Upper airfoil coordinates added lower airfoil coordinates then divided by two.
def airfoil_camberline_coordinates(filename):
	coordinates = airfoil_coordinates(str(filename))
	airfoil_x = []
	airfoil_y = []
    
	for i in coordinates:
		airfoil_x.append(i[0])
		airfoil_y.append(i[1])

	camberline_x = []
	camberline_y = []
	i = 0
	while True:
		camberline_x.append((airfoil_x[i] + airfoil_x[-i-1]) / 2)
		camberline_y.append((airfoil_y[i] + airfoil_y[-i-1]) / 2)
		
		if airfoil_x[i] == 0 and airfoil_y[i] == 0:
			break
		i = i + 1
	

	return (camberline_x,camberline_y, airfoil_x, airfoil_y)