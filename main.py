#!/usr/bin/env python3
"""
NEON CUBE RUSH — Android / Mobile Edition
==========================================
Requirements : pip install pygame
Android      : buildozer android debug

Controls (Android)
------------------
  DOIGT   : Glisser sur le cube → move
  RETOUR  : Bouton Android = retour menu / quitter
"""

import pygame, sys, random, math, time, json, os

# ── ANDROID DETECTION & VIBRATION ────────────────────────────────────
try:
    import android                                        # python-for-android
    from android.vibrator import vibrate as _vib
    def vibrate(ms=30):
        try: _vib(ms / 1000.0)
        except Exception: pass
    ANDROID = True
except ImportError:
    def vibrate(ms=30): pass
    ANDROID = False

# ── SAVE PATH ────────────────────────────────────────────────────────
try:
    from android import mActivity
    _files_dir = mActivity.getApplicationContext().getFilesDir().getAbsolutePath()
    SAVE_PATH = os.path.join(_files_dir, 'ncr_save.json')
except Exception:
    SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ncr_save.json')

# ── INIT ─────────────────────────────────────────────────────────────
pygame.init()
pygame.display.set_caption("NEON CUBE RUSH")

W, H = 420, 760          # Résolution de design (fixe, indépendante de l'écran)

# Écran physique plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
REAL_W, REAL_H = screen.get_size()
if REAL_W <= 0 or REAL_H <= 0:
    REAL_W, REAL_H = 1080, 1920   # Fallback raisonnable

# Surface de design (tout le rendu se fait ici)
design = pygame.Surface((W, H))

# Scaling : agrandir le design pour remplir l'écran (avec bandes noires si ratio différent)
SCALE    = min(REAL_W / W, REAL_H / H)
SCALED_W = int(W * SCALE)
SCALED_H = int(H * SCALE)
OFF_X    = (REAL_W - SCALED_W) // 2
OFF_Y    = (REAL_H - SCALED_H) // 2

def to_design(sx, sy):
    """Coordonnées écran physique → coordonnées design."""
    return (
        int(max(0, min(W - 1, (sx - OFF_X) / SCALE))),
        int(max(0, min(H - 1, (sy - OFF_Y) / SCALE))),
    )

def finger_to_design(fx, fy):
    """Coordonnées FINGER normalisées [0-1] → coordonnées design."""
    return to_design(fx * REAL_W, fy * REAL_H)

clock = pygame.time.Clock()
FPS = 60

# Événements utiles seulement (perf)
pygame.event.set_allowed([
    pygame.QUIT, pygame.KEYDOWN,
    pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
    pygame.FINGERDOWN, pygame.FINGERUP, pygame.FINGERMOTION,
    *([getattr(pygame, 'APP_WILLENTERBACKGROUND', -1),
       getattr(pygame, 'APP_DIDENTERFOREGROUND',  -1)] if ANDROID else []),
])

# Touche retour Android
BACK_KEY = {pygame.K_ESCAPE}
try: BACK_KEY.add(pygame.K_AC_BACK)
except AttributeError: pass

# Constantes lifecycle
_EV_BG = getattr(pygame, 'APP_WILLENTERBACKGROUND', None)
_EV_FG = getattr(pygame, 'APP_DIDENTERFOREGROUND',  None)

# Fonts
try:
    F4 = pygame.font.SysFont("Courier New", 42, bold=True)
    F2 = pygame.font.SysFont("Courier New", 22, bold=True)
    F1 = pygame.font.SysFont("Courier New", 15)
    FX = pygame.font.SysFont("Courier New", 11)
except Exception:
    F4 = pygame.font.Font(None, 48)
    F2 = pygame.font.Font(None, 28)
    F1 = pygame.font.Font(None, 20)
    FX = pygame.font.Font(None, 16)

