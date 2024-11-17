import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import PyQt5.QtWidgets
import os




class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("Formulario con Ejecución de Script")
        # Dimensiones de la ventana
        ancho = 600
        alto = 400
        x_ventana = PyQt5.QtWidgets.QDesktopWidget().screenGeometry().width() // 2 - ancho // 2
        y_ventana = PyQt5.QtWidgets.QDesktopWidget().screenGeometry().height() // 2 - alto // 2
        self.setGeometry(x_ventana, y_ventana, ancho, alto)
  
        
        

        # Crear los widgets
        self.label = QLabel("N movimientos:", self)
        self.campo_numero = QLineEdit(self)
        self.campo_numero.setPlaceholderText("Ejemplo: 5")  # Placeholder para el campo de texto

        # Botón de ejecutar otro script
        self.boton_ejecutar = QPushButton("Personalizar LAB", self)
        self.boton_ejecutar.clicked.connect(self.laberinto)
        self.texto_ejecutar = QLabel("Apartado que nos permite construir el laberinto a nuestro gusto", self)

        # Botón de ejecutar el proceso completo
        self.boton_final = QPushButton("SOLUCIÓN", self)
        self.boton_final.clicked.connect(self.proceso_completo)
        self.texto_final = QLabel("Poner a prueba la IA para buscar la solucion, con metodos\n mixtos. \n(Profundidad, Costo, Amplitud, Limitada, Iterativa y Avara)", self)

        # Hacer los botones cuadrados (igual ancho y alto)
        self.boton_ejecutar.setFixedSize(150, 150)
        self.boton_final.setFixedSize(150, 150)

        # Layout para el formulario
        layout_form = QFormLayout()
        layout_form.addRow(self.label, self.campo_numero)

        # Layout horizontal para el primer botón y su texto
        layout_ejecutar = QHBoxLayout()
        layout_ejecutar.addWidget(self.boton_ejecutar)
        layout_ejecutar.addWidget(self.texto_ejecutar)

        # Layout horizontal para el segundo botón y su texto
        layout_final = QHBoxLayout()
        layout_final.addWidget(self.boton_final)
        layout_final.addWidget(self.texto_final)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(layout_form)
        layout_principal.addLayout(layout_ejecutar)
        layout_principal.addLayout(layout_final)

        # Establecer el layout de la ventana
        self.setLayout(layout_principal)

        # Aplicar el estilo CSS a la ventana
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial';
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 5px;
                
            }
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QFormLayout {
                margin: 20px;
                padding: 20px;
            }
            QVBoxLayout {
                margin: 20px;
                padding: 20px;
            }
            QHBoxLayout {
                margin: 20px;
                padding: 20px;
            }
            QLabel {
                font-size: 16px;
                margin-bottom: 5px;
            }
        """)

    def laberinto(self):
        # Ejecutar constuir_laberinto.py
        print("Ejecutando construir_laberinto.py")
        os.system("python construir_laberinto.py")

    def proceso_completo(self):
        # Obtener el valor ingresado y ejecutar el proceso completo
        valor = self.campo_numero.text()
        
        if valor.isdigit():
            print(f"Iniciando el proceso completo con el valor: {valor}")
            with open("valor.txt", "w") as archivo:
                archivo.write(valor)
            os.system("python combinacion.py")
        else:
            print("Por favor ingresa un valor numérico válido.")

# Crear la aplicación y la ventana
app = QApplication(sys.argv)
ventana = MiVentana()
ventana.show()

# Ejecutar la aplicación
sys.exit(app.exec_())
