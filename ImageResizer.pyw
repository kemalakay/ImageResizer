#!usr/bin/python

import os, os.path, imghdr, shutil, sip

sip.setapi('QString', 2)

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PIL import Image
from time import sleep

window = None
resizer = None
srcfile = ''
imagePath = 'images/'

class imageViewer(QMainWindow):
	def __init__(self, parent=None):
		super(imageViewer, self).__init__(parent)
		self.icon = QIcon('Resources/icon.png')
		self.imageList = QListWidget()
		self.imageList.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.imageList.setContextMenuPolicy(Qt.CustomContextMenu)
		self.imageList.connect(self.imageList,SIGNAL("customContextMenuRequested(QPoint)"), self.listItemRightClicked)

		self.user_choice = None
		self.totalImageItems = 0
		self.processSteps = 0

		self.connect(self.imageList, SIGNAL('currentTextChanged(QString)'), self.displayImage)

		self.prepareImageList()
		self.imageLabel=QLabel()
		self.infoLabel = QLabel('Information')

		self.directoryLabel = QLabel("In directory:")

		leftSplitter = QSplitter(Qt.Vertical)
		leftSplitter.addWidget(self.imageLabel)
		leftSplitter.addWidget(self.infoLabel)
		
		mainSplitter = QSplitter(Qt.Horizontal)
		mainSplitter.addWidget(self.imageList)
		mainSplitter.addWidget(leftSplitter)

		self.setCentralWidget(mainSplitter)

		self.displayImage(unicode(self.imageList.item(0).text()))

		self.createActions()
		self.createMenus()

		self.widthTest = QLineEdit()
		self.heightTest = QLineEdit()

		self.setWindowTitle('Image Resizer')
		self.resize(730, 470)

	def prepareImageList(self):
		for r in os.listdir(imagePath):
			if imghdr.what(imagePath+r):
				listItem = QListWidgetItem(self.icon, r)
				self.imageList.addItem(listItem)

	def callResolutionValues(self):
		print self.member1.setImageResolution

	def appendImageList(self, fileDir):
		if imghdr.what(fileDir):
			strippedFileDir = self.findString(fileDir)
			newItem = QListWidgetItem(self.icon, strippedFileDir)
			self.imageList.addItem(newItem)

	def displayImage(self, image):
		pixMap = QPixmap(imagePath + image)
		pixMap = pixMap.scaledToWidth(400)
		self.imageLabel.setPixmap(pixMap)

		self.infoLabel.setText('<h3> Doc Info: </h3>'
								'<b> Doc: </b> %s &nbsp;'
								'<b> Type: </b> %s &nbsp;'
								'<b> Size: </b> %d &nbsp;'
								'<b> Width: </b> %d &nbsp;'
								'<b> Height: </b> %s<hr>' % (
								image,
								imghdr.what(imagePath+image),
								os.stat(imagePath + image)[6],
								pixMap.width(),
								pixMap.height()
								))

	def createActions(self):
		#File menu
		self.openAct = QAction("&Add Image...", self, shortcut="Ctrl+O", triggered=self.open)
		self.exitAct = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)
		
		#Edit menu
		self.resizeAct = QAction("&Set Resolution", self, shortcut="Ctrl+R", triggered=self.showSetSizeDialog)

		# Window size adjusting
		self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
		self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

	def createMenus(self):

		self.fileMenu = QMenu("&File", self)
		self.fileMenu.addAction(self.openAct)
		self.fileMenu.addAction(self.exitAct)

		self.editMenu = QMenu("&Edit", self)
		self.editMenu.addAction(self.resizeAct)

		self.viewMenu = QMenu("&View", self)
		
		self.menuBar().addMenu(self.fileMenu)
		self.menuBar().addMenu(self.editMenu)
		self.menuBar().addMenu(self.viewMenu)


	def showSetSizeDialog(self):
		resizer.show()

	def hideResizeConfirm(self):
		#print 'Hide Resize confirmation msg box'
		self.dialogResize.hide()

	def showResizeConfirm(self):
		self.dialogResize = ResizeMessage(self)
		self.dialogResize.show()

	def showProgressBar(self):
		self.hideResizeConfirm()
		self.dialog = ProgressBarUI(self)
		self.dialog.show()

	def close_(self):
		dialog = QPrintDialog(self.printer, self)

	def open(self):
		fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
		if fileName:
		    image = QImage(fileName)
		    if image.isNull():
		        QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
		        return

		    self.imageLabel.setPixmap(QPixmap.fromImage(image))
		    self.scaleFactor = 1.0

		    self.fitToWindowAct.setEnabled(True)
		    self.updateActions()
		    self.copyFile(fileName)
		    self.appendImageList(fileName)

		    if not self.fitToWindowAct.isChecked():
		        self.imageLabel.adjustSize()

	def normalSize(self):
		self.imageLabel.adjustSize()
		self.scaleFactor = 1.0

	def fitToWindow(self):
		fitToWindow = self.fitToWindowAct.isChecked()
		self.scrollArea.setWidgetResizable(fitToWindow)
		if not fitToWindow:
		    self.normalSize()

		self.updateActions()

	def copyFile(self, srcFile):
		shutil.copy(srcFile, imagePath)

	def updateActions(self):
		self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

	def findString(self, filePath):
		c = '/'
		dirName = filePath
		foo = ( [pos for pos, char in enumerate(dirName) if char == c])
		maxValue = max(foo)
		maxValue += 1
		finalDir = dirName[maxValue:]
		return finalDir

	def listItemRightClicked(self, QPos): 
		self.listMenu= QMenu()
		add_item = self.listMenu.addAction("Add image")
		remove_item = self.listMenu.addAction("Remove image")
		resize_item = self.listMenu.addAction("Resize...")
		self.connect(add_item, SIGNAL("triggered()"), self.open)
		self.connect(remove_item, SIGNAL("triggered()"), self.removeSel) 
		self.connect(resize_item, SIGNAL("triggered()"), self.showResizeConfirm)

		parentPosition = self.imageList.mapToGlobal(QPoint(0, 0))        
		self.listMenu.move(parentPosition + QPos)
		self.listMenu.show() 

	def menuItemClicked(self):		
		currentItemName=str(self.imageList.currentItem().text())
		print(currentItemName)

	def print_row(self):
		items = self.imageList.selectedItems()
		#print [str(x.text()) for x in self.imageList.selectedItems()]
		x=[]
		for i in range(len(items)):
			x.append(str(self.imageList.selectedItems()[i].text()))
			print x  

	def removeSel(self):
		listItems=self.imageList.selectedItems()
		if not listItems: return
		for item in listItems:
			self.imageList.takeItem(self.imageList.row(item))

