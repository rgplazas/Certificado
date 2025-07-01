"""
Editor de imágenes para CertManager Pro
Implementa herramientas básicas de ajuste de imágenes: rotación y recorte
"""
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                           QScrollArea, QWidget, QSizePolicy, QRubberBand, QToolBar,
                           QAction, QMessageBox, QDialogButtonBox, QFileDialog, QSpacerItem)
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QTransform, QPainter, QPen, QColor, QImage
from PIL import Image, ImageQt

class EditorImagenDialog(QDialog):
    """Diálogo para editar una imagen: rotar y recortar"""
    
    def __init__(self, ruta_imagen, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editor de Imagen")
        self.setMinimumSize(800, 600)
        self.setModal(True)
        
        # Propiedades de la imagen
        self.ruta_imagen_original = ruta_imagen
        self.imagen_original = QPixmap(ruta_imagen)
        self.imagen_actual = self.imagen_original.copy()
        self.angulo_rotacion = 0
        self.modo_recorte = False
        self.punto_inicio_recorte = None
        self.punto_fin_recorte = None
        self.rubber_band = None
        self.area_recorte = None
        self.seleccion_activa = False  # Indica si hay una selección activa
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Crear barra de herramientas
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.setIconSize(QSize(24, 24))
        
        # Acciones de rotación
        accion_rotar_izq = QAction(QIcon(), "Rotar 90° ↺", self)
        accion_rotar_izq.triggered.connect(lambda: self.rotar_imagen(-90))
        toolbar.addAction(accion_rotar_izq)
        
        accion_rotar_der = QAction(QIcon(), "Rotar 90° ↻", self)
        accion_rotar_der.triggered.connect(lambda: self.rotar_imagen(90))
        toolbar.addAction(accion_rotar_der)
        
        toolbar.addSeparator()
        
        # Acciones de recorte
        self.accion_recortar = QAction(QIcon(), "Modo recorte ✂", self)
        self.accion_recortar.setCheckable(True)
        self.accion_recortar.toggled.connect(self.activar_modo_recorte)
        toolbar.addAction(self.accion_recortar)
        
        self.accion_aplicar_recorte = QAction(QIcon(), "Aplicar recorte", self)
        self.accion_aplicar_recorte.setEnabled(False)
        self.accion_aplicar_recorte.triggered.connect(self.aplicar_recorte)
        toolbar.addAction(self.accion_aplicar_recorte)
        
        toolbar.addSeparator()
        
        # Acción para restablecer la imagen
        accion_restablecer = QAction(QIcon(), "Restablecer", self)
        accion_restablecer.triggered.connect(self.restablecer_imagen)
        toolbar.addAction(accion_restablecer)
        
        # Añadir la barra de herramientas al layout
        layout.addWidget(toolbar)
        
        # Área de desplazamiento para la imagen
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # Widget contenedor para la imagen
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        
        # Label para la imagen
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMouseTracking(True)
        self.image_label.mousePressEvent = self.mouse_press_event
        self.image_label.mouseMoveEvent = self.mouse_move_event
        self.image_label.mouseReleaseEvent = self.mouse_release_event
        
        # Actualizar la imagen mostrada
        self.actualizar_imagen()
        
        # Añadir widgets a los layouts
        content_layout.addWidget(self.image_label)
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # Botones de acción
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.guardar_imagen)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Información de ayuda
        info_label = QLabel("💡 Herramientas disponibles: rotación y recorte")
        info_label.setStyleSheet("color: #666; font-style: italic;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
    
    def actualizar_imagen(self):
        """Actualiza la imagen mostrada en el label"""
        scaled_pixmap = self.imagen_actual.scaled(
            self.content_widget.width() - 20, 
            self.content_widget.height() - 20,
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
    
    def rotar_imagen(self, angulo):
        """Rota la imagen el ángulo especificado en grados"""
        # Actualizar el ángulo total de rotación
        self.angulo_rotacion = (self.angulo_rotacion + angulo) % 360
        
        # Aplicar la transformación
        transform = QTransform().rotate(angulo)
        self.imagen_actual = self.imagen_actual.transformed(transform)
        
        # Actualizar la imagen mostrada
        self.actualizar_imagen()
        
        # Mostrar mensaje informativo
        mensaje = f"⚙️ Imagen rotada {angulo}°"
        
        # Crear un label temporal que se mostrará y desaparecerá
        info_label = QLabel(mensaje, self)
        info_label.setStyleSheet("color: #3498db; background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        info_label.setAlignment(Qt.AlignCenter)
        
        # Posicionarlo en la parte inferior
        info_label.setGeometry(10, self.height() - 40, self.width() - 20, 30)
        info_label.show()
        
        # Configurar temporizador para ocultar
        timer = QTimer(self)
        timer.singleShot(2000, info_label.hide)
    
    def activar_modo_recorte(self, activado):
        """Activa o desactiva el modo de recorte"""
        self.modo_recorte = activado
        
        if activado:
            # Mostrar mensaje de instrucciones al activar el modo recorte
            info_label = QLabel("\ud83d\udc40 Modo recorte activado: Haz clic y arrastra para seleccionar el área", self)
            info_label.setStyleSheet("color: green; background-color: rgba(240, 240, 240, 0.8); padding: 8px; border-radius: 5px;")
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setGeometry(10, self.height() - 50, self.width() - 20, 40)
            info_label.show()
            
            # Configurar temporizador para ocultar
            timer = QTimer(self)
            timer.singleShot(4000, info_label.hide)
        
        # Si se desactiva el modo recorte, limpiar la selección
        if not activado:
            # Limpiar la selección anterior
            if self.rubber_band:
                self.rubber_band.hide()
            self.punto_inicio_recorte = None
            self.punto_fin_recorte = None
            self.area_recorte = None
            self.seleccion_activa = False
            self.accion_aplicar_recorte.setEnabled(False)
    
    def mouse_press_event(self, event):
        """Maneja el evento de presionar el botón del ratón"""
        if self.modo_recorte and event.button() == Qt.LeftButton:
            # Si ya hay una selección activa, ocultarla
            if self.seleccion_activa and self.rubber_band:
                self.rubber_band.hide()
                self.seleccion_activa = False
            
            # Guardar punto de inicio
            self.punto_inicio_recorte = event.pos()
            self.punto_fin_recorte = None
            
            # Crear el rubber band si no existe
            if not self.rubber_band:
                self.rubber_band = QRubberBand(QRubberBand.Rectangle, self.image_label)
            
            # Inicializar en el punto de inicio
            self.rubber_band.setGeometry(QRect(self.punto_inicio_recorte, QSize()))
            self.rubber_band.show()
    
    def mouse_move_event(self, event):
        """Maneja el evento de mover el ratón"""
        if self.modo_recorte and self.rubber_band and self.punto_inicio_recorte:
            # Actualizar tamaño del rubber band
            self.punto_fin_recorte = event.pos()
            self.rubber_band.setGeometry(QRect(self.punto_inicio_recorte, self.punto_fin_recorte).normalized())
    
    def mouse_release_event(self, event):
        """Maneja el evento de soltar el botón del ratón"""
        if self.modo_recorte and event.button() == Qt.LeftButton and self.rubber_band and self.punto_inicio_recorte:
            # Guardar el punto final
            self.punto_fin_recorte = event.pos()
            
            # Guardar el área de recorte
            self.area_recorte = QRect(self.punto_inicio_recorte, self.punto_fin_recorte).normalized()
            
            # Habilitar el botón de aplicar recorte si el área es válida
            if self.area_recorte.width() > 10 and self.area_recorte.height() > 10:
                self.accion_aplicar_recorte.setEnabled(True)
                self.seleccion_activa = True  # Marcar que hay una selección activa
                
                # Asegurar que el rubber band permanece visible
                self.rubber_band.setGeometry(self.area_recorte)
                self.rubber_band.show()
                
                # Mostrar mensaje informativo
                info_label = QLabel(f"\u2702 Área seleccionada: {self.area_recorte.width()}x{self.area_recorte.height()} px. \n¡Haz clic en 'Aplicar recorte' para recortar!", self)
                info_label.setStyleSheet("color: #3498db; background-color: rgba(240, 240, 240, 0.8); padding: 8px; border-radius: 5px; font-weight: bold;")
                info_label.setAlignment(Qt.AlignCenter)
                info_label.setGeometry(10, 10, self.width() - 20, 40)
                info_label.show()
                
                # Configurar temporizador para ocultar el mensaje
                timer = QTimer(self)
                timer.singleShot(4000, info_label.hide)
            else:
                # Si el área es muy pequeña, cancelar la selección
                self.accion_aplicar_recorte.setEnabled(False)
                if self.rubber_band:
                    self.rubber_band.hide()
                self.punto_inicio_recorte = None
                self.punto_fin_recorte = None
                self.area_recorte = None
                self.seleccion_activa = False
    
    def aplicar_recorte(self):
        """Aplica el recorte a la imagen actual"""
        if self.area_recorte:
            # Obtener dimensiones y posiciones actuales
            pixmap_mostrado = self.image_label.pixmap()
            pixmap_original = self.imagen_actual
            label_rect = self.image_label.rect()
            
            # Calcular la posición real de la imagen dentro del label
            # (puede haber espacios vacíos debido a KeepAspectRatio)
            imagen_mostrada_w = pixmap_mostrado.width()
            imagen_mostrada_h = pixmap_mostrado.height()
            label_w = label_rect.width()
            label_h = label_rect.height()
            
            # Calcular offset debido al centrado de la imagen en el label
            offset_x = max(0, (label_w - imagen_mostrada_w) // 2)
            offset_y = max(0, (label_h - imagen_mostrada_h) // 2)
            
            # Ajustar las coordenadas del recorte considerando el offset
            rect_x = self.area_recorte.x() - offset_x
            rect_y = self.area_recorte.y() - offset_y
            
            # Asegurarse de que las coordenadas están dentro de la imagen mostrada
            rect_x = max(0, rect_x)
            rect_y = max(0, rect_y)
            
            # Factores de escala entre la imagen mostrada y la original
            x_scale = pixmap_original.width() / imagen_mostrada_w
            y_scale = pixmap_original.height() / imagen_mostrada_h
            
            # Calcular coordenadas en la imagen original
            x = int(rect_x * x_scale)
            y = int(rect_y * y_scale)
            w = int(self.area_recorte.width() * x_scale)
            h = int(self.area_recorte.height() * y_scale)
            
            # Asegurarse de que las dimensiones son válidas
            x = max(0, min(x, pixmap_original.width() - 1))
            y = max(0, min(y, pixmap_original.height() - 1))
            w = min(w, pixmap_original.width() - x)
            h = min(h, pixmap_original.height() - y)
            
            # Mostrar información de depuración
            print(f"Recorte: x={x}, y={y}, w={w}, h={h} | Original: {pixmap_original.width()}x{pixmap_original.height()}")
            
            # Recortar la imagen
            if w > 0 and h > 0:
                try:
                    self.imagen_actual = pixmap_original.copy(x, y, w, h)
                except Exception as e:
                    print(f"Error al recortar: {e}")
            else:
                print("Dimensiones de recorte inválidas")
                return
            
            # Limpiar el rubber band y la selección
            if self.rubber_band:
                self.rubber_band.hide()
            
            # Desactivar el modo recorte y limpiar todas las variables relacionadas
            self.accion_recortar.setChecked(False)
            self.modo_recorte = False
            self.punto_inicio_recorte = None
            self.punto_fin_recorte = None
            self.area_recorte = None
            self.seleccion_activa = False
            self.accion_aplicar_recorte.setEnabled(False)
            
            # Actualizar la imagen mostrada
            self.actualizar_imagen()
            
            # Mostrar mensaje informativo de éxito con más detalles
            mensaje_recorte = f"✅ Imagen recortada con éxito a {self.imagen_actual.width()}x{self.imagen_actual.height()} px"
            info_label = QLabel(mensaje_recorte, self)
            info_label.setStyleSheet("color: green; background-color: rgba(240, 240, 240, 0.9); padding: 8px; border-radius: 5px; font-weight: bold;")
            info_label.setAlignment(Qt.AlignCenter)
            
            # Centrar el mensaje en la parte superior
            info_label.setGeometry(10, 10, self.width() - 20, 40)
            
            # Mostrar temporalmente y luego ocultar
            timer = QTimer(self)
            timer.singleShot(3000, info_label.hide)
            
            # Mostrar el label
            info_label.show()
    
    def restablecer_imagen(self):
        """Restablece la imagen a su estado original"""
        self.imagen_actual = self.imagen_original.copy()
        self.angulo_rotacion = 0
        self.actualizar_imagen()
        
        # Limpiar el modo recorte
        if self.rubber_band:
            self.rubber_band.hide()
            self.rubber_band = None
        
        self.accion_recortar.setChecked(False)
        self.modo_recorte = False
        self.punto_inicio_recorte = None
        self.area_recorte = None
        self.accion_aplicar_recorte.setEnabled(False)
        
        # Mostrar mensaje informativo
        mensaje = "🔄 Imagen restablecida a su estado original"
        
        # Crear un label temporal que se mostrará y desaparecerá
        info_label = QLabel(mensaje, self)
        info_label.setStyleSheet("color: #e67e22; background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        info_label.setAlignment(Qt.AlignCenter)
        
        # Posicionarlo en la parte inferior
        info_label.setGeometry(10, self.height() - 40, self.width() - 20, 30)
        info_label.show()
        
        # Configurar temporizador para ocultar
        timer = QTimer(self)
        timer.singleShot(2000, info_label.hide)
    
    def guardar_imagen(self):
        """Guarda la imagen editada y cierra el diálogo"""
        # Obtener el directorio y nombre del archivo original
        directorio = os.path.dirname(self.ruta_imagen_original)
        nombre_base = os.path.basename(self.ruta_imagen_original)
        nombre_sin_extension, extension = os.path.splitext(nombre_base)
        
        # Si ya es una imagen editada, no añadir otro sufijo "_editada"
        if "_editada" in nombre_sin_extension:
            nuevo_nombre = f"{nombre_base}"
        else:
            nuevo_nombre = f"{nombre_sin_extension}_editada{extension}"
            
        nueva_ruta = os.path.join(directorio, nuevo_nombre)
        
        # Usar método simplificado para guardar la imagen
        try:
            # Método 1: Guardar directamente con QPixmap
            if self.imagen_actual.save(nueva_ruta, "PNG"):
                # Éxito al guardar directamente
                pass
            else:
                # Método 2: Convertir a QImage y luego guardar
                imagen_qimage = self.imagen_actual.toImage()
                if imagen_qimage.save(nueva_ruta, "PNG"):
                    pass
                else:
                    # Método 3: Usar PIL como último recurso
                    temp_path = os.path.join(directorio, "temp_save_image.png")
                    self.imagen_actual.save(temp_path, "PNG")
                    imagen_pil = Image.open(temp_path)
                    imagen_pil.save(nueva_ruta, "PNG")
                    try:
                        os.remove(temp_path)  # Eliminar archivo temporal
                    except:
                        pass
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar la imagen: {str(e)}")
            return
        
        # Mostrar mensaje de éxito
        QMessageBox.information(
            self, 
            "Imagen guardada", 
            f"La imagen ha sido guardada como:\n{nuevo_nombre}"
        )
        
        # Retornar la ruta de la nueva imagen
        self.nueva_ruta_imagen = nueva_ruta
        self.accept()
    
    def resizeEvent(self, event):
        """Actualiza la imagen cuando se redimensiona el diálogo"""
        self.actualizar_imagen()
        super().resizeEvent(event)
