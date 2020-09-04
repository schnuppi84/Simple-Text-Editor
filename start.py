from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMenuBar, QAction, QTextEdit, QHBoxLayout, QWidget, QFontDialog, QColorDialog, QFileDialog, QDialog, QVBoxLayout, QMessageBox
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QFileInfo
import sys

class Window(QMainWindow):                  # Klasse Fenster
    def __init__(self):
        super().__init__()
           
        self.title = ('Einfacher Text Editor mit PDF Funktion') # Window Title
        self.top = 400                          # 
        self.left = 600                         #   Abstand
        self.width = 400                        #
        self.height = 300                       #
        self.iconName = 'win.png'       #Icon
        self.setWindowIcon(QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
      
        self.createEditor()     # Anzeigen von Editor
        self.CreateMenu()       # Anzeigen von der Menü Bar
       
        self.show()

#--------------------------------- M e n ü  B a r -------------------------------#
    def CreateMenu(self):                   
        
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu("Datei")
        editMenu = mainMenu.addMenu("Bearbeiten")
        infoMenu = mainMenu.addMenu("Info")

        helpAction = QAction(QtGui.QIcon(""), 'Help', self)
        helpAction.setShortcut("")
        helpAction.triggered.connect(self.helpAction)
        infoMenu.addAction(helpAction)  #   Öffnen

        openAction = QAction(QIcon("open.png"), 'Öffnen', self)
        openAction.setShortcut("")
        openAction.triggered.connect(self.openAction)
        fileMenu.addAction(openAction)  #   Öffnen
        
        saveAction = QAction(QIcon("save.png"), 'Speichern unter', self)
        saveAction.setShortcut("")
        saveAction.triggered.connect(self.saveAction)
        fileMenu.addAction(saveAction)  #   Speichern

        printAction = QAction(QIcon("print.png"), 'Drucken', self)
        printAction.setShortcut("")
        printAction.triggered.connect(self.printDialog)
        fileMenu.addAction(printAction) #   Drucken

        printpreviewAction = QAction(QIcon("preprint.png"), 'Druckvorschau', self)
        printpreviewAction.triggered.connect(self.printPreviewDialog)
        fileMenu.addAction(printpreviewAction) #   Vorschau Druck

        pdfAction = QAction(QIcon("pdf.png"), 'PDF Exportieren', self)
        pdfAction.triggered.connect(self.pdfExport)
        fileMenu.addAction(pdfAction) #   Vorschau Druck

        exitAction = QAction(QIcon("exit.png"), 'Beenden', self)
        exitAction.setShortcut("")
        exitAction.triggered.connect(self.exitWindow)
        fileMenu.addAction(exitAction)  #   Beenden

        editAction = QAction(QIcon("edit.png"), 'Schrift', self)
        editAction.setShortcut("")
        editAction.triggered.connect(self.fontDialog)
        editMenu.addAction(editAction) #   Bearbeiten
        
        colorAction = QAction(QIcon("color.png"), 'Schrift Farbe', self)        # Schrift Farbe 
        colorAction.triggered.connect(self.colorDialog)
        editMenu.addAction(colorAction)
        
#------------------------ Exit Button funktion  ----------------------------------#
    
    def exitWindow(self):                   
        self.close()

#-------------------------Text Editor---------------------------------------------#

    def createEditor(self):                
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

#------------------------Schrift Dialog------------------------------------------#

    def fontDialog(self):                   
        font, ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

#----------------------- Schrift Farbe Dialog ----------------------------------#

    def colorDialog(self):                  
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

#----------------------------Drucken der Datei---------------------------------#
     
    def printDialog(self):              
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

#--------------------------Druck Vorschau---------------------------------------#

    def printPreviewDialog(self):                           
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()

    def printPreview(self, printer):
        self.textEdit.print_(printer)
        
#-------------------------PDF Exporter-----------------------------------------#

    def pdfExport(self):                                    
        fn, _= QFileDialog.getSaveFileName(self, "Export PDF", None, "PDF files (.pdf);;All Files()")

        if fn != '':

            if QFileInfo(fn).suffix() == "" :fn += '.pdf'

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document ().print_(printer)

#-------------------------------Datei Laden------------------------------------#

    def openAction(self):              

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

#------------------------------Datei Speichern---------------------------------#

    def saveAction(self):              

        filename, _ = QFileDialog.getSaveFileName(self, 'Datei Speichern', ".txt", "Alle Datein (*);; Text Datei (*.txt)")

        if filename:
            with open(filename, "w") as file:
                file.write(self.textEdit.toPlainText()) 
                file.close()
            
#-----------------------------Message Box-------------------------------------#

    def helpAction(self):
        QMessageBox.about(self, "Entwickelt mit QT5", "Alpha 1.0")

#------------------------------Ende-------------------------------------------#
App = QApplication(sys.argv)
Window = Window()
sys.exit(App.exec_())
