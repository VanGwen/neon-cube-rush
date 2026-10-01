[app]

# ── Identité ─────────────────────────────────────────────────────────
title           = Neon Cube Rush
package.name    = neoncuberush
package.domain  = org.jem
version         = 1.0

# ── Sources ──────────────────────────────────────────────────────────
source.dir              = .
source.include_exts     = py,png,jpg,jpeg,json,wav,ogg,mp3,ttf
source.exclude_dirs     = tests,bin,.buildozer,__pycache__,.git,.github

# ── Dépendances Python ───────────────────────────────────────────────
# Pas de version figée sur pygame → p4a choisit la version compatible
requirements = python3==3.11.0,pygame

# ── Icône & splash (ajoute tes fichiers et décommente) ───────────────
# icon.filename      = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

# ── Affichage ────────────────────────────────────────────────────────
orientation = portrait
fullscreen  = 1

# ── Android ──────────────────────────────────────────────────────────
android.permissions         = VIBRATE
android.minapi              = 21
android.targetapi           = 33
android.archs               = arm64-v8a, armeabi-v7a
android.allow_backup        = True
android.accept_sdk_license  = True
android.release_artifact    = apk

# ── python-for-android ───────────────────────────────────────────────
p4a.branch = master

[buildozer]
log_level    = 2
warn_on_root = 1
