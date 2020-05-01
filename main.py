import sys
#sys.path.append("/home/mustafa/Desktop/Aerodinamik-Odev#3/modules")
from math import pi, sqrt
from camberline_coordinates import airfoil_camberline_coordinates
from camberline_leastsquare import find_coordinates_camberline, find_coef_leastsquares
from thin_profile_theory import lift_coefficients, moment_coefficients,vortex_mag
from lumped_vortex_method import lumped_vortex, moment_coefficient_distribution, lift_coefficient_distribution, moment_coefficient, lift_coefficient
import os
import pyqtgraph
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout,QFrame, QTableWidget, QTableWidgetItem,QAbstractScrollArea
from PyQt5.QtWidgets import QMenuBar, qApp, QFileDialog, QLineEdit,QMessageBox


    
class WINDOW(QWidget):  
    alpha11 = [0,1,2,3,4,5,6,7,8,9,10]
    camberline_x, camberline_y, airfoil_x, airfoil_y = airfoil_camberline_coordinates("Airfoil/NACA-64-209.txt")
    camberline_x_leastsquare, camberline_y_leastsquare = find_coordinates_camberline("Airfoil/NACA-64-209.txt",4)
    alpha, CL = lift_coefficient_distribution("Airfoil/NACA-64-209.txt")
    c = find_coef_leastsquares("Airfoil/NACA-64-209.txt",4)
    gama_r1, gama_r,x_v = lumped_vortex("Airfoil/NACA-64-209.txt",4*pi/180)
    
    x_airfoil,gama = vortex_mag("Airfoil/NACA-64-209.txt")
    alpha1, CL1 = lift_coefficients("Airfoil/NACA-64-209.txt")
    alpha_cm_l, CM_ac = moment_coefficient_distribution("Airfoil/NACA-64-209.txt")
    alpha_cm_t,CM_ac1 = moment_coefficients("Airfoil/NACA-64-209.txt",4)

    def __init__(self):
        super().__init__()
        self.init_gui()
   

    def init_gui(self):   
        self.setWindowTitle("Aerodinamik Ödev 3 - İnce Profil Teorisi")
        self.setGeometry(0,0,1100,1000)
        self.tableCoordinate_setup()
        self.button_setup()
        self.label_setup()
        self.plot_setup()
        self.menubar_setup()
        self.show()

  
    
    def tableCoordinate_setup(self):
        self.coordinateTable = QTableWidget(self) 
        self.coordinateTable.setRowCount(len(self.airfoil_x))
        self.coordinateTable.setColumnCount(4)        
        self.coordinateTable.setColumnWidth(2,82)
        self.coordinateTable.setColumnWidth(3,82)
        self.tableUpdate()
    
    def tableUpdate(self):
        lAirfoilCoord = range(0,len(self.airfoil_x)-1)
        lCamberlineCoord = range(0,len(self.camberline_x)-1)
        
        self.coordinateTable.setItem(0,0,QTableWidgetItem('X-Profil'))
        self.coordinateTable.setItem(0,1,QTableWidgetItem('Y-Profil'))
        self.coordinateTable.setItem(0,2,QTableWidgetItem('X-Kambur'))
        self.coordinateTable.setItem(0,3,QTableWidgetItem('Y-Kambur'))
        self.coordinateTable.resizeColumnsToContents()
        for i in lAirfoilCoord:
            self.coordinateTable.setItem(i+1,0,QTableWidgetItem(str(self.airfoil_x[i]))) 
            self.coordinateTable.setItem(i+1,1,QTableWidgetItem(str(self.airfoil_y[i])))
        for i in lCamberlineCoord:     
            self.coordinateTable.setItem(i+1,2,QTableWidgetItem(str(self.camberline_x[i])))
            self.coordinateTable.setItem(i+1,3,QTableWidgetItem(str(self.camberline_y[i])))
        self.coordinateTable.setGeometry(0,130,330,300)

        

    def tableClear(self):
        self.coordinateTable.clear()

        

    
    def button_setup(self):
        button1 = QPushButton("Kanat Profili",self)
        button1.setGeometry(0,0,330,27)
        button1.clicked.connect(self.click_button1)

        button2 = QPushButton("Kamburluk Eğrisi",self)
        button2.setGeometry(0,25,330,27)
        button2.clicked.connect(self.click_button2)

        button3 = QPushButton("İnce Profil Teorisi ile Hesapla",self)
        button3.setGeometry(0,50,330,27)
        button3.clicked.connect(self.click_button3)

        button4 = QPushButton("Kümelenmiş Girdaplar Yöntemi ile Hesapla",self)
        button4.setGeometry(0,75,330,27)
        button4.clicked.connect(self.click_button4)

        button5 = QPushButton("Kamburluk Eğrisi Polinomu",self)
        button5.setGeometry(0,100,330,27)
        button5.clicked.connect(self.click_button5)
      
        button6 = QPushButton("Temizle",self)
        button6.setGeometry(0,125,330,27)
        button6.clicked.connect(self.click_button6)

    def click_button1(self):  
        self.plot1.plot(self.airfoil_x, self.airfoil_y,symbol='o',pen=pyqtgraph.mkPen('k',width=3))
        self.plot1.plot(self.camberline_x_leastsquare,self.camberline_y_leastsquare,pen=pyqtgraph.mkPen('k',width=3))
        self.label_update()
    def click_button2(self):
        self.plot3.plot(self.camberline_x,self.camberline_y,pen=pyqtgraph.mkPen('k',width=3))
        self.plot3.plot(self.camberline_x_leastsquare,self.camberline_y_leastsquare,pen=pyqtgraph.mkPen('r',width=3))
    def click_button3(self):
        self.plot2.plot(self.x_airfoil,self.gama,pen=pyqtgraph.mkPen('k',width=3))
        self.plot4.plot(self.alpha1, self.CL1, pen=pyqtgraph.mkPen('k',width=3))
        self.plot5.plot(self.alpha_cm_t, self.CM_ac1, pen=pyqtgraph.mkPen('k',width=3))
    def click_button4(self):
        self.plot4.plot(self.alpha, self.CL, pen=pyqtgraph.mkPen('r',width=3))
        self.plot2.plot(self.x_v,self.gama_r1,pen=pyqtgraph.mkPen('r',width=3))
        self.plot5.plot(self.alpha_cm_l, self.CM_ac, pen=pyqtgraph.mkPen('r',width=3))
    def click_button5(self):
        self.msgBox = QMessageBox(self)
        self.msgBox.setText("z = "+str(self.c[0])+" + "+str(self.c[1])+"x + "+"("+str(self.c[2])+")"+"x" +"² + " + str(self.c[3])+"x³ + "+"("+str(self.c[4])+")"+"x⁴" )
        self.msgBox.setGeometry(200,200,330,30)
        self.msgBox.exec()
    def click_button6(self):
        self.plot1.clear()
        self.plot2.clear()
        self.plot3.clear()
        self.plot4.clear()
        self.plot5.clear()
        self.label1.clear()
        self.label2.clear()
        self.label3.clear()
        self.label4.clear()
        self.label5.clear()
        self.label6.clear()
    


    def label_setup(self):
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label_update()


    def label_update(self):
        self.label1.setText("\tCₗ₀ = "+ str(self.CL1[1]))
        self.label1.setGeometry(0,450,330,20)
        self.label1.setStyleSheet("background-color:#ffeead;")
        self.label2.setText("\tCₘ_ac = "+str(self.CM_ac1[0]))
        self.label2.setGeometry(0,470,330,20)
        self.label2.setStyleSheet("background-color:#ffeead;")

        self.label3.setText("\tKlasik İnce Profil Teorisi")
        self.label3.setGeometry(0,430,330,20)
        self.label3.setStyleSheet("background-color:#ffeead;")

        self.label4.setText("\tKümelenmiş İnce Profil Teorisi")
        self.label4.setGeometry(0,490,330,20)
        self.label4.setStyleSheet("background-color:#ffeead;")

        self.label5.setText("\tCₗ₀ = "+ str(self.CL[1]))
        self.label5.setGeometry(0,510,330,20)
        self.label5.setStyleSheet("background-color:#ffeead;")

        self.label6.setText("\tCₘ_ac = "+str(self.CM_ac[0]))
        self.label6.setGeometry(0,530,330,20)
        self.label6.setStyleSheet("background-color:#ffeead;")



    
    def plot_setup(self):
        pyqtgraph.setConfigOption('background','w')
        pyqtgraph.setConfigOption('foreground','k')
        self.plot1 = pyqtgraph.PlotWidget(self,title="Kanat Profili")
        self.plot1.plotItem.showGrid(x=True,y=True,alpha=1)
        self.plot1.setGeometry(330,0,700,160)

        self.plot2 = pyqtgraph.PlotWidget(self,title="Girdap Şiddeti")
        self.plot2.plotItem.showGrid(x=True,y=True,alpha=2)
        self.plot2.setGeometry(330,162,700,270)

        self.plot3 = pyqtgraph.PlotWidget(self,title="Kamburluk Eğrisi")
        self.plot3.plotItem.showGrid(x=True,y=True,alpha=2)
        self.plot3.setGeometry(330,435,230,250)

        self.plot4 = pyqtgraph.PlotWidget(self,title="Taşıma Eğrisi")
        self.plot4.plotItem.showGrid(x=True,y=True,alpha=2)
        self.plot4.setGeometry(565,435,230,250)
        
        self.plot5 = pyqtgraph.PlotWidget(self,title="Moment Eğrisi")
        self.plot5.plotItem.showGrid(x=True,y=True,alpha=2)
        self.plot5.setGeometry(800,435,230,250)

        

    def menubar_setup(self):
        self.menubar = QMenuBar(self)
        actionFile1 = self.menubar.addMenu("Dosya")
        actionFile1.addAction("Yükle")
        actionFile1.addAction("Çıkış")
        actionFile1.triggered.connect(self.response)



    def response(self,action):
        if action.text() == "Çıkış":
            qApp.quit()
        else:
            self.filename = QFileDialog.getOpenFileName(self,"Dosya Aç",os.getenv("home"))
            self.camberline_x, self.camberline_y, self.airfoil_x, self.airfoil_y = airfoil_camberline_coordinates(self.filename[0])
            self.camberline_x_leastsquare, self.camberline_y_leastsquare = find_coordinates_camberline(self.filename[0],4)
            self.alpha, self.CL = lift_coefficient_distribution(self.filename[0])
            self.alpha1, self.CL1 = lift_coefficients(self.filename[0])
            self.alpha_cm_l, self.CM_ac =moment_coefficient_distribution(self.filename[0])
            self.alpha_cm_t,self.CM_ac1 = moment_coefficients(self.filename[0],4)
            self.x_airfoil,self.gama = vortex_mag(self.filename[0])
            self.c = find_coef_leastsquares(self.filename[0],4)
            self.gama_r1, self.gama_r, self.x_v = lumped_vortex(self.filename[0],4*pi/180)
            #self.click_button6()
            self.label_update()
            self.tableClear()
            self.tableUpdate()
            

app = QApplication(sys.argv)
window = WINDOW()
sys.exit(app.exec_())
