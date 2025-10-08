import os
import json
from datetime import datetime, timedelta
from fundamentals.fetch_yf import get_fundamentals_yf

CACHE_DIR = "fundamentals_cache"
CACHE_DAYS = 7  # actualizar cada semana
os.makedirs(CACHE_DIR, exist_ok=True)

# === Funciones internas ===
def _get_cache_path(symbol: str) -> str:
    """Devuelve la ruta del archivo cacheado para un símbolo."""
    return os.path.join(CACHE_DIR, f"{symbol.upper()}.json")


def is_cache_expired(symbol: str) -> bool:
    """Verifica si el cache está vencido o no existe."""
    path = _get_cache_path(symbol)
    if not os.path.exists(path):
        return True
    modified = datetime.fromtimestamp(os.path.getmtime(path))
    return datetime.now() - modified > timedelta(days=CACHE_DAYS)


# === Función principal ===
def get_cached_fundamentals(symbol: str, mode="summary") -> dict:
    """
    Retorna los fundamentales del símbolo, usando cache si está vigente.
    Si el cache no existe o está vencido, descarga nuevos datos desde Yahoo Finance.
    """
    path = _get_cache_path(symbol)

    if not os.path.exists(path) or is_cache_expired(symbol):
        try:
            data = get_fundamentals_yf(symbol, mode=mode)
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✅ Actualizado: {symbol}")
        except Exception as e:
            print(f"⚠️ Error al actualizar {symbol}: {e}")
            # Si hay error y existe cache viejo, lo usamos como fallback
            if os.path.exists(path):
                with open(path, "r") as f:
                    data = json.load(f)
                print(f"📦 Usando cache anterior de {symbol}")
            else:
                data = {}
    else:
        with open(path, "r") as f:
            data = json.load(f)
        print(f"📦 Desde cache: {symbol}")

    return data
