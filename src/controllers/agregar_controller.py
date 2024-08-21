from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QDoubleValidator

from view.ventana_agregar import Ui_VentanaAgregar

from datetime import datetime

class VentanaAgregar(QDialog, Ui_VentanaAgregar):

	def __init__(self, *args, **kwargs):
		QDialog.__init__(self, *args)
		self.setupUi(self)

		validador = QDoubleValidator()
		self.cuadroAddUltimo.setValidator(validador)
		self.cuadroAddTitulo.setFocus()

		self.setTabOrder(self.cuadroAddTitulo, self.cuadroAddUltimo)
		self.setTabOrder(self.cuadroAddUltimo, self.cuadroInfoAdicional)
		self.setTabOrder(self.cuadroInfoAdicional, self.buttonBox.button(QDialogButtonBox.Ok))

		self.buttonBox.accepted.connect(self._guardar)


	def importar(self, bitacora, completador, funcion_actualizar_completador):
		self._bitacora = bitacora
		self._actualizar_completador = funcion_actualizar_completador

		self.cuadroAddTitulo.setCompleter(completador)


	def _guardar(self):

		titulo = self.cuadroAddTitulo.text().strip()
		ultimo = self.cuadroAddUltimo.text().strip()
		info = self.cuadroInfoAdicional.text().strip()

		if '' in [titulo, ultimo]:
			return

		fecha_hora = datetime.now()

		self._bitacora.agregar(titulo, float(ultimo), fecha_hora, info_adicional=info)
		self._actualizar_completador()