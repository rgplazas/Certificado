<div align="center">

# CertManager Pro

<img src="recursos/certmanager_logo.png" alt="CertManager Pro Logo" width="180">

### Solución profesional para la gestión y conversión de certificados PDF

[![Versión](https://img.shields.io/badge/Versi%C3%B3n-v1.3.1-blue)](https://github.com/rgplazas/Certificado/releases)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green)](LICENSE)
[![Plataforma](https://img.shields.io/badge/Plataforma-Windows-lightgrey)](#)

</div>

## 💨 ÚLTIMAS ACTUALIZACIONES

### Versión 1.3.2 - Editor de Imágenes Mejorado (Julio 2025)
- ✂️ **Sistema de recorte estable** que mantiene la selección visible después de soltar el ratón
- 🔄 **Compatibilidad mejorada** entre imágenes editadas y conversión a PDF
- 🖼️ **Mejor visualización de imágenes editadas** con indicadores visuales claros
- 📝 **Mensajes informativos durante edición** con detalles sobre dimensiones y acciones
- 🛡️ **Mayor estabilidad** al editar múltiples imágenes consecutivas

### Versión 1.3.1 - Mejoras en la experiencia de usuario (Julio 2025)
- ✅ **Validación mejorada de archivos Excel** con instrucciones detalladas y mensajes claros
- 📂 **Información clara sobre ubicación de archivos** con mensajes detallados sobre dónde se guardan los PDFs
- 💡 **Mensajes informativos mejorados** para guiar al usuario durante todo el proceso
- 🔄 **Actualización de la documentación** con detalles precisos sobre la estructura de archivos

### Versión 1.3.0 - Panel de configuración PDF (Junio 2025)
- ⚙️ **Panel de configuración avanzada de PDF** con opciones para resolución, orientación, márgenes y calidad
- 📸 **Vista previa de imágenes** con miniaturas y visualización a tamaño completo
- 🔧 **Correcciones de estabilidad** con implementación de métodos faltantes y mejoras en la gestión de directorios

### Versión 1.2.0 - Interfaz moderna y mejorada UX (Junio 2025)
- ✨ **Interfaz gráfica completamente rediseñada** con estilos modernos y profesionales
- 💻 **Mejor organización visual** con agrupación lógica de controles y colores temáticos
- 📎 **Lista visual de imágenes seleccionadas** con contador y tooltips informativos
- ℹ️ **Sistema de log mejorado** con formato HTML, colores y iconos para mejor legibilidad
- 📈 **Barra de estado contextual** con información relevante en tiempo real

### Versión 1.1.0 - Almacenamiento mejorado (Mayo 2025)
- 🗽️ **Ubicación de datos optimizada** en la carpeta Documentos del usuario
- 🔑 **Estructura de carpetas persistente** entre sesiones para mejor experiencia

## 🔥 PRÓXIMA VERSIÓN IMPORTANTE

### Versión 2.0.0 - Arquitectura modular y orientada a objetos (En desarrollo)
- 🛠️ **Refactorización completa del código** para mejor mantenimiento y extensibilidad
- 📚 **Arquitectura modular** con separación clara de responsabilidades
- 🔗 **Implementación de patrones de diseño** para mayor robustez y flexibilidad
- ⚡ **Mejor rendimiento** gracias a una arquitectura optimizada
- 🧹 **Código más limpio** facilitando futuras ampliaciones
- 📂 **Organización automática** de archivos por tipos y eventos
- 🔄 **Recarga automática** de eventos disponibles

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
- Espacio adicional: Variable según el volumen de certificados (~5-20 MB por cada 100 certificados)

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

**Almacenamiento de datos y estructura de archivos**:

CertManager Pro organiza sus archivos de forma automática siguiendo esta estructura:

```
C:\Users\[Usuario]\Documents\CertManagerPro\           # Directorio principal
├── Eventos\                                     # Todos los eventos/categorías
    ├── [Nombre del Evento 1]\                    # Un evento específico
    │   ├── csv\                               # Archivos CSV exportados
    │   ├── imagenes\                          # Imágenes originales copiadas
    │   └── PDFs\                              # PDFs generados con nombres nuevos
    ├── [Nombre del Evento 2]\                    # Otro evento
    │   ├── csv\
    │   ├── imagenes\
    │   └── PDFs\
    └── ...
```

- **Estructura automática**: La aplicación crea esta estructura de carpetas automáticamente
- **Persistencia**: Los archivos se conservan entre sesiones para acceso fácil y posterior
- **Copias de seguridad**: Las imágenes originales se copian al directorio del evento (no se modifican las originales)
- **Fácil acceso**: Todos los PDFs generados se guardan en la subcarpeta `PDFs` de cada evento

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
- Se mostrará una ventana con instrucciones detalladas sobre el formato requerido
- **Requisitos del archivo Excel**:
  - Debe contener exactamente estas dos columnas:
    - `original`: Nombres de los archivos de imagen sin la extensión `.png` (deben coincidir con los nombres de las imágenes seleccionadas)
    - `nuevo`: Nombres que tendrán los PDFs generados (nombres de los participantes/certificados)
  - No puede contener celdas vacías ni valores nulos
  - Cada fila representa un certificado a generar

**Ejemplo de archivo Excel válido**:

| original | nuevo           |
|----------|----------------|
| img1     | Juan Pérez     |
| img2     | María González |
| img3     | Carlos Martínez |

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

### Código fuente
```
Certificado/
├─ CertManagerPro.py           # Punto de entrada principal 
├─ app_convertir_imagenes.py   # Núcleo de la aplicación
├─ recursos/                   # Recursos gráficos
│   ├─ certmanager_logo.png
│   ├─ certmanager_icon.ico
│   └─ certmanager_icon.png
├─ README.md                  # Documentación principal
└─ LICENSE                     # Licencia MIT
```

### Almacenamiento de datos (ubicado en Documents)
```
C:\Users\[Usuario]\Documents\CertManagerPro\
└─ eventos/                   # Estructura de datos organizada
    ├─ evento1/                # Carpeta para cada evento
    │   ├─ csv/               # Archivos CSV de nombres
    │   │   └─ imagenes.csv
    │   ├─ imagenes/          # Imágenes PNG originales
    │   └─ PDFs/              # PDFs generados
    ├─ evento2/
    └─ ...
```

> **Nota**: Esta nueva estructura separa el código fuente de los datos generados, mejorando la seguridad y facilitando las copias de seguridad.

## 💡 Historial y Roadmap

### 🗓️ Versiones publicadas

#### Versión 1.3.1 (Julio 2025) - Mejora de validación y feedback
- ✅ Validación mejorada de archivos Excel con instrucciones detalladas
- ✅ Información clara sobre ubicación de archivos generados
- ✅ Documentación actualizada con estructura detallada de directorios

#### Versión 1.3.0 (Junio 2025) - Panel de configuración PDF
- ✅ Vista previa de imágenes con miniaturas y visualización a tamaño completo
- ✅ Panel de configuración avanzada de PDF (resolución, orientación, márgenes)
- ✅ Correcciones de estabilidad en métodos y gestión de directorios

#### Versión 1.2.1 (Junio 2025) - Hotfix
- ✅ Solucionado problema con la validación de nombres de eventos
- ✅ Mejorados tooltips dinámicos con indicaciones contextuales
- ✅ Validación en tiempo real del formulario

#### Versión 1.2.0 (Junio 2025) - Interfaz moderna
- ✅ Interfaz gráfica completamente rediseñada con estilos profesionales
- ✅ Mejor organización visual con agrupación lógica de elementos
- ✅ Lista visual de imágenes seleccionadas con contador
- ✅ Sistema de log mejorado con formato HTML y colores
- ✅ Barra de estado contextual en tiempo real

#### Versión 1.1.0 (Mayo 2025) - Almacenamiento mejorado 
- ✅ Ubicación de datos optimizada en carpeta Documentos
- ✅ Estructura de carpetas persistente entre sesiones
- ✅ Organización automática de archivos por eventos
- ✅ Recarga automática de eventos disponibles

### 💭 Plan de desarrollo

#### Versión 1.4.0 (Planificada para Q3 2025)
- 🔍 Herramientas básicas de ajuste de imágenes (rotación, recorte)
- 📌 Herramientas para duplicar, eliminar y buscar eventos
- 🔎 Previsualización del PDF antes de generar
- 🗞️ Opción para fusionar múltiples PDFs en un solo documento
- 🔍 Filtrado y búsqueda en el registro de actividad

#### Versión 1.5.0 (Planificada para Q4 2025)
- 🎨 Temas de interfaz (claro/oscuro/personalizado)
- 💾 Perfiles de configuración guardados 
- 🌐 Compatibilidad con más formatos de imagen (JPG, TIFF, BMP, etc.)
- 🖼️ Plantillas predefinidas para certificados

### 🔥 Versión 2.0.0 - Arquitectura modular (Q4 2025 - Q1 2026)
- [ ] Refactorización completa a arquitectura modular y orientada a objetos
- [ ] Separación en componentes independientes para mejor mantenimiento
- [ ] Implementación de patrones de diseño avanzados
- [ ] Mayor extensibilidad para futuras funcionalidades

#### Beneficios de la nueva arquitectura:
- **Mantenimiento simplificado**: Cambios en un módulo no afectan a otros
- **Testing más efectivo**: Facilita pruebas unitarias e integración
- **Escalabilidad**: Fácil adición de nuevas características
- **Código reusable**: Componentes reutilizables en futuras aplicaciones
- **Mejor documentación**: Estructura clara que facilita el entendimiento

#### Estructura modular planificada:
```
CertManagerPro/
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias
├── README.md                    # Documentación
├── recursos/                    # Recursos estáticos (imágenes, iconos)
├── src/                         # Código fuente
│   ├── __init__.py
│   ├── config/                  # Configuraciones
│   │   ├── settings.py          # Constantes y configuraciones
│   ├── core/                    # Lógica de negocio
│   │   ├── event_manager.py     # Gestión de eventos
│   │   ├── file_manager.py      # Gestión de archivos
│   │   ├── excel_processor.py   # Procesamiento de Excel
│   │   └── pdf_converter.py     # Conversión de imágenes a PDF
│   ├── gui/                     # Interfaces gráficas
│   │   ├── main_window.py       # Ventana principal
│   │   ├── dialogs/             # Diálogos y ventanas secundarias
│   │   └── widgets/             # Widgets personalizados
│   └── utils/                   # Utilidades
│       ├── logger.py           # Sistema de logging
│       └── validators.py       # Validadores
└── tests/                      # Tests unitarios
```

#### Principales módulos y responsabilidades:

| Módulo | Responsabilidades |
|---------|-------------------|
| **EventManager** | Gestión de eventos, estructura de directorios, listar eventos |
| **FileManager** | Operaciones con archivos, copia de imágenes, gestión de rutas |
| **ExcelProcessor** | Validación y procesamiento de archivos Excel |
| **PDFConverter** | Conversión de imágenes a PDF con configuraciones |
| **MainWindow** | Interfaz principal y coordinación general |
| **Logger** | Sistema de log unificado y formateado |

#### Patrones de diseño a implementar:

- **Observer**: Para notificaciones entre componentes (ej: actualizar UI cuando cambia estado)
- **Strategy**: Para diferentes estrategias de conversión de PDFs
- **Singleton**: Para componentes globales como el logger
- **Factory**: Para crear diferentes tipos de widgets y diálogos
- **Facade**: Para simplificar interacciones complejas con subsistemas

#### Plan de migración gradual:

1. **Fase 1: Preparación** (Agosto 2025)
   - Crear la estructura de directorios base
   - Configurar entorno de desarrollo
   - Definir interfaces de los módulos principales

2. **Fase 2: Extracción de componentes** (Septiembre 2025)
   - Migrar lógica de negocio a módulos independientes
   - Implementar primeros patrones de diseño
   - Mantener compatibilidad con versión anterior

3. **Fase 3: Refactorización de UI** (Octubre 2025)
   - Rediseñar los componentes de interfaz
   - Implementar sistema de comunicación entre módulos
   - Crear primeros tests unitarios

4. **Fase 4: Integración final** (Noviembre 2025)
   - Conectar todos los componentes
   - Pruebas de integración
   - Documentación completa

5. **Fase 5: Lanzamiento** (Diciembre 2025)
   - Versión 2.0.0 estable
   - Migración de datos de versiones anteriores
   - Guía completa para usuarios y desarrolladores

#### Versión 2.1.0 - Productividad profesional (Q1 2026)
- 📧 Envío de PDFs por correo electrónico
- ☁️ Integración con servicios en la nube (Google Drive, Dropbox)
- 💿 Exportación por lotes
- 📈 Panel de estadísticas de procesamiento
- ⏱️ Procesamiento en paralelo para grandes volúmenes
- 🔗 API para integración con otros sistemas

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
