[app]

title           = Neon Cube Rush
package.name    = neoncuberush
package.domain  = org.jem
version         = 1.0

source.dir              = .
source.include_exts     = py,png,jpg,jpeg,json,wav,ogg,mp3,ttf
source.exclude_dirs     = tests,bin,.buildozer,__pycache__,.git,.github

# FIX : version pygame explicite et testée avec p4a
requirements = python3==3.11.0,pygame==2.1.4

orientation = portrait
fullscreen  = 1

android.permissions         = VIBRATE
android.minapi              = 21
android.targetapi           = 33
android.archs               = arm64-v8a, armeabi-v7a
android.allow_backup        = True
android.accept_sdk_license  = True
android.release_artifact    = apk

p4a.branch = master

[buildozer]
log_level    = 2
warn_on_root = 1