# ── DONNÉES ──────────────────────────────────────────────────────────
BIOMES = [
    {"id":1,"name":"NEON CITY",        "bg":(4,0,12),   "acc":(191,0,255),  "time":0,  "sc":12},
    {"id":2,"name":"CYBER FOREST",     "bg":(0,10,4),   "acc":(0,255,136),  "time":90, "sc":16},
    {"id":3,"name":"ELECTRIC DESERT",  "bg":(14,6,0),   "acc":(255,102,0),  "time":75, "sc":20},
    {"id":4,"name":"VOLCANO WORLD",    "bg":(14,0,0),   "acc":(255,20,20),  "time":60, "sc":24},
    {"id":5,"name":"DEEP SPACE",       "bg":(0,0,14),   "acc":(0,204,255),  "time":45, "sc":30},
]
SKINS = [
    {"id":"neon",   "name":"NEON CLASSIC",   "price":0,    "owned":True,
     "cv":{"W":(255,255,255),"Y":(255,230,0),"R":(255,32,32),"O":(255,140,0),"B":(30,144,255),"G":(0,230,118)}},
    {"id":"galaxy", "name":"GALAXY",          "price":500,  "owned":False,
     "cv":{"W":(220,200,255),"Y":(204,136,255),"R":(255,68,204),"O":(170,68,255),"B":(68,136,255),"G":(68,255,204)}},
    {"id":"fire",   "name":"INFERNO",         "price":800,  "owned":False,
     "cv":{"W":(255,238,170),"Y":(255,204,0),"R":(255,0,0),"O":(255,68,0),"B":(255,136,0),"G":(255,221,0)}},
    {"id":"ice",    "name":"ARCTIC",          "price":600,  "owned":False,
     "cv":{"W":(232,248,255),"Y":(170,222,255),"R":(136,187,255),"O":(170,204,255),"B":(0,170,255),"G":(0,255,238)}},
    {"id":"void",   "name":"VOID",            "price":1200, "owned":False,
     "cv":{"W":(42,42,42),"Y":(26,0,51),"R":(51,0,17),"O":(26,0,17),"B":(0,0,64),"G":(0,26,0)}},
    {"id":"gold",   "name":"GOLDEN",          "price":3000, "owned":False,
     "cv":{"W":(255,245,204),"Y":(255,215,0),"R":(204,153,0),"O":(204,119,0),"B":(153,119,0),"G":(255,238,136)}},
    {"id":"cherry", "name":"CHERRY BLOSSOM",  "price":1000, "owned":False,
     "cv":{"W":(255,228,232),"Y":(255,153,170),"R":(204,34,85),"O":(255,68,153),"B":(204,68,170),"G":(255,136,187)}},
    {"id":"cyber",  "name":"CYBERPUNK 2099",  "price":1800, "owned":False,
     "cv":{"W":(240,240,0),"Y":(170,170,0),"R":(255,0,68),"O":(51,51,0),"B":(26,26,0),"G":(240,240,0)}},
]
LB = [
    ("CubeGod [JP]",142800),("NeonMaster [FR]",128400),("VoidQueen [KR]",114200),
    ("IceSpeed [US]",98700), ("FireLord [BR]",87200),  ("GalaxyX [DE]",76800),
    ("TurboRub [UK]",64300), ("SpeedCube [CN]",52100), ("NightFox [IT]",39800),
]

# ── LOGIQUE CUBE ──────────────────────────────────────────────────────
def new_cube():
    return [list(c*9) for c in "WYROBG"]

cw  = lambda f: [f[6],f[3],f[0],f[7],f[4],f[1],f[8],f[5],f[2]]
ccw = lambda f: [f[2],f[5],f[8],f[1],f[4],f[7],f[0],f[3],f[6]]