class ResizeMessage(QMainWindow):
    def __init__(self, parent=None):
        super(ResizeMessage, self).__init__(parent)
        print 'ResizeMessage class has been initialized successfully'

        self.lblConfirmation = QLabel(self)
        self.lblConfirmation.setText('Start resizing with selected item(s)? <br><br>[ Width: ' + str(window.widthTest.text()) + ', ' + 'Height: '
        	+ str(window.heightTest.text()) + ' ]'
        	+ '<br><br> Choose output directory in the next step')
        #print str(window.browseOutputDirectory())
        #% , int(window.heightTest.text())
        self.lblConfirmation.setFixedSize(300,80)
        self.lblConfirmation.move(10, 30)

        qbtnYes = QPushButton('Yes', self)
        #qbtn.clicked.connect(QCoreApplication.instance().quit)
        #qbtn.clicked.connect(window.batchResize)
        qbtnYes.clicked.connect(window.showProgressBar)
        qbtnYes.resize(qbtnYes.sizeHint())
        qbtnYes.move(80, 125)
        qbtnYes.setDefault(True)

        qbtnNo = QPushButton('No', self)
        qbtnNo.clicked.connect(self.hide)
        qbtnNo.resize(qbtnNo.sizeHint())
        qbtnNo.move(150, 125)

        self.setGeometry(300, 300, 300, 190)
        self.setWindowTitle('Confirm')
        self.setFixedSize(self.size())
        self.centerOnScreen()

    def centerOnScreen (self):
    	'''centerOnScreen() Centers the window on the screen.'''
    	resolution = QDesktopWidget().screenGeometry()
    	self.move((resolution.width() / 2) - (self.frameSize().width() / 2), (resolution.height() / 2) - (self.frameSize().height() / 2))

	
