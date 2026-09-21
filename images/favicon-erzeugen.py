# Erzeugt die PNG-Fassungen des Favicons aus denselben Koordinaten wie
# images/favicon.svg. Die Strichzuege werden Segment fuer Segment als
# Rechteck gefuellt und an den Ecken mit einem Gehrungskeil geschlossen --
# ein einzelnes, selbstschneidendes Polygon fuellt PIL falsch.
import math
from PIL import Image, ImageDraw

BLAU=(0,158,227,255); WEISS=(255,255,255,255)
BREITE=6; GRENZE=2.0          # entspricht stroke-width / stroke-miterlimit
N=[(14,46),(14,18),(26,46),(26,18)]
M=[(34,46),(34,18),(42,33),(50,18),(50,46)]

def einheit(a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]; l=math.hypot(dx,dy); return dx/l,dy/l

def schnitt(p,d,q,e):
    det=d[0]*e[1]-d[1]*e[0]
    if abs(det)<1e-9: return None
    t=((q[0]-p[0])*e[1]-(q[1]-p[1])*e[0])/det
    return (p[0]+d[0]*t, p[1]+d[1]*t)

def flaechen(pfad,breite):
    h=breite/2
    d=[einheit(pfad[i],pfad[i+1]) for i in range(len(pfad)-1)]
    n=[(-dy,dx) for dx,dy in d]
    teile=[]
    for i,(a,b) in enumerate(zip(pfad,pfad[1:])):
        nx,ny=n[i]
        teile.append([(a[0]+nx*h,a[1]+ny*h),(b[0]+nx*h,b[1]+ny*h),
                      (b[0]-nx*h,b[1]-ny*h),(a[0]-nx*h,a[1]-ny*h)])
    for i in range(1,len(pfad)-1):
        v=pfad[i]
        for s in (h,-h):
            ende =(v[0]+n[i-1][0]*s, v[1]+n[i-1][1]*s)
            start=(v[0]+n[i][0]*s,   v[1]+n[i][1]*s)
            m=schnitt((pfad[i-1][0]+n[i-1][0]*s, pfad[i-1][1]+n[i-1][1]*s), d[i-1], start, d[i])
            keil=[v,ende]
            if m and math.hypot(m[0]-v[0],m[1]-v[1]) <= GRENZE*h:
                keil.append(m)
            keil.append(start)
            teile.append(keil)
    return teile

def zeichne(groesse):
    ss=max(2,min(16,1024//groesse)); s=groesse*ss; f=s/64
    bild=Image.new("RGBA",(s,s),(0,0,0,0)); d=ImageDraw.Draw(bild)
    d.ellipse([0,0,s-1,s-1],fill=BLAU)
    for pfad in (N,M):
        for teil in flaechen(pfad,BREITE):
            d.polygon([(x*f,y*f) for x,y in teil],fill=WEISS)
    return bild.resize((groesse,groesse),Image.LANCZOS)

for name,px in [("images/apple-touch-icon.png",180),("images/favicon-32.png",32),("images/icon-512.png",512)]:
    zeichne(px).save(name); print("ok",name,px)
