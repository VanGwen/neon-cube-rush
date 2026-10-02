[app]

# (str) Titre de l'application
title = Mon Application

# (str) Nom du paquet
package.name = monapp

# (str) Domaine du paquet (nécessaire pour Android)
package.domain = org.monentreprise

# (str) Dossier contenant le code source main.py
source.dir = .

# (list) Extensions de fichiers à inclure
source.include_exts = py,png,jpg,kv,atlas

# (list) Dépendances de l'application
# Remarque : python3 est laissé sans version fixe pour éviter les erreurs de compilation
requirements = python3,kivy

# (str) Orientation supportée (portrait, landscape, etc.)
orientation = portrait

# (bool) Indique si l'application doit s'exécuter en plein écran
fullscreen = 0

# (list) Permissions Android (décommentez si nécessaire)
# android.permissions = INTERNET

# (int) Version API cible Android
android.api = 33

# (int) Version API minimale supportée
android.minapi = 21

# (bool) Accepter automatiquement la licence du SDK Android
android.accept_sdk_license = True

# (str) Architectures Android cibles
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Niveau de journalisation (2 = verbeux)
log_level = 2

# (int) Avertir si Buildozer est exécuté en tant que root
warn_on_root = 1