def mv(cube, m):
    c = [list(f) for f in cube]; t = None
    if   m=="U":  c[0]=cw(c[0]);t=[c[2][0],c[2][1],c[2][2]];c[2][0]=c[5][0];c[2][1]=c[5][1];c[2][2]=c[5][2];c[5][0]=c[3][8];c[5][1]=c[3][7];c[5][2]=c[3][6];c[3][8]=c[4][2];c[3][7]=c[4][1];c[3][6]=c[4][0];c[4][0]=t[0];c[4][1]=t[1];c[4][2]=t[2]
    elif m=="U'": c[0]=ccw(c[0]);t=[c[2][0],c[2][1],c[2][2]];c[2][0]=c[4][0];c[2][1]=c[4][1];c[2][2]=c[4][2];c[4][0]=c[3][8];c[4][1]=c[3][7];c[4][2]=c[3][6];c[3][8]=c[5][0];c[3][7]=c[5][1];c[3][6]=c[5][2];c[5][0]=t[0];c[5][1]=t[1];c[5][2]=t[2]
    elif m=="D":  c[1]=cw(c[1]);t=[c[2][6],c[2][7],c[2][8]];c[2][6]=c[4][6];c[2][7]=c[4][7];c[2][8]=c[4][8];c[4][6]=c[3][2];c[4][7]=c[3][1];c[4][8]=c[3][0];c[3][0]=c[5][8];c[3][1]=c[5][7];c[3][2]=c[5][6];c[5][6]=t[0];c[5][7]=t[1];c[5][8]=t[2]
    elif m=="D'": c[1]=ccw(c[1]);t=[c[2][6],c[2][7],c[2][8]];c[2][6]=c[5][6];c[2][7]=c[5][7];c[2][8]=c[5][8];c[5][6]=c[3][2];c[5][7]=c[3][1];c[5][8]=c[3][0];c[3][0]=c[4][8];c[3][1]=c[4][7];c[3][2]=c[4][6];c[4][6]=t[0];c[4][7]=t[1];c[4][8]=t[2]
    elif m=="R":  c[5]=cw(c[5]);t=[c[0][2],c[0][5],c[0][8]];c[0][2]=c[2][2];c[0][5]=c[2][5];c[0][8]=c[2][8];c[2][2]=c[1][2];c[2][5]=c[1][5];c[2][8]=c[1][8];c[1][2]=c[3][6];c[1][5]=c[3][3];c[1][8]=c[3][0];c[3][0]=t[2];c[3][3]=t[1];c[3][6]=t[0]
    elif m=="R'": c[5]=ccw(c[5]);t=[c[0][2],c[0][5],c[0][8]];c[0][2]=c[3][6];c[0][5]=c[3][3];c[0][8]=c[3][0];c[3][0]=c[1][8];c[3][3]=c[1][5];c[3][6]=c[1][2];c[1][2]=c[2][2];c[1][5]=c[2][5];c[1][8]=c[2][8];c[2][2]=t[0];c[2][5]=t[1];c[2][8]=t[2]
    elif m=="L":  c[4]=cw(c[4]);t=[c[0][0],c[0][3],c[0][6]];c[0][0]=c[3][8];c[0][3]=c[3][5];c[0][6]=c[3][2];c[3][2]=c[1][6];c[3][5]=c[1][3];c[3][8]=c[1][0];c[1][0]=c[2][0];c[1][3]=c[2][3];c[1][6]=c[2][6];c[2][0]=t[0];c[2][3]=t[1];c[2][6]=t[2]
    elif m=="L'": c[4]=ccw(c[4]);t=[c[0][0],c[0][3],c[0][6]];c[0][0]=c[2][0];c[0][3]=c[2][3];c[0][6]=c[2][6];c[2][0]=c[1][0];c[2][3]=c[1][3];c[2][6]=c[1][6];c[1][0]=c[3][8];c[1][3]=c[3][5];c[1][6]=c[3][2];c[3][2]=t[2];c[3][5]=t[1];c[3][8]=t[0]
    elif m=="F":  c[2]=cw(c[2]);t=[c[0][6],c[0][7],c[0][8]];c[0][6]=c[4][8];c[0][7]=c[4][5];c[0][8]=c[4][2];c[4][2]=c[1][0];c[4][5]=c[1][1];c[4][8]=c[1][2];c[1][0]=c[5][6];c[1][1]=c[5][3];c[1][2]=c[5][0];c[5][0]=t[0];c[5][3]=t[1];c[5][6]=t[2]
    elif m=="F'": c[2]=ccw(c[2]);t=[c[0][6],c[0][7],c[0][8]];c[0][6]=c[5][0];c[0][7]=c[5][3];c[0][8]=c[5][6];c[5][0]=c[1][2];c[5][3]=c[1][1];c[5][6]=c[1][0];c[1][0]=c[4][2];c[1][1]=c[4][5];c[1][2]=c[4][8];c[4][2]=t[2];c[4][5]=t[1];c[4][8]=t[0]
    return c

face_done = lambda f: all(x==f[0] for x in f)
cube_done = lambda c: all(face_done(f) for f in c)

def scramble(c, n=15):
    pool = ["U","U'","D","D'","R","R'","L","L'","F","F'"]
    for _ in range(n): c = mv(c, random.choice(pool))
    return c

# ── RENDU ISOMÉTRIQUE ────────────────────────────────────────────────
SC = 28
CX, CY = W // 2, 295

def iso(x, y, z):
    return (int(CX+(x-z)*SC*0.866), int(CY+(x+z)*SC*0.5-y*SC))

def top_poly(row, col):
    x0=-1.5+col; x1=x0+1; z1=1.5-row; z0=z1-1
    return [iso(x0,1.5,z1),iso(x1,1.5,z1),iso(x1,1.5,z0),iso(x0,1.5,z0)]

def front_poly(row, col):
    x0=-1.5+col; x1=x0+1; y1=1.5-row; y0=y1-1
    return [iso(x0,y1,-1.5),iso(x1,y1,-1.5),iso(x1,y0,-1.5),iso(x0,y0,-1.5)]