class ResizeWindowUI(QMainWindow):
    def __init__(self, parent=None):
        super(ResizeWindowUI, self).__init__(parent)
        self.wValue = setXSize
        self.hValue = setYSize

        # Width label
        self.lblWidth = QLabel(self)
        self.lblWidth.move(20, 35)
        self.lblWidth.setText("Width: ")

        self.le = QLineEdit(self)
        self.le.move(80, 32)
        self.le.setText(str(self.wValue))
        self.le.setValidator(QIntValidator(10, 5000))
        self.le.setMaxLength(4)
        self.le.setAlignment(Qt.AlignRight)
        self.lbl = QLabel(self)
        self.lbl.move(190, 35)
        self.lbl.setText(" px")
        self.lbl.adjustSize

        # Height label
        self.lblHeight = QLabel(self)
        self.lblHeight.move(20, 95)
        self.lblHeight.setText("Height: ")

        self.le2 = QLineEdit(self)
        self.le2.move(80, 92)
        self.le2.setText(str(self.hValue))
        self.le2.setValidator(QIntValidator(10, 5000))
        self.le2.setMaxLength(4)
        self.le2.setAlignment(Qt.AlignRight)
        self.lbl2 = QLabel(self)
        self.lbl2.move(190, 95)
        self.lbl2.setText(" px")
        self.lbl2.adjustSize

        # Set image size button
        self.btn = QPushButton('Set output image size', self)
        self.btn.setFixedWidth(200)
        self.btn.setFixedHeight(40)
        self.btn.move(15, 145)
        self.setImageResolution()
        self.btn.clicked.connect(self.setImageResolution)
        #self.btn.clicked.connect(self.showDialog)

        self.lblResolutionW = QLabel(self)
        self.lblResolutionW.move(80, 190)
        self.lblResolutionW.setText(str(self.le.text()))
        self.lblResolutionW.setFixedSize(60,15)

        self.lblResolutionH = QLabel(self)
        self.lblResolutionH.move(115, 190)
        self.lblResolutionH.setText('x')
        self.lblResolutionH.setFixedSize(60,15)

        self.lblResolutionH = QLabel(self)
        self.lblResolutionH.move(135, 190)
        self.lblResolutionH.setText(str(self.le2.text()))
        self.lblResolutionH.setFixedSize(60,15)

        self.setGeometry(300, 300, 235, 240)
        self.setFixedSize(self.size())
        self.setWindowTitle('Set Resolution')
        self.show()

    def setImageResolution(self):
    	setXSize = self.le.text()
    	setYSize = self.le2.text()
    	self.le.textChanged[str].connect(self.onChangedW)
    	self.le2.textChanged[str].connect(self.onChangedH)

    	window.widthTest.setText(str(setXSize))
    	window.heightTest.setText(str(setYSize))
    	print str(setXSize) + ' ' + str(setYSize)

    def onChangedW(self, text):
    	self.lblResolutionW.setText(text)
    	self.lblResolutionW.adjustSize() 

    def onChangedH(self, text):
    	self.lblResolutionH.setText(text)
    	self.lblResolutionH.adjustSize()

class TaskThread(QThread):
	notifyProgress = pyqtSignal(int)
	processCompleted = pyqtSignal(bool)
	totalImageItems = 0

	def run(self):
		try:
			xSize = int(window.widthTest.text())
			ySize = int(window.heightTest.text())
		except: 
			xSize = 800
			ySize = 600
		steps = 0
		items = window.imageList.selectedItems()
		totalImageItems = len(items)
		for i in range(int(len(items))):
			try:
				# Attempt to open the image file
				fileItem = str(window.imageList.selectedItems()[i].text())
				image = Image.open(imagePath + fileItem)
			except IOError, e:
				# Report error, and then skip to the next argument
				print 'Problem opening', fileItem, ':', e
				continue

			# Resize the image
			new_image = image.resize((xSize, ySize))
			# Split our original filename into name and extension
			(name, extension) = os.path.splitext(fileItem)
			#Save the image as "(original_name)_rescaled"
			new_image.save(destPath + '/' + name + '_' + '_resized.jpg')
			steps += 1
			print 'steps called in THREAD: ' + str(steps)
			self.notifyProgress.emit(int(len(items)))
			time.sleep(0.1)
		print 'Image resizing completed \n' +  'Images saved to: ' + destPath
		self.processCompleted.emit(True)
		#self.hideProgressBar()
		#print 'batch processing is done'


class ProgressBarUI(QMainWindow):
	def __init__(self, parent=None):
		super(ProgressBarUI, self).__init__(parent)

		print 'total item size at the beginning of ProgressBarUI Class: ' + str(int(len(window.imageList.selectedItems())))
		self.outputPath = self.browseOutputDirectory()
		self.progressBar = QProgressBar(self)
		self.progressBar.setRange(0, int(len(window.imageList.selectedItems())))
		self.progressBar.setGeometry(35, 20, 100, 40)
		self.myLongTask = TaskThread()
		self.myLongTask.start()
		self.myLongTask.notifyProgress.connect(self.onProgress)
		self.myLongTask.processCompleted.connect(self.hideProgressBar)

		self.step = 0
		self.setGeometry(300, 300, 280, 170)
		self.setWindowTitle('Progress Bar')
		self.show()
		self.centerOnScreen()

	def onProgress(self, steps):
		#print 'totalItems amount called onProgress: ' + str(self.myLongTask.totalImageItems)
		#print ' '
		self.step += 1
		self.progressBar.setValue(self.step)
		print 'step amount called onProgress:' + str(self.step)

	def hideProgressBar(self):
		self.hide()

	def browseOutputDirectory(self):
		global destPath
		outputPath = 'output/'
		directory = QFileDialog.getExistingDirectory(self, "Find Files", QDir.currentPath())
		outputPath = str(directory)
		print outputPath
		destPath = outputPath
		return str(destPath)

	def centerOnScreen (self):
		'''centerOnScreen() Centers the window on the screen.'''
		resolution = QDesktopWidget().screenGeometry()
		self.move((resolution.width() / 2) - (self.frameSize().width() / 2), (resolution.height() / 2) - (self.frameSize().height() / 2))



if __name__ == '__main__':

    import sys, time

    setXSize = 800
    setYSize = 600
    destPath = ''

    application = QApplication(sys.argv)
    window = imageViewer()
    window.show()

    resizer = ResizeWindowUI()
    resizer.show()
    resizer.hide()

    application.exec_()
    application.deleteLater()
    sys.exit()