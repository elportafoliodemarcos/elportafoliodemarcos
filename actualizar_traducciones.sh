#!/bin/bash

# Carpeta de locales
LOCALE_DIR="portafolio/locale"

# Idioma base
BASE_LANG="es"

# Recorre cada idioma excepto el español
for LANG_DIR in $LOCALE_DIR/*; do
    LANG=$(basename $LANG_DIR)
    if [ "$LANG" != "$BASE_LANG" ]; then
        echo "Actualizando traducciones para $LANG..."
        django-admin makemessages -l $LANG -i venv
    fi
done

# Compila todos los mensajes .po a .mo
django-admin compilemessages

echo "Traducciones actualizadas para todos los idiomas."