def right_poly(row, col):
    z0=-1.5+col; z1=z0+1; y1=1.5-row; y0=y1-1
    return [iso(1.5,y1,z0),iso(1.5,y1,z1),iso(1.5,y0,z1),iso(1.5,y0,z0)]

dim = lambda c, f: tuple(max(0, int(x*f)) for x in c)

def draw_cube(surf, cube, colors, solved_faces, acc):
    for r in range(3):
        for c in range(3):
            col = colors.get(cube[0][r*3+c], (128,128,128))
            poly = top_poly(r, c)
            pygame.draw.polygon(surf, col, poly)
            ec = tuple(min(255, int(x*1.4)) for x in acc) if solved_faces[0] else (0,0,0)
            pygame.draw.polygon(surf, ec, poly, 1)
    for r in range(3):
        for c in range(3):
            col = dim(colors.get(cube[2][r*3+c], (128,128,128)), 0.82)
            poly = front_poly(r, c)
            pygame.draw.polygon(surf, col, poly)
            ec = dim(acc, 0.8) if solved_faces[2] else (0,0,0)
            pygame.draw.polygon(surf, ec, poly, 1)
    for r in range(3):
        for c in range(3):
            col = dim(colors.get(cube[5][r*3+c], (128,128,128)), 0.65)
            poly = right_poly(r, c)
            pygame.draw.polygon(surf, col, poly)
            ec = dim(acc, 0.6) if solved_faces[5] else (0,0,0)
            pygame.draw.polygon(surf, ec, poly, 1)

