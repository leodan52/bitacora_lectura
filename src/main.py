from controllers.madre_controller import VentanaMadre
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
	app = QApplication([])
	Ventana = VentanaMadre()
	Ventana.show()
	app.exec_()
