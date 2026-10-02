[app]

# ─────────────────────────────────────────────
# APPLICATION
# ─────────────────────────────────────────────

title = Neon Cube Rush

package.name = neoncuberush

package.domain = org.neoncuberush

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,ogg

version = 0.1


# ─────────────────────────────────────────────
# DEPENDENCIES
# ─────────────────────────────────────────────

requirements = python3,pygame


# ─────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────

orientation = portrait

fullscreen = 1


# ─────────────────────────────────────────────
# ANDROID PERMISSIONS
# ─────────────────────────────────────────────

android.permissions = VIBRATE


# ─────────────────────────────────────────────
# ANDROID SDK / NDK
# ─────────────────────────────────────────────

android.api = 33

android.sdk = 33

android.minapi = 21

android.ndk = 25b

android.ndk_api = 21


# ─────────────────────────────────────────────
# ARCHITECTURES
# ─────────────────────────────────────────────

android.archs = arm64-v8a,armeabi-v7a


# ─────────────────────────────────────────────
# STORAGE
# ─────────────────────────────────────────────

android.private_storage = True


# ─────────────────────────────────────────────
# LOGCAT
# ─────────────────────────────────────────────

android.logcat_filters = *:S python:D


# ─────────────────────────────────────────────
# PYTHON-FOR-ANDROID
# ─────────────────────────────────────────────

p4a.bootstrap = sdl2

p4a.fork = kivy


[buildozer]

# ─────────────────────────────────────────────
# BUILD CONFIG
# ─────────────────────────────────────────────

log_level = 2

warn_on_root = 1