# ── DÉTECTION SWIPE ──────────────────────────────────────────────────
def pt_in_poly(px, py, poly):
    n=len(poly); inside=False; p1x,p1y=poly[0]
    for i in range(1,n+1):
        p2x,p2y=poly[i%n]
        if min(p1y,p2y)<py<=max(p1y,p2y) and px<=max(p1x,p2x):
            if p1y!=p2y:
                xi=(py-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                if p1x==p2x or px<=xi: inside=not inside
        p1x,p1y=p2x,p2y
    return inside

def hit_zone(px, py):
    for r in range(3):
        for c in range(3):
            if pt_in_poly(px,py,top_poly(r,c)):   return "top",  r, c
    for r in range(3):
        for c in range(3):
            if pt_in_poly(px,py,front_poly(r,c)): return "front",r, c
    for r in range(3):
        for c in range(3):
            if pt_in_poly(px,py,right_poly(r,c)): return "right",r, c
    return None, None, None

def swipe_move(face, row, col, dx, dy):
    h = abs(dx) > abs(dy)
    if face=="top":
        if h: return "U" if dx>0 else "U'"
        return ("L" if dy<0 else "L'") if col==0 else ("R" if dy<0 else "R'")
    elif face=="front":
        if h:
            if row==0: return "U" if dx>0 else "U'"
            if row==2: return "D'" if dx>0 else "D"
            return "F" if dx>0 else "F'"
        return ("L" if dy<0 else "L'") if col==0 else ("R" if dy<0 else "R'")
    elif face=="right":
        return ("F" if dx<0 else "F'") if h else ("R" if dy<0 else "R'")
    return None

# ── EFFETS VISUELS ───────────────────────────────────────────────────
MAX_PARTICLES = 100

class Particle:
    __slots__ = ('x','y','col','life','sz','vx','vy')
    def __init__(self, x, y, col):
        self.x,self.y,self.col = float(x),float(y),col
        self.life=1.0; self.sz=random.uniform(2,5)
        a=random.uniform(0,math.pi*2); v=random.uniform(2,9)
        self.vx=math.cos(a)*v; self.vy=math.sin(a)*v-3
    def update(self):
        self.x+=self.vx; self.y+=self.vy
        self.vy+=0.22; self.vx*=0.98; self.life-=0.022
    def draw(self, surf):
        if self.life>0:
            pygame.draw.circle(surf, dim(self.col, 0.5+0.5*self.life),
                               (int(self.x), int(self.y)), max(1,int(self.sz*self.life)))

class FloatTxt:
    __slots__ = ('txt','x','y','col','life','big')
    def __init__(self, txt, x, y, col, big=False):
        self.txt=txt; self.x,self.y=float(x),float(y)
        self.col=col; self.life=1.0; self.big=big
    def update(self): self.y-=1.2; self.life-=0.022
    def draw(self, surf):
        if self.life>0:
            s=(F2 if self.big else F1).render(self.txt,True,self.col)
            s.set_alpha(int(self.life*255))
            surf.blit(s,(int(self.x-s.get_width()//2),int(self.y)))

PTS, FLTS = [], []

def burst(x, y, col, n=35):
    space = MAX_PARTICLES - len(PTS)
    for _ in range(min(n, space)): PTS.append(Particle(x, y, col))

# ── HELPERS UI ───────────────────────────────────────────────────────
def txt(surf, text, x, y, fnt, color, cx=False):
    s = fnt.render(str(text), True, color)
    surf.blit(s, (x - s.get_width()//2 if cx else x, y))
    return s.get_width()

def box(surf, x, y, w, h, fill, r=8, bw=0, bc=None):
    pygame.draw.rect(surf, fill, (x,y,w,h), border_radius=r)
    if bw: pygame.draw.rect(surf, bc or fill, (x,y,w,h), bw, border_radius=r)

def btn(surf, text, x, y, w, h, bg, fg, bc=None, fnt=None):
    fnt = fnt or F1; box(surf,x,y,w,h,bg,6,1,bc or bg)
    s = fnt.render(text, True, fg)
    surf.blit(s, (x+(w-s.get_width())//2, y+(h-s.get_height())//2))

def clicked(rect, pos):
    if not pos: return False
    return rect[0]<=pos[0]<=rect[0]+rect[2] and rect[1]<=pos[1]<=rect[1]+rect[3]

def make_stars():
    return [{"x":random.randint(0,W),"y":random.randint(0,H),
             "r":random.uniform(0.4,1.8),"sp":random.uniform(0.05,0.3),
             "b":random.uniform(0.2,0.9)} for _ in range(90)]

# ── ÉTAT DU JEU ──────────────────────────────────────────────────────
G = {
    "screen":"menu","bi":0,"cube":None,"score":0,"tot":0,
    "combo":1,"ct":0,"sf":[False]*6,"tl":0.0,"ta":False,
    "coins":350,"skin":"neon","skins":[dict(s) for s in SKINS],
    "drag":None,"lmv":0,"fd":0,"stars":make_stars(),
}
bm  = lambda: BIOMES[G["bi"]]
acc = lambda: bm()["acc"]
cv  = lambda: next((s["cv"] for s in G["skins"] if s["id"]==G["skin"]), SKINS[0]["cv"])

# ── SAVE / LOAD ──────────────────────────────────────────────────────
def save_game():
    data = {
        "coins": G["coins"],
        "bi":    G["bi"],
        "tot":   G.get("tot", 0),
        "skin":  G["skin"],
        "owned": [s["id"] for s in G["skins"] if s["owned"]],
    }
    try:
        with open(SAVE_PATH, "w") as f: json.dump(data, f)
    except Exception: pass

def load_save():
    try:
        with open(SAVE_PATH, "r") as f: data = json.load(f)
        G["coins"] = max(0,   int(data.get("coins", 350)))
        G["bi"]    = max(0,   min(int(data.get("bi", 0)), len(BIOMES)-1))
        G["tot"]   = max(0,   int(data.get("tot", 0)))
        G["skin"]  = data.get("skin", "neon")
        owned = set(data.get("owned", []))
        for s in G["skins"]:
            if s["id"] in owned: s["owned"] = True
    except Exception: pass

load_save()

# ── FOND ANIMÉ ───────────────────────────────────────────────────────
def draw_bg(surf):
    b = bm(); surf.fill(b["bg"]); a = b["acc"]
    for s in G["stars"]:
        s["y"] = (s["y"] + s["sp"]) % H
        pygame.draw.circle(surf, dim(a,s["b"]),
                           (int(s["x"]), int(s["y"])), max(1,int(s["r"])))

# ── MENU ─────────────────────────────────────────────────────────────
def draw_menu(surf, cp):
    a = acc(); b = bm()
    txt(surf,"NEON",W//2,78,F4,a,cx=True)
    txt(surf,"CUBE RUSH",W//2,133,F2,(210,210,210),cx=True)
    txt(surf,f"{b['name']}  LVL {b['id']}/5",W//2,172,FX,a,cx=True)
    txt(surf,f"COINS: {G['coins']:,}",W//2,196,F1,(255,215,0),cx=True)
    buttons=[("JOUER",    (W//2-120,250,240,55),a,(0,0,0)),
             ("BOUTIQUE", (W//2-120,315,240,50),(18,18,18),a),
             ("CLASSEMENT",(W//2-120,375,240,50),(18,18,18),a)]
    actions=["start","shop","lb"]
    for (t,r,bg,fg),act in zip(buttons,actions):
        btn(surf,t,*r,bg,fg,a,F1)
        if clicked(r,cp): return act
    txt(surf,"GLISSER SUR LE CUBE = MOVE",W//2,450,FX,(45,45,45),cx=True)
    return None

# ── ACTIONS JEU ──────────────────────────────────────────────────────
def start_game():
    b = bm(); c = scramble(new_cube(), b["sc"])
    G.update({"cube":c,"score":0,"combo":1,"ct":0,"sf":[False]*6,"fd":0,
              "tl":float(b["time"]) if b["time"]>0 else 9999.0,
              "ta":b["time"]>0,"lmv":pygame.time.get_ticks(),
              "screen":"game","drag":None})
    PTS.clear(); FLTS.clear()

def do_move(m):
    now = pygame.time.get_ticks()
    G["combo"] = min(G["combo"]+1, 10) if now-G["lmv"]<900 else 1
    G["lmv"] = now; G["ct"] = now
    old = [face_done(f) for f in G["cube"]]
    G["cube"] = mv(G["cube"], m)
    ns = [face_done(f) for f in G["cube"]]
    pts = G["combo"]*12; G["score"] += pts
    FLTS.append(FloatTxt(f"+{pts}",W//2+random.randint(-55,55),
                         CY+random.randint(-25,35), acc()))
    vibrate(18)
    for i in range(6):
        if ns[i] and not old[i]:
            G["fd"] += 1; bonus = 700*G["combo"]*(G["bi"]+1); G["score"] += bonus
            FLTS.append(FloatTxt(f"FACE! +{bonus:,}",W//2,CY-65,acc(),big=True))
            burst(CX, CY, acc(), 70); burst(CX, CY, (255,255,255), 18)
            vibrate(50)
    G["sf"] = ns
    if cube_done(G["cube"]): end_game(False)

def end_game(timeout):
    bonus = 0 if timeout else 2500*(G["bi"]+1)
    total = G["score"]+bonus; coins = total//7
    G["tot"] = G.get("tot",0)+total; G["coins"] += coins
    G.update({"screen":"victory","v_to":timeout,
              "v_tot":total,"v_bon":bonus,"v_co":coins})
    burst(CX, CY, acc(), 100)
    vibrate(80 if not timeout else 30)
    save_game()    # Auto-save à chaque fin de partie

# ── ÉCRAN JEU ────────────────────────────────────────────────────────
def draw_game(surf, cp, events):
    a = acc(); b = bm()
    box(surf,5,5,W-10,50,(8,8,8),6,1,a)
    txt(surf,f"SCORE: {G['score']:,}",12,17,F1,a)
    ccol = (255,215,0) if G["combo"]>=5 else a
    txt(surf,f"x{G['combo']}",W//2,14,F2,ccol,cx=True)
    tc = (255,50,50) if G["ta"] and G["tl"]<15 else a
    txt(surf,(f"{int(G['tl'])}s" if G["ta"] else "INF"),W-60,17,F1,tc)
    labels=["TOP","BTM","FRT","BCK","LFT","RGT"]
    for i,l in enumerate(labels):
        x=7+i*68; done=G["sf"][i]
        box(surf,x,62,63,22,a if done else (12,12,12),4,1,a if done else (35,35,35))
        txt(surf,l,x+32,65,FX,(0,0,0) if done else (70,70,70),cx=True)
    draw_cube(surf,G["cube"],cv(),G["sf"],a)
    txt(surf,"GLISSER VITE SUR LE CUBE = MOVE",W//2,478,FX,(45,45,45),cx=True)
    txt(surf,"HAUT:U  BAS:D  DROITE:R  GAUCHE:L  CENTRE:F",W//2,492,FX,(38,38,38),cx=True)
    back=(10,H-50,100,38)
    btn(surf,"<- MENU",*back,(20,20,20),(110,110,110),(55,55,55),FX)
    if clicked(back,cp): G["screen"]="menu"
    for p in PTS[:]:
        p.update(); p.draw(surf)
        if p.life<=0: PTS.remove(p)
    for f in FLTS[:]:
        f.update(); f.draw(surf)
        if f.life<=0: FLTS.remove(f)
    # Clavier (desktop / debug)
    for e in events:
        if e.type==pygame.KEYDOWN:
            km={pygame.K_u:"U",pygame.K_d:"D",pygame.K_r:"R",
                pygame.K_l:"L",pygame.K_f:"F"}
            if e.key in km:
                do_move(km[e.key]+("'" if e.mod&pygame.KMOD_SHIFT else ""))

# ── VICTOIRE ─────────────────────────────────────────────────────────
def draw_victory(surf, cp):
    a=acc(); is_last=G["bi"]>=len(BIOMES)-1; to=G.get("v_to",False)
    title="TEMPS ECOULE!" if to else ("MAITRE DU CUBE!" if is_last else "CUBE RESOLU!")
    txt(surf,title,W//2,90,F2,a,cx=True)
    rows=[("Score de jeu:",f"{G['score']:,}"),("Faces:",f"{G['fd']}/6"),
          ("Bonus biome:",f"+{G.get('v_bon',0):,}"),("TOTAL:",f"{G.get('v_tot',0):,}")]
    y=145
    for lab,val in rows:
        box(surf,W//2-140,y,280,32,(14,14,14),6,1,(35,35,35))
        txt(surf,lab,W//2-130,y+8,FX,(140,140,140))
        sw=FX.size(val)[0]; txt(surf,val,W//2+130-sw,y+8,FX,a)
        y+=38
    txt(surf,f"+ {G.get('v_co',0):,} COINS",W//2,y+8,F1,(255,215,0),cx=True)
    nr=(W//2-120,y+46,240,50)
    nt="REJOUER" if is_last else f"BIOME {G['bi']+2} ->"
    btn(surf,nt,*nr,a,(0,0,0),None,F1)
    mr=(W//2-120,y+108,240,44)
    btn(surf,"<- MENU",*mr,(18,18,18),(130,130,130),(55,55,55),F1)
    if clicked(nr,cp):
        G["bi"] = 0 if is_last else min(G["bi"]+1,len(BIOMES)-1)
        save_game()
        start_game()
    if clicked(mr,cp): G["screen"]="menu"
    for p in PTS[:]:
        p.update(); p.draw(surf)
        if p.life<=0: PTS.remove(p)

# ── BOUTIQUE ─────────────────────────────────────────────────────────
def draw_shop(surf, cp):
    a=acc()
    txt(surf,"BOUTIQUE",W//2,16,F2,a,cx=True)
    txt(surf,f"COINS: {G['coins']:,}",W//2,50,F1,(255,215,0),cx=True)
    y=84
    for sk in G["skins"]:
        if y>H-60: break
        eq=G["skin"]==sk["id"]; ow=sk["owned"]
        box(surf,7,y,W-14,66,(15,4,24) if eq else (11,11,11),8,1,a if eq else (38,38,38))
        for i,c in enumerate(list(sk["cv"].values())[:6]):
            pygame.draw.rect(surf,c,(17+i*13,y+6,11,11),border_radius=2)
        txt(surf,sk["name"],17,y+22,FX,a if eq else (175,175,175))
        ptxt="POSSEDE" if ow else f"COINS: {sk['price']:,}"
        txt(surf,ptxt,17,y+40,FX,(80,200,80) if ow else (255,215,0))
        br=(W-118,y+13,105,40)
        if ow:
            btn(surf,"EQUIPE" if eq else "EQUIPER",*br,
                a if eq else (28,28,28),(0,0,0) if eq else a,a,FX)
        else:
            can=G["coins"]>=sk["price"]
            btn(surf,"ACHETER",*br,(28,28,28) if can else (12,12,12),
                a if can else (45,45,45),(55,55,55) if can else (25,25,25),FX)
        if clicked(br,cp):
            if ow: G["skin"]=sk["id"]
            elif G["coins"]>=sk["price"]:
                G["coins"]-=sk["price"]; sk["owned"]=True; G["skin"]=sk["id"]
                save_game()
        y+=74
    back=(10,H-50,100,38)
    btn(surf,"<- RETOUR",*back,(18,18,18),(110,110,110),(50,50,50),FX)
    if clicked(back,cp): G["screen"]="menu"

# ── CLASSEMENT ───────────────────────────────────────────────────────
def draw_lb(surf, cp):
    a=acc()
    txt(surf,"CLASSEMENT MONDIAL",W//2,16,F2,a,cx=True)
    entries=list(LB)+[("VOUS",G.get("tot",0))]
    entries.sort(key=lambda x:x[1],reverse=True)
    y=62
    for i,(name,score) in enumerate(entries):
        if y>H-60: break
        me=name=="VOUS"
        box(surf,7,y,W-14,38,(14,4,22) if me else (10,10,10),6,1,a if me else (30,30,30))
        rc=[(255,215,0),(192,192,192),(205,127,50)][i] if i<3 else (70,70,70)
        txt(surf,f"#{i+1}",16,y+10,FX,rc)
        txt(surf,name,54,y+10,FX,a if me else (170,170,170))
        sc_str=f"{score:,}"; sw=FX.size(sc_str)[0]
        txt(surf,sc_str,W-14-sw,y+10,FX,(255,215,0))
        y+=44
    back=(10,H-50,100,38)
    btn(surf,"<- RETOUR",*back,(18,18,18),(110,110,110),(50,50,50),FX)
    if clicked(back,cp): G["screen"]="menu"

# ── BOUCLE PRINCIPALE ────────────────────────────────────────────────
last_t     = time.time()
paused     = False
use_finger = False          # True dès qu'un FINGERDOWN est reçu

while True:
    cp = None; evts = []

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            save_game(); pygame.quit(); sys.exit()
        evts.append(e)

        # ── Lifecycle Android ──────────────────────────────────────
        if _EV_BG and e.type == _EV_BG:
            paused = True; save_game()
        if _EV_FG and e.type == _EV_FG:
            paused = False; last_t = time.time()

        # ── Bouton RETOUR Android / Échap Desktop ──────────────────
        if e.type == pygame.KEYDOWN and e.key in BACK_KEY:
            if G["screen"] == "menu":
                save_game(); pygame.quit(); sys.exit()
            else:
                G["screen"] = "menu"

        # ── Touch FINGER (Android — prioritaire) ───────────────────
        if e.type == pygame.FINGERDOWN:
            use_finger = True
            pos = finger_to_design(e.x, e.y)
            if G["screen"] == "game":
                face, r, c = hit_zone(*pos)
                G["drag"] = {"x":pos[0],"y":pos[1],"t":pygame.time.get_ticks(),
                             "face":face,"row":r,"col":c}

        elif e.type == pygame.FINGERUP:
            pos = finger_to_design(e.x, e.y)
            cp  = pos
            if G["screen"] == "game" and G["drag"]:
                d=G["drag"]; dx=pos[0]-d["x"]; dy=pos[1]-d["y"]
                dt=pygame.time.get_ticks()-d["t"]
                dist=math.sqrt(dx*dx+dy*dy)
                if dist>22 and dt<450 and d["face"]:
                    m=swipe_move(d["face"],d["row"],d["col"],dx,dy)
                    if m: do_move(m)
                G["drag"]=None

        # ── Touch SOURIS (Desktop / fallback si pas de FINGER) ─────
        elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1 and not use_finger:
            pos = to_design(*e.pos)
            if G["screen"]=="game":
                face,r,c=hit_zone(*pos)
                G["drag"]={"x":pos[0],"y":pos[1],"t":pygame.time.get_ticks(),
                            "face":face,"row":r,"col":c}

        elif e.type==pygame.MOUSEBUTTONUP and e.button==1 and not use_finger:
            pos = to_design(*e.pos)
            cp  = pos
            if G["screen"]=="game" and G["drag"]:
                d=G["drag"]; dx=pos[0]-d["x"]; dy=pos[1]-d["y"]
                dt=pygame.time.get_ticks()-d["t"]
                dist=math.sqrt(dx*dx+dy*dy)
                if dist>22 and dt<450 and d["face"]:
                    m=swipe_move(d["face"],d["row"],d["col"],dx,dy)
                    if m: do_move(m)
                G["drag"]=None

    # ── Pause arrière-plan ────────────────────────────────────────
    if paused:
        pygame.time.wait(50); continue

    # ── Timer ────────────────────────────────────────────────────
    now=time.time(); dt_s=now-last_t; last_t=now
    if G["screen"]=="game" and G["ta"]:
        G["tl"]=max(0.0,G["tl"]-dt_s)
        if G["tl"]<=0: end_game(True)

    # ── Combo decay ───────────────────────────────────────────────
    if G.get("ct") and pygame.time.get_ticks()-G["ct"]>2400:
        G["combo"]=1

    # ── Rendu sur la surface de design ───────────────────────────
    s=G["screen"]
    draw_bg(design)
    if s=="menu":
        a=draw_menu(design,cp)
        if a=="start": start_game()
        elif a in ("shop","lb"): G["screen"]=a
    elif s=="game":    draw_game(design,cp,evts)
    elif s=="victory": draw_victory(design,cp)
    elif s=="shop":    draw_shop(design,cp)
    elif s=="lb":      draw_lb(design,cp)

    # ── Scale design → écran physique ────────────────────────────
    scaled = pygame.transform.scale(design, (SCALED_W, SCALED_H))
    screen.fill((0,0,0))                # Bandes noires (letterbox)
    screen.blit(scaled, (OFF_X, OFF_Y))
    pygame.display.flip()
    clock.tick(FPS)
