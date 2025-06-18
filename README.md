# CertManager Pro

> Aplicación profesional para la conversión y gestión de certificados en formato PDF, organizada por eventos o categorías.

<p align="center">
  <img src="recursos/certmanager_logo.png" alt="CertManager Pro Logo" width="128">
</p>

## Descripción

CertManager Pro es una aplicación con interfaz gráfica que permite convertir imágenes PNG a documentos PDF, especialmente diseñada para la gestión de certificados. La aplicación organiza los archivos en una estructura jerárquica por eventos o categorías, facilitando el mantenimiento y la gestión de grandes volúmenes de certificados.

![Captura de pantalla de la aplicación](https://via.placeholder.com/700x400?text=CertManager+Pro)

## Características Principales

- **Interfaz gráfica intuitiva en español**
- **Organización por eventos/categorías**
- **Importación desde archivos Excel**
- **Selección múltiple de imágenes**
- **Conversión automática a formato PDF**
- **Seguimiento detallado del proceso**
- **Estructura de carpetas organizada**

## Requisitos del Sistema

- Windows 10/11
- Python 3.8 o superior
- Dependencias (instaladas automáticamente):
  - PyQt5
  - Pandas
  - Pillow (PIL)
  - Openpyxl

## Instalación

### Como aplicación Python

1. Clonar el repositorio o descargar el código fuente
2. Instalar las dependencias:
   ```bash
   pip install PyQt5 pandas openpyxl pillow
   ```
3. Ejecutar la aplicación:
   ```bash
   python app_convertir_imagenes.py
   ```

### Como ejecutable (.exe)

1. Descargar el archivo ejecutable de la sección de [Releases](https://github.com/usuario/conversor-imagenes-pdf/releases)
2. Ejecutar `Conversor_Imagenes_PDF.exe`

## Instrucciones de Uso

1. **Seleccionar o crear un evento/categoría**
   - Ingrese un nombre de evento nuevo, o
   - Seleccione uno existente de la lista desplegable

2. **Seleccionar el archivo Excel**
   - El archivo debe contener al menos dos columnas:
     - `original`: Nombre del archivo de imagen (sin extensión)
     - `nuevo`: Nombre para el archivo PDF generado

3. **Seleccionar imágenes PNG**
   - Seleccione una o múltiples imágenes desde cualquier ubicación
   - Las imágenes serán copiadas a la carpeta del evento

4. **Iniciar conversión**
   - La aplicación procesará las imágenes y generará los PDFs
   - El progreso se mostrará en la barra inferior
   - El registro detallado mostrará el estado de cada operación

## Estructura del Proyecto

```
Certificado/
│
├── app_convertir_imagenes.py     # Archivo principal de la aplicación
│
└── eventos/                      # Directorio raíz de los eventos
    ├── evento1/                  # Carpeta para cada evento/categoría
    │   ├── csv/                  # Archivos CSV generados desde Excel
    │   │   └── imagenes.csv
    │   ├── imagenes/             # Imágenes PNG originales
    │   │   └── (archivos .png)
    │   └── PDFs/                 # PDFs generados
    │       └── (archivos .pdf)
    │
    └── evento2/
        ├── csv/
        ├── imagenes/
        └── PDFs/
```

## Futuras Mejoras

Actualmente estamos trabajando en las siguientes mejoras para próximas versiones:

### Versión 1.1
- [ ] Vista previa de imágenes seleccionadas
- [ ] Opciones de configuración del PDF (resolución, orientación)
- [ ] Funciones de edición básica (rotación, recorte)

### Versión 1.2
- [ ] Gestión avanzada de eventos (duplicar, eliminar, buscar)
- [ ] Previsualización del PDF antes de generar
- [ ] Fusionar múltiples PDFs en un solo documento

### Versión 1.3
- [ ] Temas de interfaz (claro/oscuro)
- [ ] Guardado de configuraciones preferidas
- [ ] Soporte para más formatos de imagen (JPG, TIFF, BMP)

### Versión 2.0
- [ ] Envío de PDFs por correo electrónico
- [ ] Integración con servicios en la nube
- [ ] Procesamiento en paralelo para grandes volúmenes

## Contribuir

Las contribuciones son bienvenidas. Por favor, siga estos pasos:

1. Hacer un fork del repositorio
2. Crear una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de los cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

## Autor

Desarrollado por [Tu Nombre o Empresa] - [tu.email@ejemplo.com]

---

Si encuentra algún problema o tiene alguna sugerencia, no dude en abrir un [issue](https://github.com/usuario/conversor-imagenes-pdf/issues) en el repositorio.
