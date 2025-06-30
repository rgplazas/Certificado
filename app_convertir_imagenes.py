import os
import sys
import pandas as pd
import shutil
import datetime
import platform
import io
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QComboBox, QLineEdit, QGroupBox,
                             QTextEdit, QListWidget, QListWidgetItem, QProgressBar, QMessageBox,
                             QStatusBar, QDialog, QGridLayout, QScrollArea, QSizePolicy,
                             QSpacerItem, QTabWidget, QToolButton)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont, QColor, QPalette, QDesktopServices
from PIL import Image

class ImagenThumbnailWidget(QListWidget):
    """Widget personalizado para mostrar miniaturas de imágenes con vista previa"""
    imagenClicada = pyqtSignal(str)  # Señal para emitir cuando se hace clic en una imagen
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListWidget.IconMode)
        self.setIconSize(QSize(90, 90))  # Imágenes un poco más grandes
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setSpacing(12)  # Más espacio entre items
        self.setGridSize(QSize(120, 140))  # Más espacio para ícono + texto
        self.setWordWrap(True)  # Permitir ajuste de texto
        self.itemDoubleClicked.connect(self.on_item_doble_clic)
        self.setUniformItemSizes(True)
        self.setTextElideMode(Qt.ElideMiddle)  # Truncar en el medio si no cabe
        
        # Mejorar estilo para evitar superposiciones
        self.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin: 8px;
                padding-bottom: 10px; /* Espacio adicional abajo para el texto */
            }
            QListWidget::item:selected {
                background-color: #d6eaf8;
                border: 1px solid #3498db;
            }
        """)
    
    def agregar_imagen(self, ruta_imagen):
        """Agrega una imagen con su miniatura al widget"""
        try:
            nombre_archivo = os.path.basename(ruta_imagen)
            
            # Crear miniatura
            imagen_pil = Image.open(ruta_imagen)
            imagen_pil.thumbnail((80, 80), Image.LANCZOS)
            
            # Convertir imagen PIL a QPixmap usando un buffer de memoria
            buffer = io.BytesIO()
            # Guardar en formato PNG para preservar transparencia si existe
            imagen_pil.save(buffer, format='PNG')
            buffer.seek(0)
            
            # Crear QImage desde los datos binarios y convertir a QPixmap
            qimg = QImage.fromData(buffer.getvalue())
            pixmap = QPixmap.fromImage(qimg)
            
            # Crear item y configurarlo
            item = QListWidgetItem(self)
            item.setIcon(QIcon(pixmap))
            # Acortar nombre para mejor visualización
            nombre_corto = nombre_archivo[:12] + '...' if len(nombre_archivo) > 12 else nombre_archivo
            item.setText(nombre_corto)
            item.setData(Qt.UserRole, ruta_imagen)  # Guardar ruta completa
            item.setToolTip(f"Nombre: {nombre_archivo}\nRuta: {ruta_imagen}\n\nDoble clic para ver en tamaño completo")
            
            # Añadir al widget
            self.addItem(item)
            return True
            
        except Exception as e:
            print(f"Error al cargar miniatura: {str(e)}")
            return False
    
    def on_item_doble_clic(self, item):
        """Emitir señal cuando se hace doble clic en una imagen"""
        ruta_imagen = item.data(Qt.UserRole)
        self.imagenClicada.emit(ruta_imagen)
    
    def limpiar(self):
        """Limpiar todas las miniaturas"""
        self.clear()

class ConfiguracionPDFDialog(QDialog):
    """Diálogo de configuración avanzada para la generación de PDFs"""
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración Avanzada de PDF")
        self.setMinimumWidth(400)
        self.setModal(True)
        
        # Valores por defecto o recibidos
        self.config = config or {
            'resolucion': 100,  # DPI
            'orientacion': 'auto',  # auto, portrait, landscape
            'margen': 5,  # mm
            'calidad': 'normal'  # alta, normal, baja
        }
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Título del panel
        titulo = QLabel("📝 Configuración Avanzada de PDF")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db; padding: 5px;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Descripción
        desc = QLabel("Personaliza cómo se generarán los archivos PDF a partir de tus imágenes.")
        desc.setStyleSheet("color: #7f8c8d; font-style: italic;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Formulario de ajustes
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(15)
        
        # 1. Resolución
        lbl_res = QLabel("Resolución:")
        lbl_res.setStyleSheet("font-weight: bold;")
        self.combo_res = QComboBox()
        self.combo_res.addItems(["72 DPI (Web)", "100 DPI (Estándar)", "150 DPI (Calidad Media)", "300 DPI (Alta Calidad)"])
        res_values = {72: 0, 100: 1, 150: 2, 300: 3}
        self.combo_res.setCurrentIndex(res_values.get(self.config['resolucion'], 1))
        self.combo_res.setStyleSheet("padding: 4px;")
        form_layout.addWidget(lbl_res, 0, 0)
        form_layout.addWidget(self.combo_res, 0, 1)
        
        # 2. Orientación
        lbl_orient = QLabel("Orientación:")
        lbl_orient.setStyleSheet("font-weight: bold;")
        self.combo_orient = QComboBox()
        self.combo_orient.addItems(["Automática", "Vertical (Retrato)", "Horizontal (Paisaje)"])
        orient_values = {'auto': 0, 'portrait': 1, 'landscape': 2}
        self.combo_orient.setCurrentIndex(orient_values.get(self.config['orientacion'], 0))
        self.combo_orient.setStyleSheet("padding: 4px;")
        form_layout.addWidget(lbl_orient, 1, 0)
        form_layout.addWidget(self.combo_orient, 1, 1)
        
        # 3. Márgenes
        lbl_margen = QLabel("Márgenes:")
        lbl_margen.setStyleSheet("font-weight: bold;")
        self.combo_margen = QComboBox()
        self.combo_margen.addItems(["Sin márgenes", "Pequeños (5mm)", "Medianos (10mm)", "Grandes (20mm)"])
        margen_values = {0: 0, 5: 1, 10: 2, 20: 3}
        self.combo_margen.setCurrentIndex(margen_values.get(self.config['margen'], 1))
        self.combo_margen.setStyleSheet("padding: 4px;")
        form_layout.addWidget(lbl_margen, 2, 0)
        form_layout.addWidget(self.combo_margen, 2, 1)
        
        # 4. Calidad de Compresión
        lbl_calidad = QLabel("Calidad:")
        lbl_calidad.setStyleSheet("font-weight: bold;")
        self.combo_calidad = QComboBox()
        self.combo_calidad.addItems(["Alta (más grande)", "Normal", "Económica (más pequeña)"])
        calidad_values = {'alta': 0, 'normal': 1, 'baja': 2}
        self.combo_calidad.setCurrentIndex(calidad_values.get(self.config['calidad'], 1))
        self.combo_calidad.setStyleSheet("padding: 4px;")
        form_layout.addWidget(lbl_calidad, 3, 0)
        form_layout.addWidget(self.combo_calidad, 3, 1)
        
        # Añadir formulario al layout principal
        layout.addLayout(form_layout)
        
        # Información adicional
        info = QLabel("💡 Los cambios se aplicarán a todos los PDFs generados en esta sesión.")
        info.setStyleSheet("font-style: italic; color: #7f8c8d; font-size: 9px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_default = QPushButton("Restaurar Valores")
        btn_default.clicked.connect(self.restaurar_default)
        btn_default.setStyleSheet("""QPushButton { 
            background-color: #ecf0f1; 
            color: #7f8c8d; 
            border: none; 
            padding: 6px 12px; 
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #bdc3c7;
            color: #2c3e50;
        }""")
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setStyleSheet("""QPushButton { 
            background-color: #e74c3c; 
            color: white; 
            border: none; 
            padding: 6px 12px; 
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }""")
        
        btn_save = QPushButton("Guardar Configuración")
        btn_save.setDefault(True)
        btn_save.clicked.connect(self.accept)
        btn_save.setStyleSheet("""QPushButton { 
            background-color: #3498db; 
            color: white; 
            border: none; 
            padding: 8px 16px; 
            border-radius: 3px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }""")
        
        btn_layout.addWidget(btn_default)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        
        layout.addLayout(btn_layout)
        
    def restaurar_default(self):
        """Restaura los valores predeterminados"""
        self.combo_res.setCurrentIndex(1)  # 100 DPI
        self.combo_orient.setCurrentIndex(0)  # Auto
        self.combo_margen.setCurrentIndex(1)  # 5mm
        self.combo_calidad.setCurrentIndex(1)  # Normal
    
    def get_config(self):
        """Obtener la configuración seleccionada"""
        # Mapear índices de combos a valores reales
        res_map = {0: 72, 1: 100, 2: 150, 3: 300}
        orient_map = {0: 'auto', 1: 'portrait', 2: 'landscape'}
        margen_map = {0: 0, 1: 5, 2: 10, 3: 20}
        calidad_map = {0: 'alta', 1: 'normal', 2: 'baja'}
        
        return {
            'resolucion': res_map[self.combo_res.currentIndex()],
            'orientacion': orient_map[self.combo_orient.currentIndex()],
            'margen': margen_map[self.combo_margen.currentIndex()],
            'calidad': calidad_map[self.combo_calidad.currentIndex()]
        }

class VisorImagenDialog(QDialog):
    """Diálogo para mostrar una imagen en tamaño completo"""
    def __init__(self, ruta_imagen, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Vista previa de la imagen")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        # Cargar imagen
        self.pixmap = QPixmap(ruta_imagen)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Área de desplazamiento para la imagen
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Widget contenedor para la imagen
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        
        # Label para la imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ajustar_imagen()
        
        # Botón para cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        
        # Añadir widgets a los layouts
        content_layout.addWidget(self.image_label)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        layout.addWidget(btn_cerrar)
        
    def ajustar_imagen(self):
        """Ajustar la imagen al tamaño del contenedor"""
        # Escalar la imagen manteniendo proporciones
        scaled_pixmap = self.pixmap.scaled(
            self.width() - 30, self.height() - 50,
            Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        
    def resizeEvent(self, event):
        """Reescalar la imagen cuando se redimensiona el diálogo"""
        self.ajustar_imagen()
        super().resizeEvent(event)

class ConvertidorThread(QThread):
    """Hilo para procesar la conversión de imágenes a PDF"""
    progreso = pyqtSignal(int)
    log = pyqtSignal(str)
    finalizado = pyqtSignal(bool)
    
    def __init__(self, archivo_excel, nombre_evento, directorio_eventos, pdf_config=None):
        super().__init__()
        self.archivo_excel = archivo_excel
        self.nombre_evento = nombre_evento
        self.directorio_eventos = directorio_eventos
        # Configuración PDF por defecto si no se proporciona
        self.pdf_config = pdf_config or {
            'resolucion': 100,  # DPI
            'orientacion': 'auto',  # auto, portrait, landscape
            'margen': 5,  # mm
            'calidad': 'normal'  # alta, normal, baja
        }
    
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
                            # Aplicar configuración de orientación si no es automática
                            if self.pdf_config['orientacion'] != 'auto':
                                if self.pdf_config['orientacion'] == 'portrait' and img.width > img.height:
                                    # Rotar si es necesario para formato vertical
                                    img = img.rotate(90, expand=True)
                                elif self.pdf_config['orientacion'] == 'landscape' and img.height > img.width:
                                    # Rotar si es necesario para formato horizontal
                                    img = img.rotate(90, expand=True)
                            
                            # Convertir si es necesario
                            if img.mode in ("RGBA", "P"):
                                img = img.convert("RGB")
                            
                            # Calcular márgenes si son necesarios (en puntos, 1mm = 2.83 puntos)
                            margen_pts = self.pdf_config['margen'] * 2.83 if self.pdf_config['margen'] > 0 else 0
                            
                            # Aplicar calidad según configuración
                            compress_level = 50  # por defecto
                            if self.pdf_config['calidad'] == 'alta':
                                compress_level = 95
                            elif self.pdf_config['calidad'] == 'baja':
                                compress_level = 30
                                
                            # Guardar con la configuración aplicada
                            img.save(
                                ruta_pdf, 
                                "PDF", 
                                resolution=float(self.pdf_config['resolucion']),
                                quality=compress_level)
                            
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
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CertManager Pro')
        self.setMinimumSize(800, 600)
        
        # Inicializar variables
        self.archivo_excel = None
        self.nombre_evento = ""
        self.imagenes_seleccionadas = []
        self.directorio_base = None
        self.directorio_eventos = None
        self.thread = None
        self.previsualizar_activo = False
        
        # Configuración por defecto de PDF
        self.pdf_config = {
            'resolucion': 100,  # DPI
            'orientacion': 'auto',  # auto, portrait, landscape
            'margen': 5,  # mm
            'calidad': 'normal'  # alta, normal, baja
        }
        
        # Inicializar la interfaz
        self.initUI()
        
        # Inicializar directorios
        self.inicializar_directorios()
        
        # Timer para actualizar el estado
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.actualizar_status)
        self.status_timer.start(3000)  # Actualiza cada 3 segundos
        self.ultima_conversion = None
        self.conversion_exitosa = False
        
    def inicializar_directorios(self):
        """Inicializa los directorios necesarios para la aplicación"""
        # Definir directorio base en Documents del usuario
        usuario_home = os.path.expanduser("~")
        self.directorio_base = os.path.join(usuario_home, "Documents", "CertManagerPro")
        
        # Directorio para eventos
        self.directorio_eventos = os.path.join(self.directorio_base, "Eventos")
        
        # Crear directorios si no existen
        for directorio in [self.directorio_base, self.directorio_eventos]:
            if not os.path.exists(directorio):
                os.makedirs(directorio)
                print(f"Directorio creado: {directorio}")
        
        # Actualizar ComboBox con eventos existentes
        self.cargar_eventos_disponibles()
    
    def obtener_directorio_evento(self, nombre_evento):
        """Obtiene la ruta completa al directorio de un evento"""
        return os.path.join(self.directorio_eventos, nombre_evento)
        
    def cargar_eventos_disponibles(self):
        """Carga la lista de eventos disponibles en el ComboBox"""
        # Limpiar el ComboBox
        if hasattr(self, 'combo_eventos'):
            self.combo_eventos.clear()
            
            # Obtener la lista de directorios de eventos
            if os.path.exists(self.directorio_eventos):
                eventos = [d for d in os.listdir(self.directorio_eventos) 
                           if os.path.isdir(os.path.join(self.directorio_eventos, d))]
                
                # Ordenar por fecha de modificación (más reciente primero)
                eventos.sort(key=lambda x: os.path.getmtime(os.path.join(self.directorio_eventos, x)), 
                             reverse=True)
                
                # Añadir al ComboBox
                for evento in eventos:
                    self.combo_eventos.addItem(evento)
                
                if eventos:
                    if hasattr(self, 'log_text'):
                        self.log_mensaje(f"Se cargaron {len(eventos)} eventos existentes", tipo='info')
                    # Seleccionar el evento más reciente
                    self.combo_eventos.setCurrentIndex(0)
                    
    def log_mensaje(self, mensaje, tipo='info'):
        """Añade un mensaje al registro de la aplicación"""
        if hasattr(self, 'log_text'):
            # Obtener fecha y hora actual
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Definir colores para diferentes tipos de mensajes
            color = "#2c3e50"  # Color predeterminado (gris oscuro)
            if tipo == 'error':
                color = "#e74c3c"  # Rojo
                mensaje = f"❌ ERROR: {mensaje}"
            elif tipo == 'warning':
                color = "#f39c12"  # Naranja
                mensaje = f"⚠️ {mensaje}"
            elif tipo == 'success':
                color = "#27ae60"  # Verde
                mensaje = f"✅ {mensaje}"
            elif tipo == 'info':
                color = "#2980b9"  # Azul
                mensaje = f"ℹ️ {mensaje}"
            
            # Crear HTML formateado
            html = f"<span style='color:{color};'>[{timestamp}] {mensaje}</span>"
            
            # Añadir al QTextEdit
            self.log_text.append(html)
            
            # Actualizar barra de estado para mensajes importantes
            if tipo in ['error', 'success']:
                self.statusBar.showMessage(mensaje, 5000)
                
    def actualizar_status(self):
        """Actualiza la barra de estado con información relevante"""
        # Determinar mensaje apropiado
        if self.thread and self.thread.isRunning():
            # Si hay un proceso de conversión activo
            mensaje = "⏳ Conversión en progreso..."
        elif hasattr(self, 'ultima_conversion') and self.ultima_conversion:
            # Tiempo desde la última conversión
            tiempo_transcurrido = datetime.datetime.now() - self.ultima_conversion
            minutos = int(tiempo_transcurrido.total_seconds() / 60)
            
            if self.conversion_exitosa:
                if minutos < 1:
                    mensaje = "✅ Última conversión exitosa hace menos de un minuto"
                else:
                    mensaje = f"✅ Última conversión exitosa hace {minutos} minutos"
            else:
                if minutos < 1:
                    mensaje = "❌ La última conversión falló hace menos de un minuto"
                else:
                    mensaje = f"❌ La última conversión falló hace {minutos} minutos"
        else:
            # Mensaje por defecto
            mensaje = "Listo para conversión → Seleccione Excel e imágenes PNG para comenzar"
            
        # Actualizar barra de estado
        self.statusBar.showMessage(mensaje)
        
    def actualizar_progreso(self, valor):
        """Actualiza la barra de progreso y el estado"""
        # Actualizar barra de progreso
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setValue(valor)
            
            # Actualizar mensaje de estado para valores significativos
            if valor == 0:
                self.statusBar.showMessage("⏳ Iniciando proceso de conversión...")
            elif valor == 100:
                self.statusBar.showMessage("✅ ¡Proceso finalizado!")
            elif valor % 10 == 0:  # Solo actualizar en intervalos de 10%
                self.statusBar.showMessage(f"Progreso: {valor}% completado")
                
            # Mantener la interfaz responsiva
            QApplication.processEvents()
        
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
        
        # Contenedor para miniaturas y su información
        miniaturas_container = QWidget()
        miniaturas_layout = QVBoxLayout(miniaturas_container)
        miniaturas_layout.setContentsMargins(0, 0, 0, 0)
        miniaturas_layout.setSpacing(2)
        
        # Etiqueta informativa para las miniaturas - colocada arriba
        info_miniaturas = QLabel("✨ Doble clic en una imagen para ver en tamaño completo ✨")
        info_miniaturas.setStyleSheet("""
            color: #3498db; 
            font-style: italic; 
            font-size: 9px; 
            background-color: #ecf0f1; 
            border-radius: 2px; 
            padding: 3px;
        """)
        info_miniaturas.setAlignment(Qt.AlignCenter)
        
        # Widget de miniaturas para mostrar imágenes seleccionadas
        self.lista_imagenes = ImagenThumbnailWidget()
        self.lista_imagenes.setMinimumHeight(200)  # Más espacio para las miniaturas
        self.lista_imagenes.imagenClicada.connect(self.mostrar_vista_previa)
        
        # Añadir en orden: primero la etiqueta informativa, luego las miniaturas
        miniaturas_layout.addWidget(info_miniaturas)
        miniaturas_layout.addWidget(self.lista_imagenes)
        
        imagenes_layout.addLayout(imagen_contador_layout)
        imagenes_layout.addWidget(self.btn_imagenes)
        imagenes_layout.addWidget(miniaturas_container)  # Agregar el contenedor que tiene las miniaturas y la etiqueta
        grupo_imagenes.setLayout(imagenes_layout)
        
        # Sección para comenzar la conversión - Grupo 4
        grupo_conversion = QGroupBox("📦 Paso 4: Iniciar conversión")
        grupo_conversion.setStyleSheet(GROUPBOX_STYLE)
        conversion_layout = QVBoxLayout()
        
        # Añadir información de ayuda
        info_label = QLabel("Al hacer clic en el botón, se crearán PDFs para todas las imágenes seleccionadas.")
        info_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        
        # Layout para botones de configuración y conversión
        btn_horizontal_layout = QHBoxLayout()
        
        # Botón de configuración avanzada
        self.btn_config_pdf = QPushButton("⚙️ Configuración Avanzada PDF")
        self.btn_config_pdf.setStyleSheet("""QPushButton { 
            background-color: #f39c12; 
            color: white; 
            border: none; 
            padding: 6px 12px; 
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #d35400;
        }""")
        self.btn_config_pdf.setToolTip("Configurar resolución, orientación y otros ajustes para los PDF generados")
        self.btn_config_pdf.clicked.connect(self.abrir_config_pdf)
        btn_horizontal_layout.addWidget(self.btn_config_pdf)
        
        # Spacer para separar botones
        btn_horizontal_layout.addStretch()
        
        # Botón de conversión con estilo destacado
        self.btn_convertir = QPushButton("✨ Convertir Imágenes a PDF ✨")
        self.btn_convertir.setStyleSheet(ACTION_BUTTON_STYLE)
        self.btn_convertir.setMinimumHeight(40)  # Botón más grande
        self.btn_convertir.setToolTip("Procesar todas las imágenes y crear los archivos PDF")
        self.btn_convertir.clicked.connect(self.iniciar_conversion)
        self.btn_convertir.setEnabled(False)
        btn_horizontal_layout.addWidget(self.btn_convertir)
        
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
        
        # Agregar elementos al layout general
        conversion_layout.addWidget(info_label)
        conversion_layout.addLayout(btn_horizontal_layout)  # Usar el layout horizontal para los botones
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
            
            # Limpiar y actualizar el widget de miniaturas
            self.lista_imagenes.limpiar()
            
            # Indicar que estamos cargando miniaturas
            self.statusBar.showMessage("Cargando miniaturas de las imágenes...")
            QApplication.processEvents()  # Actualizar la interfaz
            
            # Contador para estadísticas
            cargadas = 0
            errores = 0
            
            # Cargar miniaturas de imágenes
            for archivo in archivos:
                if self.lista_imagenes.agregar_imagen(archivo):
                    cargadas += 1
                else:
                    errores += 1
            
            # Habilitar botón de conversión
            self.actualizar_estado_btn_convertir()
            
            # Reportar resultados en el log
            if errores == 0:
                self.log_mensaje(f"Se cargaron {cargadas} miniaturas de imágenes correctamente.", tipo='success')
            else:
                self.log_mensaje(f"Se cargaron {cargadas} miniaturas. Hubo problemas con {errores} imágenes.", tipo='warning')
            
            # Actualizar barra de estado
            self.statusBar.showMessage(f"Listo para procesar {len(archivos)} imágenes | Doble clic para ver una previsualización", 5000)
    
    def mostrar_vista_previa(self, ruta_imagen):
        """Mostrar vista previa de la imagen en tamaño completo"""
        try:
            visor = VisorImagenDialog(ruta_imagen, self)
            visor.exec_()  # Mostrar diálogo modal
        except Exception as e:
            self.log_mensaje(f"Error al mostrar la vista previa: {str(e)}", tipo='error')
    
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
        
    def abrir_config_pdf(self):
        """Abre el diálogo de configuración avanzada de PDF"""
        dialog = ConfiguracionPDFDialog(self, self.pdf_config)
        if dialog.exec_():
            # Actualizar la configuración si el usuario acepta
            self.pdf_config = dialog.get_config()
            self.log_mensaje(f"📝 Configuración PDF actualizada: {self.pdf_config['resolucion']} DPI, "
                       f"orientación {self.pdf_config['orientacion']}, "
                       f"márgenes {self.pdf_config['margen']}mm")
    
    def iniciar_conversion(self):
        """Inicia el proceso de conversión tras validar"""
        if not self.archivo_excel:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un archivo Excel.")
            return
        if not self.imagenes_seleccionadas:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar al menos una imagen PNG.")
            return
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
        self.combo_eventos.setEnabled(False)
        self.input_evento.setEnabled(False)
        self.btn_config_pdf.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Actualizar la barra de estado
        self.statusBar.showMessage("⌛ Iniciando proceso de conversión...")
        
        # Crear el hilo de conversión con la configuración actualizada
        self.thread = ConvertidorThread(self.archivo_excel, self.nombre_evento, self.directorio_eventos, self.pdf_config)
        self.thread.progreso.connect(self.actualizar_progreso)
        self.thread.log.connect(self.log_mensaje)
        self.thread.finalizado.connect(self.procesar_finalizacion)
        self.thread.start()
    
    def procesar_finalizacion(self, exito):
        """Procesa la finalización del hilo de conversión"""
        self.progress_bar.setValue(100)
        self.btn_convertir.setEnabled(True)
        self.btn_excel.setEnabled(True)
        self.btn_imagenes.setEnabled(True)
        self.combo_eventos.setEnabled(True)
        self.input_evento.setEnabled(True)
        self.btn_config_pdf.setEnabled(True)
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
