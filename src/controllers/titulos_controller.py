from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from view.ventana_titulos import Ui_Dialog

class VentanaTitulos(QDialog, Ui_Dialog):

	def __init__(self, *args, **kwargs):
		QDialog.__init__(self, *args)
		self.setupUi(self)

		self._ediciones = []

		self.tableTitulos.cellDoubleClicked.connect(self._edicion_celda_titulo)
		self.buttonBox.accepted.connect(self._guardar)

	def importar(self, bitacora, funcion_actualizar_completador):
		self.tableTitulos.setRowCount(0)

		self._bitacora = bitacora
		self._actualizar_completador = funcion_actualizar_completador

		titulos = self._bitacora.unique_titulos()

		for n, t in enumerate(titulos):
			self.tableTitulos.insertRow(n)

			titulo = t['titulo']
			conteo = str(t['conteo'])
			ultimo = t['ultimo'].strftime(r'%Y-%m-%d %H:%Mhrs')

			self.tableTitulos.setItem(n, 0, QTableWidgetItem(titulo))
			self.tableTitulos.setItem(n, 1, QTableWidgetItem(conteo))
			self.tableTitulos.setItem(n, 2, QTableWidgetItem(ultimo))

		self.tableTitulos.resizeColumnsToContents()

	def _edicion_celda_titulo(self, row, column):
		item = self.tableTitulos.item(row, 0)
		self._ediciones.append({'old_name' : item.text(), 'row' : row})
		self.tableTitulos.editItem(item)

	def _guardar(self):
		num_cambios_inicial = self._bitacora.num_cambios

		for e in self._ediciones:
			item = self.tableTitulos.item(e['row'], 0)
			self._bitacora.editar_titulo(e['old_name'], item.text())

		if self._bitacora.num_cambios > num_cambios_inicial:
			self._actualizar_completador