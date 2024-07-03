from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtGui import QIntValidator

from view.ventana_agregar import Ui_VentanaAgregar

from datetime import datetime

class VentanaAgregar(QDialog, Ui_VentanaAgregar):

	def __init__(self, *args, **kwargs):
		QDialog.__init__(self, *args)
		self.setupUi(self)

		validador = QIntValidator()
		self.cuadroAddUltimo.setValidator(validador)
		self.cuadroAddTitulo.setFocus()

		self.setTabOrder(self.cuadroAddTitulo, self.cuadroAddUltimo)
		self.setTabOrder(self.cuadroAddUltimo, self.buttonBox.button(QDialogButtonBox.Ok))

		self.buttonBox.accepted.connect(self._guardar)


	def importar(self, bitacora, completador, funcion_actualizar_completador):
		self._bitacora = bitacora
		self._actualizar_completador = funcion_actualizar_completador

		self.cuadroAddTitulo.setCompleter(completador)


	def _guardar(self):

		titulo = self.cuadroAddTitulo.text().strip()
		ultimo = self.cuadroAddUltimo.text().strip()

		if '' in [titulo, ultimo]:
			return

		fecha_hora = datetime.now()

		self._bitacora.agregar(titulo, int(ultimo), fecha_hora)
		self._actualizar_completador()