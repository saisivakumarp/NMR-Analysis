# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 09:59:42 2020

@aut(hor: saisi
"""

from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io_tecmag_file import*
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, width = 5, height = 4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.clear
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMR Analysis [copyright @sai siva kumar pinnepalli]")
        self.setWindowIcon(QIcon("icons/fid.png"))
        self.setGeometry(200, 100, 1600, 900)
        # self.setFixedSize(self.size())
        self.UI()
        self.show()
    
    def UI(self):
        self.widgets()
        self.layouts()
        
        
    def widgets(self):
        #Left Top Layout 1#
        self.leftLayout1Title = QLabel('Load files for analysis')
        self.loadedFilesDisplay = QListWidget()
        # self.loadedFilesDisplay.editItem()
        self.loadButton = QPushButton('Open Files')
        self.loadButton.clicked.connect(self.funcOpenFiles)
        self.analysisType = QComboBox()
        self.analysisType.addItems(['Single Pulse Experiment', 'CPMAS'])
        self.analysisButton = QPushButton('Analyze')
        self.analysisButton.clicked.connect(self.funcAnalyzeData)
        self.clearButton = QPushButton('Clear All')
        self.clearButton.clicked.connect(self.funcClearFiles)
        self.leftLayout1End = QLabel('______________________________________________')
        #Left Top Layout 2#
        self.leftLayout2Title = QLabel('Graph Parameters')
        self.nmrPlotTitle = QLineEdit()
        self.nmrPlotTitle.setPlaceholderText('Enter title')
        self.nmrPlotTitle.textChanged.connect(self.titleGetText)
        self.nmrPlotXLabel = QLineEdit()
        self.nmrPlotXLabel.setPlaceholderText('Default - ppm')
        self.nmrPlotXAxis = QComboBox()
        self.nmrPlotXAxis.addItems(['ppm', 'kHz', 'pts'])
        self.nmrPlotXAxis.currentTextChanged.connect(self.xAxisGetPlot)
        self.nmrPlotYLabel = QLineEdit()
        self.nmrPlotYLabel.setPlaceholderText('Deafault - arbitrary units')
        self.referenceValue = QLineEdit()
        self.referenceValue.setText('0')
        self.referenceValue.textChanged.connect(self.refGetValue)
        self.nmrShiftLeft = QSpinBox()
        self.nmrShiftLeft.setRange(0, 3000)
        self.nmrShiftLeft.valueChanged[int].connect(self.shiftLeftGetValue)
        self.nmrExpValue = QSpinBox()
        self.nmrExpValue.setRange(0, 100)
        self.nmrExpValue.valueChanged[int].connect(self.expGetValue)
        self.nmrBaseLine = QLineEdit()
        self.nmrBaseLine.setText('0.2')
        self.nmrBaseLine.textChanged.connect(self.baseLineGetValue)
        self.ph0Slider = QSlider(Qt.Horizontal)
        self.ph0Slider.setValue(0)
        self.ph0Slider.setMinimum(-360)
        self.ph0Slider.setMaximum(360)
        self.ph0Slider.setTickPosition(QSlider.TicksBelow)
        self.ph0Slider.setTickInterval(180)
        self.ph0Slider.valueChanged[int].connect(self.ph0GetValue)
        self.ph1Slider = QSlider(Qt.Horizontal)
        self.ph1Slider.setValue(0)
        self.ph1Slider.setMinimum(-360)
        self.ph1Slider.setMaximum(360)
        self.ph1Slider.setTickPosition(QSlider.TicksBelow)
        self.ph1Slider.setTickInterval(180)
        self.ph1Slider.valueChanged[int].connect(self.ph1GetValue)
        self.resetButton = QPushButton('Reset')
        self.resetButton.clicked.connect(self.funcResetAction)
        self.leftLayout2End = QLabel('______________________________________________')
        #Left Top Layout 3#
        self.leftLayout3Title = QLabel('Export Data')
        self.csvFormat = QRadioButton('*.csv')
        self.csvFormat.setChecked(True)
        self.textFormat = QRadioButton('*.txt')
        self.exportButton = QPushButton('Export data to CSV')
        self.exportButton.clicked.connect(self.funcExportData)
       
    def layouts(self):
        #Main Layouts#
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.leftLayout1Top = QVBoxLayout()
        self.leftLayout1 = QFormLayout()
        self.leftLayout1Frame = QFrame()
        self.leftLayout1Bottom = QVBoxLayout()
        self.leftLayout2Top = QVBoxLayout()
        self.leftLayout2 = QFormLayout()
        self.leftLayout2Bottom = QVBoxLayout()
        self.leftLayout2Frame = QFrame()
        self.leftLayout3Top = QVBoxLayout()
        self.leftLayout3 = QFormLayout()
        self.leftLayout3Bottom = QVBoxLayout()
        self.leftLayout3Frame = QFrame()
        
        #Left Top Layout 1#
        self.leftLayout1Top.addWidget(self.leftLayout1Title)
        self.leftLayout1Top.setAlignment(Qt.AlignLeft)
        self.leftLayout1.addRow(QLabel('Files:'), self.loadedFilesDisplay)
        self.leftLayout1.addRow(QLabel(''), self.loadButton)
        self.leftLayout1.addRow(QLabel('Analysis  :'), self.analysisType)
        self.leftLayout1.addRow(QLabel(''), self.analysisButton)
        self.leftLayout1.addRow(QLabel(''), self.clearButton)
        self.leftLayout1Frame.setLayout(self.leftLayout1)
        
        #Left Top Layout 2#
        self.leftLayout2Top.addWidget(self.leftLayout2Title)
        self.leftLayout2Top.setAlignment(Qt.AlignLeft)
        self.leftLayout2.addRow(QLabel('Title'), self.nmrPlotTitle)
        self.leftLayout2.addRow(QLabel('x axis'), self.nmrPlotXAxis)
        self.leftLayout2.addRow(QLabel('Ref (ppm):'), self.referenceValue)
        self.leftLayout2.addRow(QLabel('Shift left:'), self.nmrShiftLeft)
        self.leftLayout2.addRow(QLabel('Exponent:'), self.nmrExpValue)
        self.leftLayout2.addRow(QLabel('Baseline:'), self.nmrBaseLine)
        self.leftLayout2.addRow(QLabel('Ph0'), self.ph0Slider)
        self.leftLayout2.addRow(QLabel('Ph1:'), self.ph1Slider)
        self.leftLayout2.addRow(QLabel(''), self.resetButton)
        self.leftLayout2Bottom.addWidget(self.exportButton)
        self.leftLayout2Frame.setLayout(self.leftLayout2)


        #Assigning Layouts to MainLayout#
        self.mainLeftLayout.addLayout(self.leftLayout1Top,1)
        self.mainLeftLayout.addWidget(self.leftLayout1Frame, 40)
        self.mainLeftLayout.addLayout(self.leftLayout2Top,1)
        self.mainLeftLayout.addWidget(self.leftLayout2Frame, 60)
        self.mainLeftLayout.addLayout(self.leftLayout2Bottom,1) 
        self.mainLayout.addLayout(self.mainLeftLayout, 10)
        self.mainLayout.addLayout(self.mainRightLayout, 90)
        self.setLayout(self.mainLayout)
    
    def ph0GetValue(self):
        self.funcAnalyzeData()
        
    def ph1GetValue(self):
        self.funcAnalyzeData()
    
    def shiftLeftGetValue(self):
        self.funcAnalyzeData()
    
    def expGetValue(self):
        self.funcAnalyzeData()
        
    def xAxisGetPlot(self):
        self.funcAnalyzeData()
    
    def refGetValue(self):
        self.funcAnalyzeData()
    
    def titleGetText(self):
        self.funcAnalyzeData()
    
    def baseLineGetValue(self):
        self.funcAnalyzeData()
    
    def funcExportData(self):
        self.funcAnalyzeData()
        self.xDataFrame = pd.DataFrame(reversed(self.xaxis))
        self.yDataFrame = pd.DataFrame(self.nmrSpectrum)
        self.yDataFrameTransposed = self.yDataFrame.transpose()
        self.xyDataFrame = pd.concat([self.xDataFrame, self.yDataFrameTransposed], axis=1, sort=False)
        # print(self.xyDataFrame)
        self.xyDataFrameHeader = []
        for i in range(numberFID+1):
            if i ==0:
                headerText = 'X' + '(' + self.nmrPlotXAxis.currentText() + ')'
                self.xyDataFrameHeader.append(headerText)
            if i > 0:
                headerText = self.filesNames[i-1]
                self.xyDataFrameHeader.append(headerText)
        
        if self.csvFormat.isChecked():
            self.csvDataFileName, ok = QFileDialog.getSaveFileName(self, 'Save data', "", "CSV(*.csv)")
            if ok:
                self.xyDataFrame.to_csv(self.csvDataFileName, header=self.xyDataFrameHeader, index=False)
        # elif self.textFormat.isChecked():
        #     self.csvDataFileName, ok = QFileDialog.getSaveFileName(self, 'Save data', "", "text(*.txt)")
        #     if ok:
        #         self.xyDataFrame.to_csv(self.csvDataFileName)
            
    def funcResetAction(self):
        self.ph0Slider.setValue(0)
        self.ph1Slider.setValue(0)
        self.referenceValue.setText('0')
        self.nmrShiftLeft.setValue(0)
        self.nmrExpValue.setValue(0)
        self.nmrPlotTitle.clear()
        self.nmrBaseLine.setText('0.2')
    
    def funcOpenFiles(self):
        self.fileurl = QFileDialog.getOpenFileNames(self, "Select one or more files to open", "", "Tecmag NMR (*tnt)")
        self.filesURLList = []
        self.filesNames = []
        for list in self.fileurl[0]:
            self.filesURLList.append(list)
        for i in range(0,len(self.filesURLList)):
            file = os.path.basename(self.filesURLList[i])
            editedFile = file.split('.')[0]
            self.filesNames.append(str(editedFile))
        self.filesNames.reverse()
        self.loadedFilesDisplay.addItems(self.filesNames)
    
    def funcClearFiles(self):
        if self.loadedFilesDisplay.count() != 0:
            self.filesNames.clear()
            self.filesURLList.clear()
            self.loadedFilesDisplay.clear()
            if self.mainRightLayout.count() > 0:
                for i in reversed (range(self.mainRightLayout.count())):
                    self.mainRightLayout.takeAt(i).widget().deleteLater()
        else:
            QMessageBox.information(self, "Info", "No files to clear.")
            
    
    def funcAnalyzeData(self):
        if self.loadedFilesDisplay.count() != 0:
            if str(self.analysisType.currentText()) == 'Single Pulse Experiment':
                self.dataList = []
                self.dwellList = []
                self.obsFreqList = []
                for item in self.filesURLList:
                    [self.data, self.dwell, self.obsFreq]= read_tecmag_file(item)
                    self.dataList.append(self.data)
                    self.dwellList.append(self.dwell)
                    self.obsFreqList.append(self.obsFreq)
                self.nmrData = np.array(self.dataList)
                self.nmrDwell = np.array(self.dwellList)
                self.nmrObsFreq = np.array(self.obsFreqList)
                # print(self.nmrData)
                # print(self.nmrDwell)
                # print(self.nmrObsFreq)
                self.checkNmrData()
                self.processNmrData()
            if str(self.analysisType.currentText()) == 'CPMAS':
                QMessageBox.information(self, "Warning", "Functions for this analysis is not yet ready.")
        else:
            QMessageBox.information(self, "Warning", "Please load data files.")
    
    def checkNmrData(self):
        global spectrometerFreq
        global spectralWidth
        if len(self.obsFreqList)==(self.obsFreqList.count(self.obsFreqList[0])):
            spectrometerFreq = round(self.obsFreqList[0], 5)*1e6
            # print(spectrometerFreq)
            if len(self.dwellList)==(self.dwellList.count(self.dwellList[0])):
                spectralWidth = 1/self.dwellList[0]
                return True
            else:
                QMessageBox.information(self, "Warning", "Dwell times are not identical")
                return False
            return True
        else:
            QMessageBox.information(self, "Warning", "Spectrometer Frequencies are not identical")
            return False
        
    def processNmrData(self):
        global numberFID
        global numberAcqPoints
        global pivot
        [numberFID, numberAcqPoints] = self.nmrData.shape
        pivot = round(numberAcqPoints/2)
        self.nmrPlot()
    
    def nmrPlot(self):
        self.nmrPhase()
        self.nmrSpectrum = np.real(self.nmrPhasedData)     #plot real part only
        self.nmrSpectrum = self.nmrSpectrum/np.amax(self.nmrSpectrum, axis=None)
        self.nmrSpectrumGraph()

    def nmrPhase(self):
        """Performs ph0"""
        self.nmrFFT()
        self.ph0Value = self.ph0Slider.value()
        self.ph1Value = self.ph1Slider.value()
        
        if numberAcqPoints == 1:
            print("Error: unphased_data should be composed of coloumn vectors")
            
        value = np.exp((self.ph0Value*np.pi/180)*1.0j)
        self.nmrPhasedData = self.nmrFFTData * value
        
        """Performs ph1"""
        if abs(self.ph1Value) > 0:
            fphase = np.linspace(0, self.ph1Value, numberAcqPoints)
            fphase = fphase - fphase[pivot]
            kron_x = np.ones_like(numberFID)
            kron_y = np.exp((fphase*np.pi/180)*1.0j)
            fphase = np.kron(kron_x, kron_y)
            self.nmrPhasedData = self.nmrPhasedData * fphase
        
    def nmrFFT(self):
        """Pefroms FFT on FID"""
        global numberFID
        global numberAcqPoints
        global pivot
        global spectralWidth
        exp_value = self.nmrExpValue.value()
        self.shiftLeft()
        em_val = np.arange(0,numberAcqPoints,1)
        em_val = -1 * em_val * exp_value * np.pi/spectralWidth
        for i in range(0, numberFID):
            self.procfid[i,0:] = self.procfid[i,0:] * np.transpose(np.exp(em_val))
            self.nmrFFTData = np.zeros((numberFID, numberAcqPoints), complex)    
            """Performs Fourier transform on the spectral data"""
            self.nmrFFTData = np.fft.fft(self.procfid)
            """Performs spectral shift(swapping +ve and-ve of the spectrum"""
            self.nmrFFTData = np.fft.fftshift(self.nmrFFTData)
        
    def shiftLeft(self):
        global shift_left
        global baseline_correction
        baseline_correction = float(self.nmrBaseLine.text())
        shift_left = self.nmrShiftLeft.value()
        """Performs array rotation, replacing the rotated elements with zeroes and baseline correction"""
        self.leftShiftedFID = self.leftRotate(self.nmrData, shift_left)
        # print("Left Shifted FID", self.leftShiftedFID)
        self.alteredFID = self.replaceZeroes(self.leftShiftedFID, shift_left)
        # print("Altered FID", self.alteredFID)
        self.procfid = np.zeros((numberFID, numberAcqPoints), complex)
        for i in range(0, numberFID):
            self.procfid[i,0:] = self.nmrData[i,0:] - np.mean(self.alteredFID[i, round(numberAcqPoints*(1-baseline_correction)):(numberAcqPoints)])
        
        # print("Proc FID", self.procfid)
        
    def leftRotate(self, fid, d):
        """Rotates the array from left to right by 'd' steps & returns new fid"""
        for g in range(0,numberFID):
            n = numberAcqPoints
            if d>= n:
                print("Shift_left value is higher than acquisition points")
                sys.exit()
            else:
                for j in range(0,d): 
                    temp = fid[g,0] 
                    for i in range(n-1): 
                        fid[g, i] = fid[g, (i+1)] 
                    fid[g, (n-1)] = temp 
        return fid

    def replaceZeroes(self,fid, d):
        """Replaces the shifted elements in the array with zeroes"""
        n = numberAcqPoints
        for g in range(0,numberFID):
            for i in range(0,d):
                fid[g, (n-1)] = 0
                n -= 1
        return fid
    
    def create_xaxis(self,axis_type='pts', zf=None, numberAcqPoints=None, freq = None, ref_index=None, ref_value=None):
        global spectralWidth
        if (zf is not None):
            xaxis = np.arange(zf,0,-1)  #note this returns [zf, zf-1, ...2,1]  - zero not included      Note: you may want to reverse this?
            if axis_type == 'pts':
                return xaxis
        else:
            print("error in create_xaxis - zf not defined")
            return       
    
        if (spectralWidth is not None):
            xaxis = np.linspace(spectralWidth/2,-spectralWidth/2,zf)
            if (axis_type == 'Hz') | (axis_type == 'Hz_unref'):
                return xaxis
            elif (axis_type == 'kHz')|(axis_type == 'kHz_unref'):
                return xaxis/1000
            elif axis_type == 'Hz_ref':
                if (ref_index is not None) & (ref_value is not None): 
                    xaxis = xaxis -xaxis[int(ref_index)] + ref_value   
                    return xaxis
            elif axis_type == 'kHz_ref':
                if (ref_index is not None) & (ref_value is not None): 
                    xaxis = xaxis-xaxis[int(ref_index)] + ref_value*1000   
                    return xaxis/1000
        else:
            print("error in create_xaxis - spectralWidth not defined")
            return       
        if (freq is not None):
            xaxis = xaxis/freq *1e6   #convert Hz to ppm  (xaxis and freq are both in Hz)
            if axis_type == 'ppm_unref':
                return xaxis
        else:
            print("error in create_xaxis - freq not defined")
            return       
        if (ref_index is not None) & (ref_value is not None): 
            if (axis_type == 'ppm_ref') | (axis_type =='ppm'):
                xaxis = xaxis -xaxis[int(ref_index)] + ref_value  
                return xaxis
        else:
            print("error in create_xaxis - ref_point and/or ref_value are not defined")
            return       
        print("error in create_xaxis - if you got this far, then axis_type was not a recognized type")
        return

    def XAxis(self):
        global spectralWidth
        global numberAcqPoints
        global spectrometerFreq
        global numberFID
        global ref_value

        ref_value = float(self.referenceValue.text())

        if self.nmrPlotXAxis.currentText() == 'pts':
            self.xaxis = self.create_xaxis(axis_type='pts', zf=numberAcqPoints)
        elif self.nmrPlotXAxis.currentText() == 'kHz':
            self.xaxis = self.create_xaxis(axis_type='kHz', zf=numberAcqPoints)
            self.xaxis = self.create_xaxis(axis_type='kHz_ref', zf=numberAcqPoints, ref_index=numberAcqPoints/2, ref_value=ref_value)
        elif self.nmrPlotXAxis.currentText() == 'ppm':
            self.xaxis = self.create_xaxis(axis_type='ppm_unref', zf=numberAcqPoints, freq = spectrometerFreq)
            self.xaxis = self.create_xaxis(axis_type='ppm', zf=numberAcqPoints, freq = spectrometerFreq, ref_index=numberAcqPoints/2, ref_value=ref_value)
    
    def nmrSpectrumGraph(self):
        global numberFID
        self.XAxis()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        offset = 1.0
        self.sc.axes.cla()

        for i in range(0, numberFID):
            self.sc.axes.plot(self.xaxis, self.nmrSpectrum[i,0:] + (i*offset), label = self.filesNames[i])
            # self.sc.axes.legend(bbox_to_anchor=(0.9,0.60), fontsize = 15)
            # self.sc.axes.legend(fontsize = 15)
            handles, labels = self.sc.axes.get_legend_handles_labels()
            self.sc.axes.legend(reversed(handles), reversed(labels), fontsize=15)
            self.sc.axes.set_xlim([max(self.xaxis), min(self.xaxis)])
            self.sc.axes.set_title(self.nmrPlotTitle.text(), fontsize = 20)
            if self.nmrPlotYLabel.text() == "":
                self.nmrPlotYLabel.setText('Arbitrary Units (AU)')
            if self.nmrPlotXAxis.currentText() == 'pts':
                self.nmrPlotXLabel.setText('pts')
            elif self.nmrPlotXAxis.currentText() == 'kHz':
                self.nmrPlotXLabel.setText('kHz')
            elif self.nmrPlotXAxis.currentText() == 'ppm':
                self.nmrPlotXLabel.setText('ppm')
            self.sc.axes.set_ylabel(self.nmrPlotYLabel.text(), fontsize = 20)
            self.sc.axes.set_xlabel(self.nmrPlotXLabel.text(), fontsize = 20)
        
        if self.mainRightLayout.count() > 0:
            for i in reversed (range(self.mainRightLayout.count())):
                self.mainRightLayout.takeAt(i).widget().deleteLater()

        self.toolbar = NavigationToolbar(self.sc, self)
        self.mainRightLayout.addWidget(self.toolbar)
        self.mainRightLayout.addWidget(self.sc)
        self.show()

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())
    
if __name__ == '__main__':
    main()