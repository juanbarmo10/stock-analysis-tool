# 🧩 Stock Analysis Tool

Proyecto para descargar, analizar y visualizar métricas fundamentales de acciones usando `yfinance`, con manejo de caché y visualizaciones limpias.

---

## ⚙️ Estructura del proyecto

project_root/
│
├── fundamentals/
│ ├── init.py
│ ├── fetch_yf.py
│ ├── cache.py
│ ├── metrics.py
│ ├── visualize.py
│
├── main.py
├── requirements.txt
└── environment.yml


## 🧱 Configuración del entorno con Conda

Este proyecto usa **Conda** para manejar dependencias.  
El entorno se llama `binancnv`.

1. Asegúrate de tener el entorno activo:
   
   conda activate binancnv

2. Si se cambia el entorno se exporta sin builds ni prefix antes del add, commit y push:

    conda env export --no-builds | grep -v "prefix:" > environment.yml

3. Para actualizar entorno despues del pull:

    conda env update -f environment.yml --prune



   
