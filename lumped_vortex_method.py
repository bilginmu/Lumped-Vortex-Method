from camberline_coordinates import airfoil_camberline_coordinates
from camberline_leastsquare import find_coef_leastsquares, find_coordinates_camberline
from math import cos, sin,pi,sqrt
import numpy

'''Kümelenmiş Girdaplar Yöntemi
 * Toplamda kamburluk eğrisinde bulunan noktaların 1 eksiği kadar panel yerleştirilmiştir.
 * Kamburluk eğrisinde 100 tane nokta seçilmiştir. 100 noktaya karşılık 99 panel konulmuştur.
 * Kümelenmiş girdaplar yöntemi yapılırken İnce Profiller için Sayısal Hesaplamalar(M. Adil Yükselen) pseudocode'u kullanılmıştır.
 * Bu dosya içerisinde moment katsayısı:            @refmoment
 *                     moment katsayısı dağılımı:   @refmomdağılım
 *                     taşıma katsayısı:            @reftaşıma
 *                     taşıma katsayısı dağılımı:   @reftaşdağılım
 * bulunmuştur. @ref*** dosyanın içerisinde aratılarak istenen fonksiyonlara ulaşılabilir.
'''
def lumped_vortex(filename,alpha):   
    camberline_x, camberline_y = find_coordinates_camberline(filename,4)

    d_x = []        # Panelin x uzunluğu
    d_y = []        # Panelin y uzunluğu
    x_v = []        # Panel üzerindeki girdabın x konumu
    y_v = []        # Panel üzerindeki girdabın y konumu
    x_c = []        # Panel üzerindeki kontrol noktasının x konumu
    y_c = []        # Panel üzerindeki kontrol noktasının y konumu
                    # ar = R 
    a = []          # a katsayılar matrisi 
    R = []          # R sonuçların bulunduğu dizi
    theta = []      # Her panelin x ekseni ile yaptığı açı
    V_infinite = 1  # Serbest akım hızı

    for i in range(0,len(camberline_x)-1):
        
        d_x.append(camberline_x[i+1] - camberline_x[i])
        d_y.append(camberline_y[i+1] - camberline_y[i])
        x_v.append(camberline_x[i] + (camberline_x[i+1] - camberline_x[i])/4) 
        y_v.append(camberline_y[i] + (camberline_y[i+1] - camberline_y[i])/4)
        x_c.append(camberline_x[i] + 3*(camberline_x[i+1] - camberline_x[i])/4)
        y_c.append(camberline_y[i] + 3*(camberline_y[i+1] - camberline_y[i])/4)
    
    for i in range(0, len(x_c)):
        theta.append((y_c[i] - y_v[i])/(x_c[i] - x_v[i]))
    theta = numpy.arctan(theta)
    
    for i in range(0,len(x_v)):
        a.append([])
        for j in range(0,len(x_v)):
            delta_x = x_c[i] - x_v[j]
            delta_y = y_c[i] - y_v[j]
            r_2 = delta_x*delta_x + delta_y*delta_y
            a[i].append(1/(2*pi*r_2) * (delta_y * sin(theta[i]) + delta_x * cos(theta[i])))
        R.append(V_infinite * (cos(alpha) * sin(theta[i]) - sin(alpha) * cos(theta[i])))
    
    for i in range(len(R)):
        R[i] = -R[i]

    gama_r = numpy.linalg.solve(a,R)
    vortex_mag = []

    for i in range(0,len(gama_r)):
        vortex_mag.append(gama_r[i]/sqrt(d_x[i]**2 + d_y[i]**2))
    return vortex_mag, gama_r, x_v
    



# Taşıma katsayısı: @reftaşıma
def lift_coefficient(filename,alpha):
    _,gama_r,_ = lumped_vortex(filename,alpha)
    rho = 1.223 
    V_infinite = 1 
    L = 0

    for i in range(len(gama_r)):
        L += rho * V_infinite * gama_r[i]
    CL = L / (1/2 * rho * (V_infinite**2))
    return CL



# Taşıma dağılımı: @reftaşdağılım
def lift_coefficient_distribution(filename):
    alpha = [-2,0,2,4,6,8,10,12,14]
    for i in range(len(alpha)):
        alpha[i] = alpha[i] * pi /180
    
    CL = []
    for i in alpha:
        CL.append(lift_coefficient(filename,i))
    alpha = [-2,0,2,4,6,8,10,12,14]
    return alpha, CL



# Moment katsayısı :@refmoment
def moment_coefficient(filename,alpha):
    _, gama_r, x_v = lumped_vortex(filename,alpha)
    
    cm_0 = 0
    cm_ac = 0 
    V_infinite = 1
    for i in range(len(gama_r)):
        cm_0 += 2 * cos(alpha)/(V_infinite * 1) * gama_r[i] * x_v[i] 
        cm_ac += 2 * cos(alpha)/(V_infinite) * gama_r[i] * (x_v[i]-1/4)
    return -cm_ac, -cm_0



# Moment katsayısı dağılımı: @refmomdağılım
def moment_coefficient_distribution(filename):
    alpha = [0,2,4,6,8,10]
    cm_ac = []
    for i in range(len(alpha)):
        alpha[i] = alpha[i] * pi /180

    for i in alpha:
        temp,_ = moment_coefficient(filename,i)
        cm_ac.append(temp)
    alpha = [0,2,4,6,8,10]
    return alpha, cm_ac
