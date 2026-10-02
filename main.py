#!/usr/bin/env python3

"""
NEON CUBE RUSH
==============

Android / Desktop Edition

Android:
    - Touch / swipe
    - Vibration
    - Sauvegarde privée
    - Bouton retour Android
    - Pause lors du passage en arrière-plan

Desktop:
    - Souris
    - Clavier
"""

import pygame
import sys
import random
import math
import time
import json
import os


# ============================================================
# ANDROID
# ============================================================

ANDROID = False
_vibrate = None

try:
    import android
    from android.vibrator import vibrate as _android_vibrate

    ANDROID = True
    _vibrate = _android_vibrate

except ImportError:
    pass


def vibrate(ms=30):
    """
    Vibration Android.
    Ne fait rien sur Desktop.
    """
    if not ANDROID or _vibrate is None:
        return

    try:
        _vibrate(ms / 1000.0)
    except Exception:
        pass


# ============================================================
# SAVE PATH
# ============================================================

def get_save_path():
    """
    Utilise le stockage privé de l'application Android.
    Sur Desktop, utilise le dossier du programme.
    """

    if ANDROID:
        try:
            from android import mActivity

            context = mActivity.getApplicationContext()

            files_dir = (
                context
                .getFilesDir()
                .getAbsolutePath()
            )

            return os.path.join(
                files_dir,
                "ncr_save.json"
            )

        except Exception:
            pass

    return os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "ncr_save.json"
    )


SAVE_PATH = get_save_path()


# ============================================================
# PYGAME INITIALIZATION
# ============================================================

pygame.init()

pygame.display.set_caption(
    "NEON CUBE RUSH"
)

W = 420
H = 760

screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

REAL_W, REAL_H = screen.get_size()

if REAL_W <= 0 or REAL_H <= 0:
    REAL_W = 1080
    REAL_H = 1920


# ============================================================
# DESIGN SURFACE
# ============================================================

design = pygame.Surface(
    (W, H)
)


# ============================================================
# SCREEN SCALING
# ============================================================

SCALE = min(
    REAL_W / W,
    REAL_H / H
)

SCALED_W = int(W * SCALE)
SCALED_H = int(H * SCALE)

OFF_X = (
    REAL_W - SCALED_W
) // 2

OFF_Y = (
    REAL_H - SCALED_H
) // 2


def to_design(sx, sy):
    """
    Convertit une coordonnée écran
    en coordonnée de la surface de design.
    """

    if SCALE <= 0:
        return 0, 0

    x = (sx - OFF_X) / SCALE
    y = (sy - OFF_Y) / SCALE

    x = max(
        0,
        min(W - 1, x)
    )

    y = max(
        0,
        min(H - 1, y)
    )

    return int(x), int(y)


def finger_to_design(fx, fy):
    """
    Pygame FINGER events utilisent des
    coordonnées normalisées entre 0 et 1.
    """

    return to_design(
        fx * REAL_W,
        fy * REAL_H
    )


# ============================================================
# CLOCK
# ============================================================

clock = pygame.time.Clock()

FPS = 60


# ============================================================
# EVENTS
# ============================================================

allowed_events = [
    pygame.QUIT,
    pygame.KEYDOWN,
    pygame.MOUSEBUTTONDOWN,
    pygame.MOUSEBUTTONUP,
    pygame.FINGERDOWN,
    pygame.FINGERUP,
    pygame.FINGERMOTION,
]

if ANDROID:

    bg_event = getattr(
        pygame,
        "APP_WILLENTERBACKGROUND",
        None
    )

    fg_event = getattr(
        pygame,
        "APP_DIDENTERFOREGROUND",
        None
    )

    if bg_event is not None:
        allowed_events.append(bg_event)

    if fg_event is not None:
        allowed_events.append(fg_event)


pygame.event.set_allowed(
    allowed_events
)


# ============================================================
# ANDROID BACK BUTTON
# ============================================================

BACK_KEYS = {
    pygame.K_ESCAPE
}

try:
    BACK_KEYS.add(
        pygame.K_AC_BACK
    )
except AttributeError:
    pass


EV_BG = getattr(
    pygame,
    "APP_WILLENTERBACKGROUND",
    None
)

EV_FG = getattr(
    pygame,
    "APP_DIDENTERFOREGROUND",
    None
)


# ============================================================
# FONTS
# ============================================================

try:

    F4 = pygame.font.SysFont(
        "Courier New",
        42,
        bold=True
    )

    F2 = pygame.font.SysFont(
        "Courier New",
        22,
        bold=True
    )

    F1 = pygame.font.SysFont(
        "Courier New",
        15
    )

    FX = pygame.font.SysFont(
        "Courier New",
        11
    )

except Exception:

    F4 = pygame.font.Font(
        None,
        48
    )

    F2 = pygame.font.Font(
        None,
        28
    )

    F1 = pygame.font.Font(
        None,
        20
    )

    FX = pygame.font.Font(
        None,
        16
  )
