# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ml_stock.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 780)
        MainWindow.setStyleSheet("background-color: rgb(26, 6, 106);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 241, 781))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setStyleSheet("QPushButton {\n"
"background-color: rgb(26, 6, 106);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"height: 50px;\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(38, 8, 156);\n"
"}")
        self.pushButton_4.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("QPushButton {\n"
"background-color: rgb(26, 6, 106);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"height: 50px;\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(38, 8, 156);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"background-color: rgb(26, 6, 106);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"height: 50px;\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(38, 8, 156);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setStyleSheet("QPushButton {\n"
"background-color: rgb(26, 6, 106);\n"
"color: rgb(255, 255, 255);\n"
"border-radius: 10px;\n"
"height: 50px;\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(38, 8, 156);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)
        self.verticalLayout.setStretch(3, 2)
        self.verticalLayout.setStretch(4, 2)
        self.verticalLayout.setStretch(5, 4)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(240, 0, 881, 781))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.verticalLayoutWidget_2)
        self.stackedWidget.setObjectName("stackedWidget")
        self.Dashboard = QtWidgets.QWidget()
        self.Dashboard.setObjectName("Dashboard")
        self.graphicsView = QtWidgets.QGraphicsView(self.Dashboard)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 881, 791))
        self.graphicsView.setObjectName("graphicsView")
        self.stackedWidget.addWidget(self.Dashboard)
        self.Graph = QtWidgets.QWidget()
        self.Graph.setObjectName("Graph")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.Graph)
        self.graphicsView_2.setGeometry(QtCore.QRect(0, 0, 881, 791))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.stackedWidget.addWidget(self.Graph)
        self.Financial = QtWidgets.QWidget()
        self.Financial.setObjectName("Financial")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.Financial)
        self.graphicsView_3.setGeometry(QtCore.QRect(0, 0, 881, 791))
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.stackedWidget.addWidget(self.Financial)
        self.News = QtWidgets.QWidget()
        self.News.setObjectName("News")
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.News)
        self.graphicsView_4.setGeometry(QtCore.QRect(0, 0, 881, 791))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.stackedWidget.addWidget(self.News)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ML Stock"))
        self.label.setText(_translate("MainWindow", "ML STOCK RADAR"))
        self.pushButton_4.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton.setText(_translate("MainWindow", "Graph"))
        self.pushButton_2.setText(_translate("MainWindow", "Financial"))
        self.pushButton_3.setText(_translate("MainWindow", "News"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
