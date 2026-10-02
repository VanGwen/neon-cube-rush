[app]

title = Neon Cube Rush
package.name = neoncuberush
package.domain = org.jem
version = 1.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,wav,ogg,mp3,ttf
source.exclude_dirs = tests,bin,.buildozer,__pycache__,.git,.github

# Dependances Python et Pygame
requirements = python3,pygame

# Configuration Android
orientation = portrait
fullscreen = 1

android.permissions = VIBRATE
android.minapi = 21
android.api = 33
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True

# Génération de l'APK
android.release_artifact = apk

# Configuration python-for-android
p4a.branch = master

[buildozer]

log_level = 2
warn_on_root = 1
