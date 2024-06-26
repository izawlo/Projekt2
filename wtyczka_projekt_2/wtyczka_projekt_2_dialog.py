# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WtyczkaProjekt2Dialog
                                 A QGIS plugin
 Wtyczka robi podstawowe operacje na punktach (np. liczy rónice wysokości, liczy pole powierzchni). 
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Alicja Wołosiewicz, Izabela Włodarczyk
        email                : 01179247@pw.edu.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from math import atan2, sqrt, pi
from qgis.utils import iface

from qgis.PyQt import QtWidgets, uic
from qgis.core import QgsField, QgsFeature, QgsGeometry, QgsVectorLayer, QgsPointXY, QgsProject, QgsCoordinateReferenceSystem, QgsFields
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'wtyczka_projekt_2_dialog_base.ui'))
    

class WtyczkaProjekt2Dialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(WtyczkaProjekt2Dialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.roznica_wysokosci.clicked.connect(self.roznica_wyskosci_funkcja)
        self.zlicz_punkty.clicked.connect(self.licz_elementy)
        self.wyswietlanie_wspolrzednych.clicked.connect(self.wspolrzedne_funkcja)
        self.pole_powierzchni.clicked.connect(self.pole_powierzchni_funkcja)
        self.wyczyszczenie_tablicy.clicked.connect(self.wyczyszczenie_tablicy_funkcja)
        self.przycisk_zamkniecia.clicked.connect(self.wyczyszczenie_danych_funkcja)
        self.azymut.clicked.connect(self.azymut_funkcja)
        self.dlugosc_odcinka.clicked.connect(self.dlugosc_odcinka_funkcja)
        self.resetuj_wszystko.clicked.connect(self.wyczyszczenie_danych_funkcja)
        self.zapisanie_pliku.clicked.connect(self.zapisanie_pliku_funkcja)
        self.azymut_odwrotny.clicked.connect(self.azymut_funkcja)
        self.wczytaj_plik.clicked.connect(self.wybierz_plik_funkcja)
        #self.wybor_pliku.fileChanged.connect(self.wybranie_pliku_funkcja)
    
    def dlugosc_odcinka_funkcja(self):
        liczba_elementów = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        if liczba_elementów == 2:
            wybrane_elementy = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures() 
            K=[]
            for element in wybrane_elementy:
                wsp = element.geometry().asPoint()
                X = wsp.x()
                Y = wsp.y()
                K.append([X, Y])
            odl=sqrt((K[0][0]-K[1][0])**2+(K[0][1]-K[1][1])**2)
            self.dlugosc_odcinka_wynik.setText(f'Odległosć pomiędzy punktami (punkt id:1- id:2) wynosi: {odl:.3f} [m]')
        elif liczba_elementów < 2:
            self.dlugosc_odcinka_wynik.setText("Błąd")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za mało punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
        elif liczba_elementów > 2:
            self.dlugosc_odcinka_wynik.setText("Błąd")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za dużo punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
                
    def get_kat(self, p, punkt_1):
        dx = p[0] - punkt_1[0]
        dy = p[1] - punkt_1[1]
        kat = atan2(dy, dx)  
        return kat

    def sortuj_punkty(self, K):
        punkt_1 = [sum(p[0] for p in K) / len(K), sum(p[1] for p in K) / len(K)]
        posortowane_punkty = sorted(K, key=lambda p: self.get_kat( p,  punkt_1))
        return posortowane_punkty
           
    def azymut_funkcja(self):
        liczba_elementów = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        if liczba_elementów == 2:
            wybrane_elementy = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures() 
            K=[]
            for element in wybrane_elementy:
                wsp = element.geometry().asPoint()
                X = wsp.x()
                Y = wsp.y()
                K.append([X, Y])
            Az = atan2((K[1][1]-K[0][1]), (K[1][0]-K[0][0]))
            if 'stopnie_dziesietne' == self.jednostka_azymut.currentText():
                Az =Az*180/pi
                if Az < 0:
                    Az += 360
                elif Az > 360:
                    Az -= 360
                self.azymut_wynik.setText(f'Azymut wynosi (punkt id:1- id:2): {Az:.7f}[stopnie_dziesietne]')
                Az_odw = Az+180
                if Az_odw < 0:
                    Az_odw += 360
                elif Az_odw > 360:
                    Az_odw -= 360
                self.azymut_odwrotny_wynik.setText(f'Azymut odwrotny wynosi (punkt id:2- id:1): {Az_odw:.7f}[stopnie_dziesietne]')
            elif 'grady' == self.jednostka_azymut.currentText():
                Az =Az*200/pi
                if Az < 0:
                    Az += 400
                elif Az > 400:
                    Az -= 400
                self.azymut_wynik.setText(f'Azymut wynosi (punkt id:1- id:2): {Az:.4f}[grady]')
                Az_odw = Az+200
                if Az_odw < 0:
                    Az_odw += 400
                elif Az_odw > 400:
                    Az_odw -= 400
                self.azymut_odwrotny_wynik.setText(f'Azymut odwrotny wynosi (punkt id:2- id:1): {Az_odw:.4f}[grady]')
        elif liczba_elementów < 2:
            self.azymut_wynik.setText("Błąd")
            self.azymut_odwrotny_wynik.setText("Błąd")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za mało punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
        elif liczba_elementów > 2:
            self.azymut_wynik.setText("Błąd")
            self.azymut_odwrotny_wynik.setText("Błąd")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za dużo punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
            
            
            
    def licz_elementy(self):
        liczba_elementów = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        self.pokaz_ilosc_punktow.setText(str(liczba_elementów))
        
    def wspolrzedne_funkcja(self):
        wybrane_elementy = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
        K = []
        iden = 0
        for element in wybrane_elementy:
            wsp = element.geometry().asPoint()
            X = wsp.x()
            Y = wsp.y()
            K.append([X, Y])
            iden += 1
            self.wspolrzedne.append(f'Kordynaty punktu {iden}: X = {X:.3f}, Y = {Y:.3f}')
            
    def roznica_wyskosci_funkcja(self):
        liczba_elementów = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        K=[]
        if liczba_elementów == 2: 
            wyb_war = iface.activeLayer()
            wybrane = wyb_war.selectedFeatures()
            for i in wybrane:
                K.append(i['wysokosc'])
            roznica_wysokosci=float(K[1])-float(K[0])
            self.roznica_wysokosci_wynik.setText(f'Róznica wysokosci wynosi (punkt id:1- id:2): {roznica_wysokosci:.3f}[m]')
        elif liczba_elementów < 2:
            self.roznica_wysokosci_wynik.setText("Błąd")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za mało punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
        elif liczba_elementów > 2:
            self.roznica_wysokosci_wynik.setText("Błąd")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za dużo punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
            
            
    def pole_powierzchni_funkcja(self):
        liczba_elementów = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
        if liczba_elementów >= 3:
            wybrane_elementy = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
            K = []
            iden = 0
            for element in wybrane_elementy:
                wsp = element.geometry().asPoint()
                X = wsp.x()
                Y = wsp.y()
                K.append([X, Y])
            K = self.sortuj_punkty(K)
            suma=0
            for i in range(len(K)):
                if i<len(K)-1:
                    P=(K[i][0]*(K[i+1][1]-K[i-1][1]))
                    print(P)
                    suma += P
            P=(K[-1][0]*(K[0][1]-K[-2][1]))
            suma += P
            suma=0.5*abs(suma)   
            if 'metry2' == self.jednostka_pole.currentText():
                self.pole_powierzchni_wynik.setText(f'Pole powierzchni wynosi: {suma:.3f}[m^2]')
            elif 'ary' == self.jednostka_pole.currentText():
                suma=suma/100
                self.pole_powierzchni_wynik.setText(f'Pole powierzchni wynosi: {suma:.3f}[a]')
            elif 'hektary' == self.jednostka_pole.currentText():
                suma=suma/10000
                self.pole_powierzchni_wynik.setText(f'Pole powierzchni wynosi: {suma:.5f}[ha]')
                
            if 'Tak' == self.poligon_wybor.currentText():
                warstaw_poligon = QgsVectorLayer('Polygon?crs=EPSG:2180', 'poligion_obliczonego_pola', 'memory')
                warstaw_poligon.startEditing()
                
                pole = QgsField("Area", QVariant.Double)
                warstaw_poligon.addAttribute(pole)

                poligon = QgsGeometry.fromPolygonXY([[QgsPointXY(point[0], point[1]) for point in K]])
                
                area = poligon.area()
                atrybut = [area]
                
                funkcja = QgsFeature()
                funkcja.setGeometry(poligon)
                funkcja.setAttributes(atrybut)
                warstaw_poligon.addFeature(funkcja)
                
                warstaw_poligon.commitChanges()
                warstaw_poligon.updateExtents()
                QgsProject.instance().addMapLayer(warstaw_poligon)
                
        elif liczba_elementów < 3:
            self.pole_powierzchni_wynik.setText("Bład")
            okienko = QMessageBox()
            okienko.setIcon(QMessageBox.Critical)
            okienko.setText("Wybrano za mało punktów")
            okienko.setInformativeText("")
            okienko.setWindowTitle("Błąd")
            okienko.exec_()
            
    def wyczyszczenie_tablicy_funkcja(self):
        self.wspolrzedne.clear()
        
    def wyczyszczenie_danych_funkcja(self):
        self.wspolrzedne.clear()
        self.pole_powierzchni_wynik.clear()
        self.roznica_wysokosci_wynik.clear()
        self.pokaz_ilosc_punktow.clear()
        self.azymut_odwrotny_wynik.clear()
        self.azymut_wynik.clear()
        self.dlugosc_odcinka_wynik.clear()
    
    
    def wybierz_plik_funkcja(self):
        sciezka = self.wybor_pliku.filePath()
        koordynaty = []
        with open(sciezka, 'r') as plik:
            for wiersz in plik:
                wiersz = wiersz.strip()
                oddzielenie = wiersz.split(";")
                x = float(oddzielenie[0])
                y = float(oddzielenie[1])
                z = float(oddzielenie[2])
                koordynaty.append([x, y, z])

        nazwa_warstwy = 'Wczytane punkty'
        crs = QgsCoordinateReferenceSystem('EPSG:2180')
        warstwa = QgsVectorLayer('Point?crs=' + crs.authid(), nazwa_warstwy, 'memory')
    
        provider = warstwa.dataProvider()
        provider.addAttributes([QgsField('X', QVariant.Double),
                                QgsField('Y', QVariant.Double),
                                QgsField('h', QVariant.Double)])
        warstwa.updateFields()
    
        cechy = []
        for koordynaty_punkt in koordynaty:
            punkt = QgsPointXY(koordynaty_punkt[0], koordynaty_punkt[1])
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPointXY(punkt))
            feature.setAttributes([koordynaty_punkt[0], koordynaty_punkt[1], koordynaty_punkt[2]])
            cechy.append(feature)
    
        provider.addFeatures(cechy)
        warstwa.updateExtents()
    
        QgsProject.instance().addMapLayer(warstwa)
        
        layer_name = "Wczytane punkty"
        project = QgsProject.instance()
        
        while len(project.mapLayersByName(layer_name)) > 1:
            project.removeMapLayer(project.mapLayersByName(layer_name)[0])
        
    def zapisanie_pliku_funkcja(self):
        '''
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "Plik_wynikowy_wtyczki_AW_IW.txt")
        '''
        
        with open("Plik_wynikowy_wtyczki_AM_DJ.txt", "w") as plik:
            wybrane_elementy = self.mMapLayerComboBox_layers.currentLayer().selectedFeatures()
            punkty_ilosc=len(wybrane_elementy)
            plik.write(f'liczba wybranych punktów: {punkty_ilosc}\n')
            K = []
            iden = 0
            for element in wybrane_elementy:
                wsp = element.geometry().asPoint()
                X = wsp.x()
                Y = wsp.y()
                K.append([X, Y])
                iden += 1
                plik.write(f"Współrzędne punktu numer {iden}: X = {X:.3f}, Y = {Y:.3f}\n")
                
            liczba_elementów = len(self.mMapLayerComboBox_layers.currentLayer().selectedFeatures())
            if liczba_elementów == 2:
                Az = atan2((K[1][1]-K[0][1]), (K[1][0]-K[0][0]))
                if 'stopnie_dziesietne' == self.jednostka_azymut.currentText():
                    Az =Az*180/pi
                    if Az < 0:
                        Az += 360
                    elif Az > 360:
                        Az -= 360
                    Az_odw = Az+180
                    if Az_odw < 0:
                        Az_odw += 360
                    elif Az_odw > 360:
                        Az_odw -= 360
                    plik.write(f"Azymut wynosi (punkt id:1- id:2): {Az:.7f}[stopnie dziesiętne]\n")
                    plik.write(f"Azymut odwrotny wynosi(punkt id:2- id:1): {Az_odw:.7f}[stopnie dziesiętne]\n")
                elif 'grady' == self.jednostka_azymut.currentText():
                    Az =Az*200/pi
                    if Az < 0:
                        Az += 400
                    elif Az > 400:
                        Az -= 400
                    Az_odw = Az+200
                    if Az_odw < 0:
                        Az_odw += 400
                    elif Az_odw > 400:
                        Az_odw -= 400
                    plik.write(f"Azymut wynosi(punkt id:1- id:2): {Az:.4f}[grady]\n")
                    plik.write(f"Azymut odwrotny wynosi(punkt id:2- id:1): {Az_odw:.4f}[grady]\n")
                odl=sqrt((K[0][0]-K[1][0])**2+(K[0][1]-K[1][1])**2)
                plik.write(f'Odległosć miedzy punktami (punkt id:1- id:2) wynosi: {odl:.3f} [m] \n')
                wyb_war = iface.activeLayer()
                wybrane = wyb_war.selectedFeatures()
                L=[]
                for i in wybrane:
                    L.append(i[2])
                roznica_wysokosci=L[1]-L[0]
                plik.write(f'Różnica wysokosci (punkt id:1- id:2): {roznica_wysokosci:.3f} [m]\n')
            elif liczba_elementów < 2:
                plik.write(f"Azymut wynosi: Wybrano za mało punktów\n ")
                plik.write(f"Odległosć miedzy punktami wynosi: Wybrano za mało punktów\n ")
                plik.write(f"Różnica wysokosci: Wybrano za mało punktów\n")
            elif liczba_elementów > 2:
                plik.write(f"Azymut wynosi: Wybrano za dużo punktów\n")
                plik.write(f"Odległosć miedzy punktami wynosi: Wybrano za dużo punktów\n")
                plik.write(f"Różnica wysokoci: Wybrano za dużo punktów\n")
            if liczba_elementów >=3:
                suma=0
                K = self.sortuj_punkty(K)
                for i in range(len(K)):
                    if i<len(K)-1:
                        P=(K[i][0]*(K[i+1][1]-K[i-1][1]))
                        print(P)
                        suma += P
                P=(K[-1][0]*(K[0][1]-K[-2][1]))
                suma += P
                suma=0.5*abs(suma)
                ary=suma/100
                ha=suma/10000
                plik.write(f'Pole wynosi: {suma:.3f} [m]\n')
                plik.write(f'Pole wynosi: {ary:.3f} [a]\n')
                plik.write(f'Pole wynosi: {ha:.3f} [ha]\n')
            else:
                plik.write(f"Pole wynosi: Wybrano za mało punktów\n")
            
