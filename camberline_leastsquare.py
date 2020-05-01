# This function calculate the camberline polynomial that can be any degree.
# Fitting curve method is least squares method.
from camberline_coordinates import airfoil_camberline_coordinates
import numpy



def find_coef_leastsquares(filename, degree):
    camberline_x, camberline_y, _, _ = airfoil_camberline_coordinates(filename)
    D = [[0 for _ in range(0,degree+1)] for _ in range(0,degree+1)]
    for i in range(0,degree+1):
        for j in range(0,degree+1):
            sum = 0
            for k in range(0,len(camberline_x)):
                sum += (camberline_x[k] ** j) * (camberline_x[k] ** i)
            D[i][j] = sum
    
    F = [0 for _ in range(degree+1)]
    for i in range(0,degree+1):
        sum = 0
        for j in range(0,len(camberline_x)):
            sum += camberline_y[j] * (camberline_x[j] ** i)
        F[i] = sum
    
    coef = [0 for _ in range(degree+1)]
    D = numpy.array(D)       
    F = numpy.array(F)
    coef = numpy.linalg.solve(D,F)
    
    sum = 0
    for i in coef:
        sum += i ** 2
    if sum < 10 ** (-15):
        coef = [0 for _ in range(degree+1)]    
    coef[0] = round(coef[0],5)
    coef[1] = round(coef[1],5)
    coef[2] = round(coef[2],5)
    coef[3] = round(coef[3],5)
    coef[4] = round(coef[4],5)
    return coef




def find_coordinates_camberline(filename,degree):
    coef = find_coef_leastsquares(filename,degree)
    camberline_x_leastsquares = list(numpy.arange(0,1,0.01))
    camberline_y_leastsquares = []
    for i in range(len(camberline_x_leastsquares)):
        sum = 0
        for j in range(0,len(coef)):
            sum += coef[j] * (camberline_x_leastsquares[i] ** j)         
        camberline_y_leastsquares.append(sum)
    return camberline_x_leastsquares, camberline_y_leastsquares