#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import slug
from processor import Process
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
	QPushButton, QAction, QLineEdit, QMessageBox, QProgressBar)




class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'Поиск объектов'
		self.left = 200
		self.top = 200
		self.width = 540
		self.height = 340
		self.initUi()
		self.proc = Process()
		#self.initSearchTag()
	
	def initUi(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('info')
		info = QAction( 'info', self )
		
		fileMenu.addAction(info)
		self.setWindowIcon(QtGui.QIcon('web.png'))
		
		self.citytext = QLineEdit(self)
		self.citytext.setPlaceholderText(" введите город")
		self.citytext.move(120, 20)
		self.citytext.resize(280, 30)

		self.categorytext = QLineEdit(self)
		self.categorytext.setPlaceholderText(" введите категорию")
		self.categorytext.move(120, 80)
		self.categorytext.resize(280, 30)

		self.button = QPushButton('сканировать', self)
		self.button.move(120, 180)
		self.button.resize(280, 30)
		self.button.clicked.connect(self.on_click)
		#self.progress = QProgressBar(self)
		#self.progress.move(120, 220)
		#self.progress.resize(280, 30)


		self.show()

	@pyqtSlot()
	def on_click(self):
		
		CityValue = self.citytext.text()
		CategoryValue = self.categorytext.text()
		
		cuty = slug.slug(self.proc.transliterate(CityValue))
		category = slug.slug(self.proc.transliterate(CategoryValue))
		
		self.proc.result_hub(cuty, category)
		print(self.proc.progressbar())
		#self.progress.setValue(self.proc.progressbar())
		
		QMessageBox.question(self, 'Сканирование', CityValue, QMessageBox.Ok, QMessageBox.Ok)
		self.citytext.setText("")
		self.categorytext.setText("")

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
