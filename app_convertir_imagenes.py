import os
import sys
import shutil
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, 
                            QProgressBar, QMessageBox, QTextEdit, QGroupBox,
                            QLineEdit, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image

class ConvertidorThread(QThread):
    """Hilo para procesar la conversión de imágenes a PDF"""
    progreso = pyqtSignal(int)
    log = pyqtSignal(str)
    finalizado = pyqtSignal(bool)
    
    def __init__(self, archivo_excel, nombre_evento, directorio_eventos):
        super().__init__()
        self.archivo_excel = archivo_excel
        self.nombre_evento = nombre_evento
        self.directorio_eventos = directorio_eventos
    
    def run(self):
        try:
            # Usar la estructura de directorios del evento
            directorio_evento = os.path.join(self.directorio_eventos, self.nombre_evento)
            dir_csv = os.path.join(directorio_evento, "csv")
            dir_imagenes = os.path.join(directorio_evento, "imagenes")
            dir_pdfs = os.path.join(directorio_evento, "PDFs")
            
            # Convertir Excel a CSV
            archivo_csv = os.path.join(dir_csv, "imagenes.csv")
            self.log.emit(f"📊 Convirtiendo Excel a CSV para el evento '{self.nombre_evento}'...")
            
            # Leer el archivo Excel
            df = pd.read_excel(self.archivo_excel)
            
            # Asegurarse de que existan las columnas necesarias
            if 'original' not in df.columns or 'nuevo' not in df.columns:
                # Intentar usar la primera y segunda columna
                if len(df.columns) >= 2:
                    df = df.rename(columns={df.columns[0]: 'original', df.columns[1]: 'nuevo'})
                    self.log.emit("⚠️ No se encontraron columnas 'original' y 'nuevo'. Usando las dos primeras columnas.")
                else:
                    self.log.emit("❌ El archivo Excel no tiene suficientes columnas.")
                    self.finalizado.emit(False)
                    return
            
            # Guardar como CSV
            df.to_csv(archivo_csv, sep=';', index=False)
            self.log.emit(f"✅ CSV guardado en: {os.path.join(self.nombre_evento, 'csv', 'imagenes.csv')}")
            
            # Procesar imágenes
            total_filas = len(df)
            for idx, fila in df.iterrows():
                nombre_original = str(fila['original']).strip() + '.png'
                nuevo_nombre = str(fila['nuevo']).strip().replace(' ', '_') + '.pdf'
                
                ruta_imagen = os.path.join(dir_imagenes, nombre_original)
                ruta_pdf = os.path.join(dir_pdfs, nuevo_nombre)
                
                # Actualizar progreso
                progreso_actual = int((idx + 1) / total_filas * 100)
                self.progreso.emit(progreso_actual)
                
                if os.path.exists(ruta_imagen):
                    try:
                        with Image.open(ruta_imagen) as img:
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            img.save(ruta_pdf, "PDF", resolution=100.0)
                        self.log.emit(f"✅ Convertido: {nombre_original} → {nuevo_nombre}")
                    except Exception as e:
                        self.log.emit(f"⚠️ Error al convertir {nombre_original}: {str(e)}")
                else:
                    self.log.emit(f"❌ No se encontró la imagen: {os.path.join(self.nombre_evento, 'imagenes', nombre_original)}")
            
            self.log.emit(f"🎉 ¡Proceso completado para el evento '{self.nombre_evento}'!")
            self.finalizado.emit(True)
            
        except Exception as e:
            self.log.emit(f"❌ Error: {str(e)}")
            self.finalizado.emit(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = None
        self.imagenes_seleccionadas = []
        self.nombre_evento = ""
    
    def initUI(self):
        self.setWindowTitle("CertManager Pro")
        self.setMinimumSize(700, 500)
        
        # Establecer icono de la aplicación
        icono_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recursos", "certmanager_icon.ico")
        if os.path.exists(icono_path):
            self.setWindowIcon(QIcon(icono_path))
        
        # Widget y layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Sección para seleccionar o crear evento - Grupo 0
        grupo_evento = QGroupBox("Paso 1: Seleccionar o crear evento/categoría")
        evento_layout = QVBoxLayout()
        
        evento_input_layout = QHBoxLayout()
        self.label_evento = QLabel("Nombre del evento:")
        self.input_evento = QLineEdit()
        self.btn_cargar_eventos = QPushButton("Actualizar eventos")
        self.btn_cargar_eventos.clicked.connect(self.cargar_eventos_disponibles)
        evento_input_layout.addWidget(self.label_evento)
        evento_input_layout.addWidget(self.input_evento)
        evento_input_layout.addWidget(self.btn_cargar_eventos)
        
        evento_lista_layout = QHBoxLayout()
        self.label_eventos = QLabel("Eventos existentes:")
        self.combo_eventos = QComboBox()
        self.combo_eventos.currentIndexChanged.connect(self.cambiar_evento)
        evento_lista_layout.addWidget(self.label_eventos)
        evento_lista_layout.addWidget(self.combo_eventos)
        
        evento_layout.addLayout(evento_input_layout)
        evento_layout.addLayout(evento_lista_layout)
        grupo_evento.setLayout(evento_layout)
        
        # Sección para seleccionar archivo Excel - Grupo 2
        grupo_excel = QGroupBox("Paso 2: Seleccionar archivo Excel")
        excel_layout = QHBoxLayout()
        self.label_excel = QLabel("Archivo Excel:")
        self.btn_excel = QPushButton("Seleccionar Excel")
        self.btn_excel.clicked.connect(self.seleccionar_excel)
        excel_layout.addWidget(self.label_excel)
        excel_layout.addWidget(self.btn_excel)
        grupo_excel.setLayout(excel_layout)
        
        # Sección para seleccionar imágenes - Grupo 2
        grupo_imagenes = QGroupBox("Paso 2: Seleccionar imágenes PNG")
        imagenes_layout = QVBoxLayout()
        
        self.label_imagenes = QLabel("Imágenes seleccionadas: 0")
        self.btn_imagenes = QPushButton("Seleccionar Imágenes PNG")
        self.btn_imagenes.clicked.connect(self.seleccionar_imagenes)
        
        imagenes_layout.addWidget(self.label_imagenes)
        imagenes_layout.addWidget(self.btn_imagenes)
        grupo_imagenes.setLayout(imagenes_layout)
        
        # Sección para comenzar la conversión - Grupo 3
        grupo_conversion = QGroupBox("Paso 3: Iniciar conversión")
        conversion_layout = QVBoxLayout()
        
        self.btn_convertir = QPushButton("Convertir Imágenes a PDF")
        self.btn_convertir.clicked.connect(self.iniciar_conversion)
        self.btn_convertir.setEnabled(False)
        conversion_layout.addWidget(self.btn_convertir)
        
        grupo_conversion.setLayout(conversion_layout)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        # Área de log
        log_grupo = QGroupBox("Registro de actividad")
        log_layout = QVBoxLayout()
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        log_layout.addWidget(self.log_area)
        log_grupo.setLayout(log_layout)
        
        # Añadir widgets al layout principal
        main_layout.addWidget(grupo_evento)
        main_layout.addWidget(grupo_excel)
        main_layout.addWidget(grupo_imagenes)
        main_layout.addWidget(grupo_conversion)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(log_grupo)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Atributos para los archivos y eventos
        self.archivo_excel = ""
        self.directorio_base = os.path.dirname(os.path.abspath(__file__))
        self.directorio_eventos = os.path.join(self.directorio_base, "eventos")
        
        # Crear directorio de eventos si no existe
        if not os.path.exists(self.directorio_eventos):
            os.makedirs(self.directorio_eventos)
            self.log_mensaje(f"✅ Directorio de eventos creado: {self.directorio_eventos}")
        
        # Cargar eventos existentes
        self.cargar_eventos_disponibles()
        
    def seleccionar_excel(self):
        opciones = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo Excel", "",
            "Archivos Excel (*.xlsx *.xls);;Todos los archivos (*)", options=opciones
        )
        
        if archivo:
            self.archivo_excel = archivo
            self.label_excel.setText(f"Archivo Excel: {os.path.basename(archivo)}")
            self.actualizar_estado_btn_convertir()
            self.log_mensaje(f"📄 Archivo Excel seleccionado: {archivo}")
    
    def seleccionar_imagenes(self):
        opciones = QFileDialog.Options()
        archivos, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar imágenes PNG", "",
            "Imágenes PNG (*.png);;Todos los archivos (*)", options=opciones
        )
        
        if archivos:
            self.imagenes_seleccionadas = archivos
            self.label_imagenes.setText(f"Imágenes seleccionadas: {len(archivos)}")
            self.actualizar_estado_btn_convertir()
            self.log_mensaje(f"🖼️ {len(archivos)} imágenes PNG seleccionadas")
    
    def cargar_eventos_disponibles(self):
        """Cargar los eventos disponibles en el directorio de eventos"""
        # Guardar el evento actual si se está escribiendo
        nuevo_evento = self.input_evento.text().strip()
        
        # Limpiar el combobox
        self.combo_eventos.clear()
        
        # Añadir opción para nuevo evento
        self.combo_eventos.addItem("-- Crear nuevo evento --")
        
        # Obtener lista de directorios en la carpeta de eventos
        if os.path.exists(self.directorio_eventos):
            eventos = [d for d in os.listdir(self.directorio_eventos) 
                    if os.path.isdir(os.path.join(self.directorio_eventos, d))]
            
            # Añadir eventos existentes al combo
            for evento in sorted(eventos):
                self.combo_eventos.addItem(evento)
            
            if eventos:
                self.log_mensaje(f"📂 Se encontraron {len(eventos)} eventos existentes")
            else:
                self.log_mensaje("📂 No se encontraron eventos previos")
        
        # Si hay un nuevo evento escrito, seleccionarlo
        if nuevo_evento:
            index = self.combo_eventos.findText(nuevo_evento)
            if index >= 0:
                self.combo_eventos.setCurrentIndex(index)
            else:
                self.input_evento.setText(nuevo_evento)  # Mantener el texto
    
    def cambiar_evento(self):
        """Manejar cambio de evento seleccionado"""
        seleccion = self.combo_eventos.currentText()
        
        # Si es "crear nuevo", no hacer nada
        if seleccion == "-- Crear nuevo evento --":
            self.input_evento.clear()
            self.input_evento.setFocus()
            return
        
        # Si es un evento existente, cargar su nombre
        self.input_evento.setText(seleccion)
        self.nombre_evento = seleccion
        self.log_mensaje(f"📂 Evento seleccionado: {seleccion}")
    
    def actualizar_estado_btn_convertir(self):
        # Habilitar el botón de conversión solo si hay Excel, imágenes y nombre de evento
        tiene_evento = bool(self.input_evento.text().strip())
        self.btn_convertir.setEnabled(bool(self.archivo_excel and self.imagenes_seleccionadas and tiene_evento))
    
    def log_mensaje(self, mensaje):
        self.log_area.append(mensaje)
        # Desplazar al final del texto
        cursor = self.log_area.textCursor()
        cursor.movePosition(cursor.End)
        self.log_area.setTextCursor(cursor)
    
    def iniciar_conversion(self):
        if not self.archivo_excel:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un archivo Excel primero.")
            return
            
        if not self.imagenes_seleccionadas:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar al menos una imagen PNG.")
            return
        
        # Obtener nombre del evento desde el campo de entrada
        self.nombre_evento = self.input_evento.text().strip()
        if not self.nombre_evento:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar un nombre para el evento o categoría.")
            return
        
        # Crear estructura de directorios para el evento
        directorio_evento = os.path.join(self.directorio_eventos, self.nombre_evento)
        dir_csv = os.path.join(directorio_evento, "csv")
        dir_imagenes = os.path.join(directorio_evento, "imagenes")
        dir_pdfs = os.path.join(directorio_evento, "PDFs")
        
        # Crear directorios si no existen
        for directorio in [directorio_evento, dir_csv, dir_imagenes, dir_pdfs]:
            if not os.path.exists(directorio):
                os.makedirs(directorio)
                self.log_mensaje(f"✅ Directorio creado: {os.path.relpath(directorio, self.directorio_base)}")
        
        # Copiar las imágenes seleccionadas a la carpeta de imágenes del evento
        self.log_mensaje(f"🖼️ Copiando imágenes a la carpeta '{os.path.join(self.nombre_evento, 'imagenes')}'...")
        for ruta_imagen in self.imagenes_seleccionadas:
            nombre_archivo = os.path.basename(ruta_imagen)
            ruta_destino = os.path.join(dir_imagenes, nombre_archivo)
            try:
                shutil.copy2(ruta_imagen, ruta_destino)
                self.log_mensaje(f"✅ Copiada: {nombre_archivo}")
            except Exception as e:
                self.log_mensaje(f"❌ Error al copiar {nombre_archivo}: {str(e)}")
        
        # Actualizar la lista de eventos
        self.cargar_eventos_disponibles()
        
        # Desactivar botones durante la conversión
        self.btn_excel.setEnabled(False)
        self.btn_imagenes.setEnabled(False)
        self.btn_convertir.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Crear y ejecutar el hilo de conversión
        self.thread = ConvertidorThread(self.archivo_excel, self.nombre_evento, self.directorio_eventos)
        self.thread.progreso.connect(self.actualizar_progreso)
        self.thread.log.connect(self.log_mensaje)
        self.thread.finalizado.connect(self.proceso_finalizado)
        self.thread.start()
    
    def actualizar_progreso(self, valor):
        self.progress_bar.setValue(valor)
    
    def proceso_finalizado(self, exito):
        # Reactivar botones
        self.btn_excel.setEnabled(True)
        self.btn_convertir.setEnabled(True)
        
        if exito:
            QMessageBox.information(self, "Éxito", "Proceso completado correctamente.")
        else:
            QMessageBox.critical(self, "Error", "Hubo errores en el proceso. Revise el log.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
