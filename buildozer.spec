[app]

title = Neon Cube Rush

package.name = neoncuberush

package.domain = org.neoncuberush

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,wav,ogg

version = 0.1

requirements = python3,pygame

p4a.bootstrap = sdl2

orientation = portrait

fullscreen = 1

android.permissions = VIBRATE

android.api = 33

android.minapi = 21

android.ndk = 25b

android.ndk_api = 21

android.private_storage = True

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.logcat_filters = *:S python:D


[buildozer]

log_level = 2

warn_on_root = 1
