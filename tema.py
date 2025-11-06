#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

# --- Rutas base ---
HOME = Path.home()
BASH_THEME = HOME / ".bash_theme"
BASHRC = HOME / ".bashrc"
FASTFETCH_DIR = HOME / ".config" / "fastfetch"
FASTFETCH_CONF = FASTFETCH_DIR / "config.jsonc"
DIRCOLORS_FILE = HOME / ".dircolors"

# --- Temas disponibles ---
THEMES = {
    "ocean": {
        "ps1_color": "38;5;81",  # celeste
        "dircolors": "di=34:ln=36:so=35:pi=33:ex=32",
        "accent": "cyan",
        "logo": "~/.config/fastfetch/ArchP.png",
    },
    "fire": {
        "ps1_color": "38;5;196",  # rojo
        "dircolors": "di=31:ln=35:so=33:pi=33:ex=91",
        "accent": "red",
        "logo": "~/.config/fastfetch/Fire.png",
    },
    "forest": {
        "ps1_color": "38;5;34",  # verde
        "dircolors": "di=32:ln=36:so=33:pi=33:ex=92",
        "accent": "green",
        "logo": "~/.config/fastfetch/Forest.png",
    },
}

# --- Verificación de argumentos ---
if len(sys.argv) < 2:
    print("Uso: theme.py [ocean|fire|forest]")
    sys.exit(1)

theme_name = sys.argv[1].lower()
if theme_name not in THEMES:
    print(f"Tema '{theme_name}' no existe. Opciones: {', '.join(THEMES.keys())}")
    sys.exit(1)

theme = THEMES[theme_name]

# --- Crear carpeta fastfetch si no existe ---
FASTFETCH_DIR.mkdir(parents=True, exist_ok=True)

# --- Actualizar prompt (PS1) ---
ps1_line = f"export PS1='\\[\\033[{theme['ps1_color']}m\\]\\u@\\h:\\w\\$ \\[\\033[0m\\]'"
dircolors_line = f"eval $(dircolors -b {DIRCOLORS_FILE})"

BASH_THEME.write_text(f"{ps1_line}\n{dircolors_line}\n")

# --- Escribir dircolors ---
DIRCOLORS_FILE.write_text(theme["dircolors"])

# --- Asegurar carga en .bashrc ---
bashrc_content = BASHRC.read_text() if BASHRC.exists() else ""
if "source ~/.bash_theme" not in bashrc_content:
    with open(BASHRC, "a") as f:
        f.write("\n# Tema personalizado\nsource ~/.bash_theme\n")

# --- Configuración base de Fastfetch ---
base_config = {
    "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
    "logo": {
        "source": theme["logo"],
        "type": "kitty",
        "height": 16,
        "width": 30,
        "padding": {"top": 8, "left": 3}
    },
    "modules": [
        "os", "kernel", "shell", "cpu", "gpu", "memory"
    ]
}

FASTFETCH_CONF.write_text(json.dumps(base_config, indent=4))

# --- Aplicar inmediatamente ---
os.system(f"source {BASH_THEME}")

print(f"✅ Tema '{theme_name}' aplicado correctamente.")
