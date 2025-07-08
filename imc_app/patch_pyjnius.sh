#!/bin/bash

echo "Aplicando patch no pyjnius para corrigir erro 'long'..."

BUILD_PATH=$(find .buildozer/android/platform/build-*/build/other_builds/pyjnius-sdl2/ -type d | head -1)

if [ -z "$BUILD_PATH" ]; then
  echo "Erro: pasta pyjnius não encontrada no buildozer"
  exit 1
fi

# Substitui long por int nos arquivos pxi problemáticos
sed -i 's/isinstance(arg, long)/isinstance(arg, int)/g' $BUILD_PATH/pyjnius/jnius_utils.pxi
sed -i 's/isinstance(arg, long)/isinstance(arg, int)/g' $BUILD_PATH/pyjnius/jnius_conversion.pxi

echo "Patch aplicado com sucesso."
