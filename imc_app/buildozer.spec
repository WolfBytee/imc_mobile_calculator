[app]

# (str) Título da sua aplicação
title = Calculadora de IMC

# (str) Nome do pacote
package.name = imc_wolfbyte

# (str) Domínio do pacote (necessário para empacotamento android/ios)
package.domain = org.wolfbyte.imc

# (str) Diretório do código fonte onde o main.py está
source.dir = .

# (list) Extensões de arquivos a serem incluídas
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (list) Lista de inclusões usando casamento de padrões
source.include_patterns = assets/*,assets/fonts/*.ttf

# (list) Arquivos a serem excluídos
#source.exclude_exts = spec

# (list) Diretórios a serem excluídos
#source.exclude_dirs = tests, bin, venv

# (str) Versão da aplicação
version = 0.1

# (list) Requisitos da aplicação
requirements = python3,kivy,matplotlib,numpy,pillow,kivy_garden.matplotlib

# (str) Ícone da aplicação
icon.filename = %(source.dir)s/assets/images/icone.png

# (list) Orientações suportadas
orientation = portrait

# (bool) Indicação de tela cheia
fullscreen = 1

#
# Configurações específicas do Android
#

android.api = 34

# (int) API mínima que o APK / AAB suportará.
android.minapi = 21

# (list) Arquiteturas Android para as quais construir
android.archs = arm64-v8a, armeabi-v7a

# (bool) Habilita o recurso de backup automático do Android (API >=23)
android.allow_backup = True

# (str) O formato usado para empacotar o app para o modo de lançamento (aab ou apk).
# 'aab' é o formato preferido pela Google Play Store.
android.release_artifact = aab

# android.add_assets = dados_imc.json


[buildozer]

# (int) Nível de log (0 = apenas erro, 1 = info, 2 = debug)
log_level = 2

# (int) Avisar se o buildozer for executado como root (0 = False, 1 = True)
warn_on_root = 1