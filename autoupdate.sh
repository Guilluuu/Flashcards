#!/bin/bash

while true; do
    git add .
    git commit -m "Autoupdated"
    git push
    echo "Actualización automática completada."
    sleep 60  # Esperar 60 segundos antes de volver a ejecutar
done
