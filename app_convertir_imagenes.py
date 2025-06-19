import os
import sys
import shutil
import pandas as pd
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QFileDialog, QWidget, 
                            QProgressBar, QMessageBox, QTextEdit, QGroupBox,
                            QLineEdit, QComboBox, QScrollArea, QFrame, QGridLayout,
                            QSizePolicy, QSpacerItem, QTabWidget, QToolButton,
                            QStatusBar, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QDesktopServices
from PIL import Image, ImageQt

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

# Estilos para la interfaz moderna
COLOR_PRIMARY = "#3498db"  # Azul
COLOR_SECONDARY = "#2ecc71"  # Verde
COLOR_BACKGROUND = "#f5f5f5"  # Gris claro
COLOR_TEXT = "#333333"  # Casi negro
COLOR_WARNING = "#e67e22"  # Naranja
COLOR_ERROR = "#e74c3c"  # Rojo
COLOR_SUCCESS = "#27ae60"  # Verde oscuro

# Estilos para tema oscuro
COLOR_DARK_PRIMARY = "#2980b9"  # Azul oscuro
COLOR_DARK_SECONDARY = "#27ae60"  # Verde oscuro
COLOR_DARK_BACKGROUND = "#2c3e50"  # Azul grisáceo oscuro
COLOR_DARK_TEXT = "#ecf0f1"  # Blanco grisáceo

BUTTON_STYLE = """
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QPushButton:pressed {
        background-color: #1c6ea4;
    }
    QPushButton:disabled {
        background-color: #bdc3c7;
        color: #7f8c8d;
    }
"""

ACTION_BUTTON_STYLE = """
    QPushButton {
        background-color: #2ecc71;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #27ae60;
    }
    QPushButton:pressed {
        background-color: #1e8449;
    }
    QPushButton:disabled {
        background-color: #bdc3c7;
        color: #7f8c8d;
    }
"""

GROUPBOX_STYLE = """
    QGroupBox {
        border: 1px solid #bdc3c7;
        border-radius: 6px;
        margin-top: 10px;
        font-weight: bold;
        background-color: #ffffff;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
        color: #3498db;
    }
"""

