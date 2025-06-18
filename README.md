<div align="center">

# CertManager Pro

<img src="recursos/certmanager_logo.png" alt="CertManager Pro Logo" width="180">

### Solución profesional para la gestión y conversión de certificados PDF

[![Versión](https://img.shields.io/badge/Versi%C3%B3n-v1.0.0-blue)](https://github.com/rgplazas/Certificado/releases)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)
[![Plataforma](https://img.shields.io/badge/Plataforma-Windows-lightgrey)](#)

</div>

## 📋 Descripción

CertManager Pro es una aplicación con interfaz gráfica intuitiva que transforma imágenes PNG en documentos PDF profesionales. Diseñada especialmente para la organización y gestión eficiente de certificados, permite clasificarlos por eventos o categorías en una estructura jerárquica, ideal para instituciones educativas, organizadores de eventos, departamentos de recursos humanos o cualquier entorno que maneje grandes volúmenes de certificados.

## ✨ Características Principales

| Característica | Descripción |
| --- | --- |
| 🌐 **Interfaz intuitiva en español** | Diseño moderno y fácil de usar para todos los usuarios |
| 📁 **Organización por eventos** | Sistema jerárquico para mantener certificados ordenados por eventos o categorías |
| 📊 **Importación desde Excel** | Lectura automática de datos desde hojas de cálculo de Excel |
| 🖼️ **Selección múltiple de imágenes** | Procesa varias imágenes en una sola operación |
| 📄 **Conversión inteligente a PDF** | Ajuste automático de imágenes para generar PDFs de alta calidad |
| 📊 **Seguimiento en tiempo real** | Barra de progreso y registro detallado de cada operación |
| 🗂️ **Estructura organizada** | Carpetas y archivos automáticamente organizados y fáciles de encontrar |

## 💻 Requisitos del Sistema

**Plataforma**: Windows 10/11

**Hardware recomendado**:
- Procesador: 1.5 GHz o superior
- RAM: 2 GB o superior
- Espacio en disco: 100 MB para la aplicación

**Software necesario** (para la versión Python):
- Python 3.8 o superior
- Dependencias:
  ```
  PyQt5>=5.15.0
  pandas>=1.0.0
  Pillow>=8.0.0
  openpyxl>=3.0.0
  ```
  
> **Nota**: La versión ejecutable no requiere ninguna instalación adicional de software.

## 📍 Instalación

### ⏰ Instalación Rápida (Recomendado)

1. Descarga la versión ejecutable desde [GitHub Releases](https://github.com/rgplazas/Certificado/releases/latest)
2. Extrae el archivo ZIP en la ubicación deseada
3. Ejecuta `CertManagerPro.exe`

### ⚙️ Instalación para Desarrollo

1. Clona el repositorio o descarga el código fuente:
   ```bash
   git clone https://github.com/rgplazas/Certificado.git
   cd Certificado
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   # Si no existe requirements.txt:
   pip install PyQt5 pandas openpyxl pillow
   ```

4. Ejecuta la aplicación:
   ```bash
   python CertManagerPro.py
   ```

## 📖 Guía de Uso

### Flujo de Trabajo en 4 Pasos

#### 1⃣ Gestiona Eventos o Categorías

- **Crear nuevo evento**: Escribe un nombre descriptivo en el campo de texto
- **Usar evento existente**: Selecciona uno de la lista desplegable
- **Actualizar lista**: Usa el botón "Actualizar eventos" para refrescar la lista

#### 2⃣ Importa Datos desde Excel

- Haz clic en "Seleccionar Excel"
- El archivo debe contener dos columnas principales:
  - `original`: Identificador de la imagen (sin extensión .png)
  - `nuevo`: Nombre deseado para el PDF de salida
- Formatos soportados: `.xlsx`, `.xls`

#### 3⃣ Selecciona Imágenes

- Haz clic en "Seleccionar Imágenes PNG"
- Puedes seleccionar múltiples imágenes a la vez (Ctrl+clic o Shift+clic)
- Las imágenes seleccionadas se copiarán automáticamente a la carpeta del evento

#### 4⃣ Inicia la Conversión

- Presiona "Convertir Imágenes a PDF" para comenzar el proceso
- Sigue el progreso en la barra inferior y en el registro de actividad
- Los PDFs generados se almacenan en la carpeta `eventos/[evento]/PDFs/`

## 💿 Estructura del Proyecto

```
Certificado/
├── CertManagerPro.py           # Punto de entrada principal 
├── app_convertir_imagenes.py   # Núcleo de la aplicación
├── recursos/                   # Recursos gráficos
│   ├── certmanager_logo.png
│   ├── certmanager_icon.ico
│   └── certmanager_icon.png
├── README.md                  # Documentación principal
├── LICENSE                     # Licencia MIT
└── eventos/                   # Estructura de datos organizada
    ├── evento1/                # Carpeta para cada evento
    │   ├── csv/               # Archivos CSV de nombres
    │   │   └── imagenes.csv
    │   ├── imagenes/          # Imágenes PNG originales
    │   └── PDFs/              # PDFs generados
    ├── evento2/
    └── ...
```

## 💡 Roadmap: Futuras Mejoras

Nuestro plan de desarrollo para CertManager Pro incluye las siguientes mejoras:

### 🟡 Versión 1.1 - Experiencia mejorada
- [ ] Vista previa de imágenes seleccionadas en miniaturas
- [ ] Panel de configuración avanzada de PDF (resolución, orientación)
- [ ] Herramientas básicas de ajuste de imágenes (rotación, recorte, brillo/contraste)

### 🟠 Versión 1.2 - Gestión de eventos
- [ ] Herramientas para duplicar, eliminar y buscar eventos
- [ ] Previsualización del PDF antes de generar
- [ ] Opción para fusionar múltiples PDFs en un solo documento
- [ ] Filtrado y búsqueda en el registro de actividad

### 🟢 Versión 1.3 - Personalización 
- [ ] Temas de interfaz (claro/oscuro/personalizado)
- [ ] Perfiles de configuración guardados
- [ ] Compatibilidad con más formatos de imagen (JPG, TIFF, BMP, etc.)
- [ ] Plantillas predefinidas para certificados

### 🔵 Versión 2.0 - Productividad profesional
- [ ] Envío de PDFs por correo electrónico
- [ ] Integración con servicios en la nube (Google Drive, Dropbox)
- [ ] Procesamiento en paralelo para grandes volúmenes
- [ ] API para integración con otros sistemas

## 📈 Estadísticas

[![GitHub estrellas](https://img.shields.io/github/stars/rgplazas/Certificado?style=social)](https://github.com/rgplazas/Certificado/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rgplazas/Certificado?style=social)](https://github.com/rgplazas/Certificado/network/members)
[![GitHub issues](https://img.shields.io/github/issues/rgplazas/Certificado)](https://github.com/rgplazas/Certificado/issues)

## 🤝 Contribuir

¡Tus contribuciones son bienvenidas y apreciadas! Sí deseas colaborar, por favor:

1. Haz fork del repositorio
2. Crea una rama para tu función: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios: `git commit -am 'Añadir: nueva funcionalidad'`
4. Sube la rama: `git push origin feature/nueva-funcionalidad`
5. Envía un Pull Request

Consulta nuestra [guía de contribución](CONTRIBUTING.md) para más detalles.

## ⚖️ Licencia

Este proyecto está disponible bajo la [Licencia MIT](LICENSE).

## 👨‍💻 Autor

Desarrollado con ❤️ por [Ricardo Gastón Plazas](https://github.com/rgplazas)

---

<div align="center">

¿Encontraste algún error o tienes alguna idea? [Crea un issue](https://github.com/rgplazas/Certificado/issues)

------------------| © 2025

</div>
