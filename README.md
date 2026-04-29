# El Guardián - Archivo Digital

Repositorio del diario escolar "El Guardián". Esta página web muestra automáticamente las ediciones guardadas en la carpeta `diarios`.

## 🚀 Despliegue Automático

Este proyecto utiliza **GitHub Actions** para:
1. Escanear la carpeta `diarios`.
2. Generar la base de datos `diarios.json`.
3. Desplegar la web en **GitHub Pages**.

## 📂 Cómo agregar nuevo contenido
1. Sube tus carpetas de diarios y archivos (PDF/JPG/PNG) a la carpeta `diarios/`.
2. Haz un commit y push a la rama `main`.
3. La web se actualizará automáticamente en unos minutos.

## 🛠️ Desarrollo Local
Si deseas verlo localmente:
1. Ejecuta `python scan_diarios.py` para actualizar la lista.
2. Abre `index.html` en tu navegador.