HEADER_STYLE = """
    QLabel {
        color: #3498db;
        font-weight: bold;
        font-size: 16px;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_dark = False  # Por defecto usar tema claro
        self.initUI()
        self.thread = None
        self.imagenes_seleccionadas = []
        self.nombre_evento = ""
        self.previsualizar_activo = False
        
        # Timer para actualizar el estado
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.actualizar_status)
        self.status_timer.start(3000)  # Actualiza cada 3 segundos
        
        # Inicializar variables adicionales para UX mejorada
        self.ultima_conversion = None
        self.conversion_exitosa = False
        
    def set_application_style(self):
        """Aplica estilos modernos a la aplicación"""
        # Estilo general de la aplicación
        self.setStyleSheet(f"""
            QMainWindow, QDialog, QWidget {{background-color: {COLOR_BACKGROUND};}}
            QLabel {{color: {COLOR_TEXT};}}
            QGroupBox {{font-size: 14px;}}
            QComboBox {{padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;}}
            QLineEdit {{padding: 5px; border: 1px solid #bdc3c7; border-radius: 3px;}}
            QPushButton {{padding: 6px 12px; border-radius: 3px;}}
        """)
    
    def initUI(self):
        self.setWindowTitle("CertManager Pro")
        self.setMinimumSize(800, 600)  # Tamaño un poco más grande para mejor UX
        
        # Establecer icono de la aplicación
        icono_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recursos", "certmanager_icon.ico")
        if os.path.exists(icono_path):
            self.setWindowIcon(QIcon(icono_path))
            
        # Establecer la paleta de colores para toda la aplicación
        self.set_application_style()
        
        # Widget y layout principal
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Sección para seleccionar o crear evento - Grupo 0
        grupo_evento = QGroupBox("🌟 Paso 1: Seleccionar o crear evento/categoría")
        grupo_evento.setStyleSheet(GROUPBOX_STYLE)
        evento_layout = QVBoxLayout()
        
        evento_input_layout = QHBoxLayout()
        self.label_evento = QLabel("Nombre del evento:")
        self.label_evento.setStyleSheet("font-weight: bold;")
        self.input_evento = QLineEdit()
        self.input_evento.setPlaceholderText("Ingrese nombre del evento o categoría")
        self.input_evento.textChanged.connect(self.actualizar_estado_btn_convertir)
        self.btn_cargar_eventos = QPushButton("🔄 Actualizar")
        self.btn_cargar_eventos.setStyleSheet(BUTTON_STYLE)
        self.btn_cargar_eventos.setToolTip("Actualizar la lista de eventos disponibles")
        self.btn_cargar_eventos.clicked.connect(self.cargar_eventos_disponibles)
        evento_input_layout.addWidget(self.label_evento)
        evento_input_layout.addWidget(self.input_evento)
        evento_input_layout.addWidget(self.btn_cargar_eventos)
        
        evento_lista_layout = QHBoxLayout()
        self.label_eventos = QLabel("Eventos existentes:")
        self.label_eventos.setStyleSheet("font-weight: bold;")
        self.combo_eventos = QComboBox()
        self.combo_eventos.setMinimumHeight(30)
        self.combo_eventos.setStyleSheet("font-size: 12px;")
        self.combo_eventos.setToolTip("Seleccione un evento existente para trabajar con él")
        self.combo_eventos.currentIndexChanged.connect(self.cambiar_evento)
        evento_lista_layout.addWidget(self.label_eventos)
        evento_lista_layout.addWidget(self.combo_eventos)
        
        evento_layout.addLayout(evento_input_layout)
        evento_layout.addLayout(evento_lista_layout)
        grupo_evento.setLayout(evento_layout)
        
        # Sección para seleccionar archivo Excel - Grupo 2
        grupo_excel = QGroupBox("📊 Paso 2: Seleccionar archivo Excel")
        grupo_excel.setStyleSheet(GROUPBOX_STYLE)
        excel_layout = QHBoxLayout()
        
        self.label_excel = QLabel("Archivo seleccionado:")
        self.label_excel.setStyleSheet("font-weight: bold;")
        self.path_excel = QLabel("Ninguno")
        self.path_excel.setStyleSheet("font-style: italic; color: #7f8c8d;")
        
        self.btn_excel = QPushButton("📁 Seleccionar Excel")
        self.btn_excel.setStyleSheet(BUTTON_STYLE)
        self.btn_excel.setToolTip("Seleccionar archivo Excel con columnas 'original' y 'nuevo'")
        self.btn_excel.clicked.connect(self.seleccionar_excel)
        
        excel_layout_horizontal = QHBoxLayout()
        excel_layout_horizontal.addWidget(self.btn_excel)
        excel_layout_horizontal.addStretch()
        
        excel_layout.addWidget(self.label_excel)
        excel_layout.addWidget(self.path_excel, 1)  # El 1 da mayor prioridad de espacio
        excel_layout.addLayout(excel_layout_horizontal)
        grupo_excel.setLayout(excel_layout)
        
        # Sección para seleccionar imágenes - Grupo 2
        grupo_imagenes = QGroupBox("🖼️ Paso 3: Seleccionar imágenes PNG")
        grupo_imagenes.setStyleSheet(GROUPBOX_STYLE)
        imagenes_layout = QVBoxLayout()
        
        # Contador de imágenes con estilo
        imagen_contador_layout = QHBoxLayout()
        self.label_imagenes = QLabel("Imágenes seleccionadas:")
        self.label_imagenes.setStyleSheet("font-weight: bold;")
        self.contador_imagenes = QLabel("0")
        self.contador_imagenes.setStyleSheet("color: #3498db; font-weight: bold; font-size: 14px;")
        imagen_contador_layout.addWidget(self.label_imagenes)
        imagen_contador_layout.addWidget(self.contador_imagenes)
        imagen_contador_layout.addStretch()
        
        # Botón para seleccionar imágenes
        self.btn_imagenes = QPushButton("🖼️ Seleccionar Imágenes PNG")
        self.btn_imagenes.setStyleSheet(BUTTON_STYLE)
        self.btn_imagenes.setToolTip("Seleccionar una o múltiples imágenes en formato PNG")
        self.btn_imagenes.clicked.connect(self.seleccionar_imagenes)
        
        # Lista para mostrar imágenes seleccionadas
        self.lista_imagenes = QListWidget()
        self.lista_imagenes.setStyleSheet("border: 1px solid #bdc3c7; border-radius: 3px;")
        self.lista_imagenes.setAlternatingRowColors(True)
        self.lista_imagenes.setMaximumHeight(100)
        
        imagenes_layout.addLayout(imagen_contador_layout)
        imagenes_layout.addWidget(self.btn_imagenes)
        imagenes_layout.addWidget(self.lista_imagenes)
        grupo_imagenes.setLayout(imagenes_layout)
        
        # Sección para comenzar la conversión - Grupo 4
        grupo_conversion = QGroupBox("📦 Paso 4: Iniciar conversión")
        grupo_conversion.setStyleSheet(GROUPBOX_STYLE)
        conversion_layout = QVBoxLayout()
        
        # Añadir información de ayuda
        info_label = QLabel("Al hacer clic en el botón, se crearán PDFs para todas las imágenes seleccionadas.")
        info_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        
        # Botón de conversión con estilo destacado
        self.btn_convertir = QPushButton("✨ Convertir Imágenes a PDF ✨")
        self.btn_convertir.setStyleSheet(ACTION_BUTTON_STYLE)
        self.btn_convertir.setMinimumHeight(40)  # Botón más grande
        self.btn_convertir.setToolTip("Procesar todas las imágenes y crear los archivos PDF")
        self.btn_convertir.clicked.connect(self.iniciar_conversion)
        self.btn_convertir.setEnabled(False)
        
        # Añadir layout para la barra de progreso
        progreso_layout = QVBoxLayout()
        progreso_label = QLabel("Progreso:")
        progreso_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                width: 5px;
            }
        """)
        
        progreso_layout.addWidget(progreso_label)
        progreso_layout.addWidget(self.progress_bar)
        
        conversion_layout.addWidget(info_label)
        conversion_layout.addWidget(self.btn_convertir)
        conversion_layout.addLayout(progreso_layout)
        
        grupo_conversion.setLayout(conversion_layout)
        
        # Área de log mejorada
        log_grupo = QGroupBox("📓 Registro de actividad")
        log_grupo.setStyleSheet(GROUPBOX_STYLE)
        log_layout = QVBoxLayout()
        
        # Encabezado del registro
        log_header = QLabel("Historial de operaciones:")
        log_header.setStyleSheet("font-weight: bold;")
        
        # Área de texto para el log con estilos
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background-color: #ffffff;
                font-family: Consolas, Monaco, monospace;
                padding: 5px;
            }
        """)
        
        # Botón para limpiar el log
        btn_limpiar_log = QPushButton("🚮 Limpiar registro")
        btn_limpiar_log.setStyleSheet(BUTTON_STYLE)
        btn_limpiar_log.clicked.connect(lambda: self.log_area.clear())
        
        log_layout.addWidget(log_header)
        log_layout.addWidget(self.log_area)
        log_layout.addWidget(btn_limpiar_log)
        log_grupo.setLayout(log_layout)
        
        # Crear barra de estado
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: #f8f9fa; color: #333333;")
        self.setStatusBar(self.statusBar)
        
        # Añadir widgets al layout principal con proporciones adecuadas
        main_layout.addWidget(grupo_evento, 1)
        main_layout.addWidget(grupo_excel, 1)
        main_layout.addWidget(grupo_imagenes, 2)
        main_layout.addWidget(grupo_conversion, 1)
        main_layout.addWidget(log_grupo, 3)  # El registro ocupa más espacio
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Atributos para los archivos y eventos
        self.archivo_excel = ""
        
        # Usar una ubicación amigable para el usuario (carpeta Documentos)
        try:
            # Obtener la carpeta de documentos del usuario
            documentos_dir = os.path.join(os.path.expanduser("~"), "Documents")
            if not os.path.exists(documentos_dir):
                documentos_dir = os.path.join(os.path.expanduser("~"), "Documentos")  # Para sistemas en español
            
            # Crear directorio de aplicación dentro de Documentos
            app_dir = os.path.join(documentos_dir, "CertManagerPro")
            if not os.path.exists(app_dir):
                os.makedirs(app_dir)
            
            self.directorio_base = app_dir
        except Exception:
            # Si hay algún error, usar directorio local como respaldo
            self.directorio_base = os.path.dirname(os.path.abspath(__file__))
            self.log_mensaje("⚠️ No se pudo acceder a la carpeta Documentos, usando directorio local.")
        
        # Definir directorio de eventos
        self.directorio_eventos = os.path.join(self.directorio_base, "eventos")
        
        # Crear directorio de eventos si no existe
        if not os.path.exists(self.directorio_eventos):
            os.makedirs(self.directorio_eventos)
            self.log_mensaje(f"✅ Directorio de eventos creado: {self.directorio_eventos}")
        else:
            self.log_mensaje(f"📁 Usando directorio de eventos: {self.directorio_eventos}")
        
        # Cargar eventos existentes
        self.cargar_eventos_disponibles()
        
    def seleccionar_excel(self):
        if not self.nombre_evento:
            QMessageBox.warning(self, "Error", "Debe seleccionar o crear un evento primero")
            return
            
        opciones = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo Excel", "",
            "Archivos Excel (*.xlsx *.xls);;Todos los archivos (*)", options=opciones
        )
        
        if archivo:
            try:
                # Verificar si el archivo tiene las columnas necesarias
                df = pd.read_excel(archivo)
                if 'original' not in df.columns or 'nuevo' not in df.columns:
                    QMessageBox.warning(
                        self, "Error", 
                        "El archivo Excel debe tener las columnas 'original' y 'nuevo'"
                    )
                    return
                
                # Guardar referencia al archivo
                self.archivo_excel = archivo
                nombre_archivo = os.path.basename(archivo)
                
                # Actualizar la interfaz con el archivo seleccionado
                self.path_excel.setText(nombre_archivo)
                self.path_excel.setStyleSheet("color: #3498db; font-weight: bold;")
                self.path_excel.setToolTip(archivo)
                
                # Actualizar el estado del botón
                self.actualizar_estado_btn_convertir()
                
                # Mostrar mensaje en el log con estilo y barra de estado
                self.log_area.append(f"<span style='color:#3498db;'>📁 Archivo Excel seleccionado: {nombre_archivo}</span>")
                self.statusBar.showMessage(f"Archivo Excel cargado: {nombre_archivo}", 5000)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al procesar el archivo Excel: {str(e)}")
                self.log_area.append(f"<span style='color:#e74c3c;'>❌ Error: {str(e)}</span>")
    
    def seleccionar_imagenes(self):
        """Permite al usuario seleccionar múltiples imágenes en formato PNG"""
        if not self.nombre_evento:
            QMessageBox.warning(self, "Error", "Debe seleccionar o crear un evento primero")
            return
            
        opciones = QFileDialog.Options()
        archivos, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar Imágenes PNG", "", "Archivos PNG (*.png)", options=opciones
        )
        
        if archivos:
            self.imagenes_seleccionadas = archivos
            # Actualizar el contador
            self.contador_imagenes.setText(str(len(archivos)))
            
            # Actualizar la lista de imágenes
            self.lista_imagenes.clear()
            for archivo in archivos:
                nombre_archivo = os.path.basename(archivo)
                item = QListWidgetItem(nombre_archivo)
                item.setToolTip(archivo)  # Mostrar ruta completa al pasar el mouse
                self.lista_imagenes.addItem(item)
            
            # Habilitar botón de conversión
            self.btn_convertir.setEnabled(True)
            
            # Mostrar mensaje en el log con estilo
            self.log_area.append(f"<span style='color:#2ecc71;'>✅ Se seleccionaron {len(archivos)} imágenes.</span>")
            # Actualizar barra de estado
            self.statusBar.showMessage(f"Listo para procesar {len(archivos)} imágenes", 5000)
    
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
        # Obtener y validar el texto del campo de evento
        nombre_evento = self.input_evento.text().strip()
        tiene_evento = bool(nombre_evento)
        
        # Actualizar la propiedad nombre_evento si hay texto
        if tiene_evento:
            self.nombre_evento = nombre_evento
        
        # Habilitar el botón de conversión solo si hay Excel, imágenes y nombre de evento
        self.btn_convertir.setEnabled(bool(self.archivo_excel and self.imagenes_seleccionadas and tiene_evento))
        
        # Actualizar tooltip del botón de conversión
        if not self.archivo_excel:
            self.btn_convertir.setToolTip("Debe seleccionar un archivo Excel primero")
        elif not self.imagenes_seleccionadas:
            self.btn_convertir.setToolTip("Debe seleccionar al menos una imagen PNG")
        elif not tiene_evento:
            self.btn_convertir.setToolTip("Debe ingresar un nombre para el evento o categoría")
        else:
            self.btn_convertir.setToolTip("Iniciar el proceso de conversión de imágenes a PDF")
    
    def log_mensaje(self, mensaje, tipo='info'):
        """Registra un mensaje en el área de log con formato HTML y colores"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Asignar colores según el tipo de mensaje
        if tipo == 'success':
            color = COLOR_SUCCESS
            icono = "✅" # Marca de verificación verde
        elif tipo == 'error':
            color = COLOR_ERROR
            icono = "❌" # Cruz roja
        elif tipo == 'warning':
            color = COLOR_WARNING
            icono = "⚠️" # Señal de advertencia
        else: # info
            color = COLOR_PRIMARY
            icono = "💬" # Globo de diálogo
            
        # Formato HTML con timestamp
        mensaje_html = f"<span style='color:#7f8c8d; font-size:10px;'>[{timestamp}]</span> "
        mensaje_html += f"<span style='color:{color};'>{icono} {mensaje}</span>"
        
        # Agregar al log y asegurar que se vea la última línea
        self.log_area.append(mensaje_html)
        self.log_area.ensureCursorVisible()
        
        # Actualizar barra de estado para mensajes importantes
        if tipo in ['error', 'warning', 'success']:
            self.statusBar.showMessage(mensaje, 5000)
        # Desplazar al final del texto
        cursor = self.log_area.textCursor()
        cursor.movePosition(cursor.End)
        self.log_area.setTextCursor(cursor)
        
    def iniciar_conversion(self):
        """Iniciar el proceso de conversión de imágenes a PDF"""
        if not self.archivo_excel:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un archivo Excel.")
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
                self.log_mensaje(f"Directorio creado: {os.path.relpath(directorio, self.directorio_base)}", tipo='success')
        
        # Copiar las imágenes seleccionadas a la carpeta de imágenes del evento
        self.log_mensaje(f"Copiando imágenes a la carpeta '{os.path.join(self.nombre_evento, 'imagenes')}'...", tipo='info')
        
        # Contador para estadísticas
        exito_count = 0
        error_count = 0
        
        for ruta_imagen in self.imagenes_seleccionadas:
            nombre_archivo = os.path.basename(ruta_imagen)
            ruta_destino = os.path.join(dir_imagenes, nombre_archivo)
            try:
                shutil.copy2(ruta_imagen, ruta_destino)
                self.log_mensaje(f"Copiada: {nombre_archivo}", tipo='success')
                exito_count += 1
            except Exception as e:
                self.log_mensaje(f"Error al copiar {nombre_archivo}: {str(e)}", tipo='error')
                error_count += 1
        
        # Resumen de la copia
        if error_count == 0:
            self.log_mensaje(f"Todas las imágenes ({exito_count}) se copiaron con éxito", tipo='success')
        else:
            self.log_mensaje(f"Se copiaron {exito_count} imágenes con éxito, {error_count} con errores", tipo='warning')
            
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
        self.thread.finalizado.connect(self.procesar_finalizacion)
        self.thread.start()
        
        # Actualizar la barra de estado
        self.statusBar.showMessage("⏳ Iniciando proceso de conversión...")
    
    def actualizar_progreso(self, valor):
        self.progress_bar.setValue(valor)
    
    def procesar_finalizacion(self, exito):
        """Procesa la finalización del hilo de conversión"""
        self.progress_bar.setValue(100)
        self.btn_convertir.setEnabled(True)
        self.thread = None
        
        # Guardar estado de la última conversión
        self.conversion_exitosa = exito
        self.ultima_conversion = datetime.datetime.now()
        
        if exito:
            # Mensaje con estilo de éxito
            self.log_mensaje("La conversión ha finalizado con éxito.", tipo='success')
            QMessageBox.information(self, "Conversión Completada", "✨ La conversión ha finalizado con éxito. ✨\n\nLos archivos PDF se han guardado en la carpeta del evento.")
            
            # Muestra la ruta de salida en la barra de estado para facilitar la ubicación
            directorio_evento = self.obtener_directorio_evento(self.nombre_evento)
            directorio_pdfs = os.path.join(directorio_evento, "pdfs")
            self.statusBar.showMessage(f"✅ Conversión exitosa! PDFs guardados en: {directorio_pdfs}", 10000)
        else:
            # Mensaje con estilo de error
            self.log_mensaje("Hubo errores en el proceso. Revise el log para más detalles.", tipo='error')
            QMessageBox.critical(self, "Error", "❌ Hubo errores en el proceso. Revise el registro de actividad.")

    def actualizar_status(self):
        """Actualiza la barra de estado con información contextual"""
        # Si hay una conversión exitosa reciente, mostrar mensaje
        if self.conversion_exitosa and self.ultima_conversion:
            tiempo_pasado = datetime.datetime.now() - self.ultima_conversion
            if tiempo_pasado.total_seconds() < 60:  # Menos de un minuto
                self.statusBar.showMessage("✅ La última conversión fue exitosa!")
                return
        
        # Mostrar información contextual según el estado actual
        if self.thread and self.thread.isRunning():
            self.statusBar.showMessage("⏳ Procesando imágenes...")
        elif len(self.imagenes_seleccionadas) > 0:
            self.statusBar.showMessage(f"🖼️ {len(self.imagenes_seleccionadas)} imágenes listas para procesar")
        elif self.archivo_excel:
            self.statusBar.showMessage("📋 Archivo Excel cargado. Seleccione imágenes para continuar.")
        elif self.nombre_evento:
            self.statusBar.showMessage(f"📂 Evento actual: {self.nombre_evento}. Seleccione un archivo Excel.")
        else:
            self.statusBar.showMessage("🔍 Seleccione o cree un evento para comenzar")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
