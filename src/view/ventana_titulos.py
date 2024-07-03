# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './bin/UI/ventana_titulos.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(570, 392)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tableTitulos = QtWidgets.QTableWidget(self.frame)
        self.tableTitulos.setStyleSheet("QTableWidget::item{\n"
"    border: None;\n"
"    padding: 10%;;\n"
"}")
        self.tableTitulos.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableTitulos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableTitulos.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableTitulos.setShowGrid(False)
        self.tableTitulos.setCornerButtonEnabled(True)
        self.tableTitulos.setRowCount(1)
        self.tableTitulos.setObjectName("tableTitulos")
        self.tableTitulos.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableTitulos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTitulos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTitulos.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTitulos.setItem(0, 0, item)
        self.tableTitulos.horizontalHeader().setVisible(True)
        self.tableTitulos.horizontalHeader().setCascadingSectionResizes(True)
        self.tableTitulos.horizontalHeader().setDefaultSectionSize(150)
        self.tableTitulos.horizontalHeader().setMinimumSectionSize(100)
        self.tableTitulos.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableTitulos)
        self.verticalLayout.addWidget(self.frame)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setAccessibleName("")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ver/Editar títulos registrados"))
        self.label.setText(_translate("Dialog", "Los títulos agregados en la bitácora son:"))
        self.tableTitulos.setToolTip(_translate("Dialog", "<html><head/><body><p>Da doble click para editar título</p></body></html>"))
        item = self.tableTitulos.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Título"))
        item = self.tableTitulos.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Registros agregados"))
        item = self.tableTitulos.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Último registro"))
        __sortingEnabled = self.tableTitulos.isSortingEnabled()
        self.tableTitulos.setSortingEnabled(False)
        item = self.tableTitulos.item(0, 0)
        item.setText(_translate("Dialog", "sdasdasdadddddddddddddddddddddddddddddddddddddddddddddddddd"))
        self.tableTitulos.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
