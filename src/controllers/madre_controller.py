from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QCompleter, QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

from models.bitacora_lectura import Registro, Bitacora
from models.gestor_ajustes import Ajustes

from view.ventana_madre import Ui_MainWindow

from controllers.titulos_controller import VentanaTitulos
from controllers.agregar_controller import VentanaAgregar

import os


class VentanaMadre(QMainWindow, Ui_MainWindow):

	def __init__(self, *args, **kwargs):
		QMainWindow.__init__(self, *args)
		self.setupUi(self)

		self._ruta_ajustes = './settings.json'
		self._ajustes = Ajustes(self._ruta_ajustes)
		self._ajustes.cargar_ajustes()

		try:
			self._ruta_db = self._ajustes['ruta_db']
		except KeyError:
			self._ruta_db = './data/db.json'
			self._ajustes['ruta_db'] = self._ruta_db

		if not os.path.isdir(os.path.dirname(self._ruta_db)):
			os.mkdir(os.path.dirname(self._ruta_db))

		self._patron = ''
		self._lista_versiones = []
		self._num_versiones_guardadas = 0
		self._version_en_uso = -1

		self._bitacora = Bitacora()
		self._bitacora.cargar_ruta_db(self._ruta_db)
		self._bitacora.cargar_data()

		# Botones

		self.buscarButton.clicked.connect(self._buscartitulo)
		self.buttonTitulosRegistrados.clicked.connect(self._abrirVentanaTitulosRegistrados)
		self.agregarButton.clicked.connect(self._abrirVentanaAgregar)
		self.buttonEliminarRegistro.clicked.connect(self._eliminarRegistro)


		# Teclas

		self.cuadroBuscar.returnPressed.connect(self.buscarButton.animateClick)

		# Menus

		# menú Archivo
		self.actionExportarTXT.triggered.connect(self._exportarTXT)
		self.actionImportarTXT.triggered.connect(self._importarTXT)

		# menú Editar

		self.actionDeshacer.triggered.connect(self._deshacer_cambio)
		self.actionRehacer.triggered.connect(self._rehacer_cambio)

		# Menú base de datos

		self.actionActualizarBase.triggered.connect(self._actualizar_base)
		self.actionEditarRutaBase.triggered.connect(self._editar_ruta_base)

		# Acciones iniciales
		self._guardar_versiones()
		self._actualizar_completador()

	def _buscartitulo(self, checked, boton = True):

		if boton:
			self._patron = self.cuadroBuscar.text().strip()

		if not self._patron:
			return

		titulos_encontrados = self._bitacora.buscar_titulo(self._patron)

		num_resultados = len(titulos_encontrados)
		self.contadorLabel.setText(f'Resultados encontrados: {num_resultados}')

		self._listar_en_tabla(titulos_encontrados)

	def _listar_en_tabla(self, titulos):
		self.tableWidget.setRowCount(0)
		self._registrosTabulados = []

		if not len(titulos):
			return

		for n,t in enumerate(titulos):
			self.tableWidget.insertRow(n)
			titulo = t.titulo
			fecha = t.fecha.strftime(r'%Y-%m-%d')
			hora = t.fecha.strftime(r'%H:%M')
			ultimo = t.ultimo_leido

			self.tableWidget.setItem(n, 0, QTableWidgetItem(titulo))
			self.tableWidget.setItem(n, 1, QTableWidgetItem(fecha))
			self.tableWidget.setItem(n, 2, QTableWidgetItem(f'{hora}hrs'))
			self.tableWidget.setItem(n, 3, QTableWidgetItem(str(ultimo)))

			self._registrosTabulados.append(t)

		self.tableWidget.resizeColumnsToContents()

	def _actualizar_completador(self):
		titulos = list(map(lambda x: x['titulo'], self._bitacora.unique_titulos()))

		self._completador = QCompleter(titulos)
		self._completador.setCaseSensitivity(Qt.CaseInsensitive)
		self._completador.setFilterMode(Qt.MatchContains)

		self.cuadroBuscar.setCompleter(self._completador)

	def _eliminarRegistro(self):
		rangos = self.tableWidget.selectedRanges()

		if not rangos:
			return

		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setText(f'¿Estás seguro de eliminar el(los) registro(s)?')
		msg.setWindowTitle('Eliminar registro(s)')
		msg.setStandardButtons(QMessageBox.Abort | QMessageBox.Yes)

		respuesta = msg.exec_()

		if respuesta != QMessageBox.Yes:
			return

		row_eliminar = []

		for rango in rangos:
			inicialrow = rango.bottomRow()
			rowstop = inicialrow + rango.rowCount() # finalrow = rowstop - 1

			for row in range(inicialrow, rowstop):
				registro_eliminar = self._registrosTabulados[row]
				self._bitacora.eliminar_registro(registro_eliminar)
				row_eliminar.append(row)

		row_eliminar.sort()
		row_eliminar.reverse()
		for row in row_eliminar:
			self.tableWidget.removeRow(row)

		self._guardar_versiones()

	def _guardar_versiones(self):

		if not self._lista_versiones:
			self._lista_versiones.append(self._bitacora.copy())

		if self._lista_versiones[self._version_en_uso] != self._bitacora:
			if self._version_en_uso < -1:
				self._lista_versiones = self._lista_versiones[:self._version_en_uso + 1]
			self._lista_versiones.append(self._bitacora.copy())
			self._version_en_uso = -1

		self._num_versiones_guardadas = len(self._lista_versiones)

	def _deshacer_cambio(self):
		if self._version_en_uso == -len(self._lista_versiones):
			return

		self._version_en_uso -= 1
		self._bitacora = self._lista_versiones[self._version_en_uso]
		self._buscartitulo(checked = False, boton = False)

	def _rehacer_cambio(self):
		if self._version_en_uso == -1:
			return

		self._version_en_uso += 1
		self._bitacora = self._lista_versiones[self._version_en_uso]
		self._buscartitulo(checked = False, boton = False)

	def _exportarTXT(self):

		try:
			ruta = self._ajustes['ruta_exportarTXT']
		except KeyError:
			ruta = './'

		archivo = QFileDialog.getSaveFileName(self, "Guardar archivo",
											os.path.join(ruta, 'salida.txt'),
											'Archivo TXT (*.txt)')[0]

		if not archivo.strip():
			return

		self._bitacora.escribir_archivoTXT(archivo)
		self._ajustes['ruta_exportarTXT'] = os.path.dirname(archivo)

	def _importarTXT(self):

		try:
			ruta = self._ajustes['ruta_importarTXT']
		except KeyError:
			ruta = './'

		archivo = QFileDialog.getOpenFileName(self,"Elige el archivo", ruta, 'Archivo TXT (*.txt)')[0]

		if not archivo.strip():
			return

		self._bitacora.leer_archivoTXT(archivo)
		self._ajustes['ruta_importarTXT'] = archivo

	def _actualizar_base(self):
		self._bitacora.guardar_data()

	def _editar_ruta_base(self):
		try:
			ruta = os.path.dirname(self._ajustes['ruta_db'])
		except KeyError:
			ruta = './'

		ruta = QFileDialog.getExistingDirectory(self,"Elige el directorio de la base de datos",
												ruta)

		if not ruta.strip():
			return

		self._ruta_db = os.path.join(ruta, 'db.json')
		self._ajustes['ruta_db'] = self._ruta_db
		self._bitacora.cargar_ruta_db(self._ruta_db)
		self._bitacora.guardar_data()

	def _abrirVentanaTitulosRegistrados(self):
		self._ventanaTitulosRegistrados = VentanaTitulos()
		self._ventanaTitulosRegistrados.importar(self._bitacora, self._actualizar_completador)
		self._ventanaTitulosRegistrados.exec_()

		self._guardar_versiones()

	def _abrirVentanaAgregar(self):
		self._ventanaAgregar = VentanaAgregar()
		self._ventanaAgregar.importar(self._bitacora, self._completador, self._actualizar_completador)
		self._ventanaAgregar.exec_()

		self._guardar_versiones()

	def closeEvent(self, event):
		num_cambios_base = self._bitacora.num_cambios

		if num_cambios_base == 0:
			event.accept()
			return

		msg = QMessageBox(self)
		msg.setIcon(QMessageBox.Warning)
		msg.setText(f'Hay cambios sin guardar, ¿Desea guardarlos?')
		msg.setWindowTitle('Guardar cambios')
		msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		msg.setDefaultButton(QMessageBox.Yes)

		eleccion = msg.exec_()


		if eleccion == QMessageBox.Yes:
			self._actualizar_base()
			event.accept()
		elif eleccion == QMessageBox.No:
			event.accept()
		else:
			event.ignore()
