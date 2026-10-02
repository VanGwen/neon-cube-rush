[app]

# ─────────────────────────────
# Informations de l'application
# ─────────────────────────────

title = Neon Cube Rush

package.name = neoncuberush

package.domain = org.neoncuberush

version = 0.1


# ─────────────────────────────
# Fichiers du projet
# ─────────────────────────────

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,ogg


# ─────────────────────────────
# Dépendances Python
# ─────────────────────────────

requirements = python3,pygame


# ─────────────────────────────
# Python-for-Android
# ─────────────────────────────

p4a.bootstrap = sdl2


# ─────────────────────────────
# Android
# ─────────────────────────────

orientation = portrait

fullscreen = 1

android.permissions = VIBRATE

android.api = 33

android.minapi = 21

android.ndk = 25b

android.ndk_api = 21

android.archs = arm64-v8a,armeabi-v7a

android.private_storage = True


# ─────────────────────────────
# Logs Android
# ─────────────────────────────

android.logcat_filters = *:S python:D


# ─────────────────────────────
# Buildozer
# ─────────────────────────────

[buildozer]

log_level = 2

warn_on_root = 1
