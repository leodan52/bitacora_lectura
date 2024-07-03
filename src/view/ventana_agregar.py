# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bin/UI/ventana_agregar.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VentanaAgregar(object):
    def setupUi(self, VentanaAgregar):
        VentanaAgregar.setObjectName("VentanaAgregar")
        VentanaAgregar.resize(802, 217)
        self.verticalLayout = QtWidgets.QVBoxLayout(VentanaAgregar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(VentanaAgregar)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.cuadroAddUltimo = QtWidgets.QLineEdit(self.frame)
        self.cuadroAddUltimo.setObjectName("cuadroAddUltimo")
        self.gridLayout.addWidget(self.cuadroAddUltimo, 2, 1, 1, 1)
        self.cuadroAddTitulo = QtWidgets.QLineEdit(self.frame)
        self.cuadroAddTitulo.setObjectName("cuadroAddTitulo")
        self.gridLayout.addWidget(self.cuadroAddTitulo, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(VentanaAgregar)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.cuadroAddUltimo)
        self.label.setBuddy(self.cuadroAddTitulo)

        self.retranslateUi(VentanaAgregar)
        self.buttonBox.accepted.connect(VentanaAgregar.accept)
        self.buttonBox.rejected.connect(VentanaAgregar.reject)
        QtCore.QMetaObject.connectSlotsByName(VentanaAgregar)

    def retranslateUi(self, VentanaAgregar):
        _translate = QtCore.QCoreApplication.translate
        VentanaAgregar.setWindowTitle(_translate("VentanaAgregar", "Agregar registro"))
        self.label_2.setText(_translate("VentanaAgregar", "¿Cuál fue el último capítulo leído?"))
        self.label.setText(_translate("VentanaAgregar", "Ingrese el título de la obra: "))
        self.label_3.setText(_translate("VentanaAgregar", "<html><head/><body><p><span style=\" font-size:12pt;\">Ingrese los datos a continuación:</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaAgregar = QtWidgets.QDialog()
    ui = Ui_VentanaAgregar()
    ui.setupUi(VentanaAgregar)
    VentanaAgregar.show()
    sys.exit(app.exec_())
