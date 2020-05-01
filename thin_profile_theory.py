import sys
sys.path.append("/home/mustafa/Desktop/Aerodinamik-Odev#3/modules")
import numpy
from math import pi, sin, cos
from camberline_leastsquare import find_coef_leastsquares

"""Klasik İnce Profil Teorisi
 * Bu dosyada içerisinde fourier katsayısları: @reffourier
 *                       taşıma katsayıları:   @reftaşıma
 *                       moment katsayıları:   @refmoment
 *                       girdap şiddetleri:    @refgirdap
 * bulunmuştur. @ref*** dosyanın içerisinde aratılarak istenen fonksiyonlara ulaşılabilir.
"""
# Fourier katsayıları: @reffourier
def fourier_coefficients(filename,degree,alpha):
    c = find_coef_leastsquares(filename,degree)   # Kamburluk eğrisi katsayılar matrisi
    A = []                                        # Fourier katsayıları
    b = []                                        # Katsayılar

    b.append(c[1] + c[2] + 9/8*c[3] + 5/4*c[4])
    b.append(-(c[2] + 3/2*c[3] + 15/8*c[4]))
    b.append(((3/8)*c[3] + (3/4)*c[4]))
    b.append(1/8*c[4])
   
    alpha = alpha * pi / 180
    A.append(alpha - b[0])
    A.append(b[1])
    A.append(b[2])
    A.append(b[3])
    return A


# Taşıma katsayıları: @reftaşıma
def lift_coefficients(filename):
    #alpha = list(range(0,15))      
    alpha = [-2, 0, 2, 4, 6, 8, 10, 12 ]
    CL = [0 for _ in range(len(alpha))]
    for i in range(len(alpha)):
        A = fourier_coefficients(filename,4,alpha[i])
        CL[i] = 2 * pi * (A[0] + A[1]/2) 
    CL[0] = round(CL[0],5)
    return alpha,CL


# Moment katsayıları: @refmoment
def moment_coefficients(filename,alpha):
    
    
    x = [-2,0,2,4,6,8,10]
    CM_ac = []
    for alpha in x:
        A = fourier_coefficients(filename,4,alpha)
        CM_ac.append(-pi/4 * (A[1] - A[2]))
    return x, CM_ac


# Girdap şiddetleri: @refgirdap
def vortex_mag(filename):
    A = fourier_coefficients(filename,4,4)
    theta = list(numpy.arange(0.13,pi,0.1))

    gama = [0 for _ in range(len(theta))]
    for i in range(len(theta)):
        gama[i] = 2 * 1 * (A[0] * (1+cos(theta[i]))/sin(theta[i]) + A[1]*sin(1*theta[i]) + A[2]*sin(2*theta[i]) +A[3]*sin(3*theta[i]))  
    x = []
   
    for i in theta:
        x.append(1/2*(1-cos(i)))
    return x, gama


