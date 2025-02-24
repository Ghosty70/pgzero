import pgzrun
import random
from turtle import Screen
import keyboard
from pgzero.actor import Actor
from pgzero.screen import Screen

from pgzero.builtins import animate

WIDTH = 600 # Pencere Genişliği
HEIGHT = 300 # Pencere Yüksekliği

TITLE = "Uzaylı Koşusu" # Oyunun Adı
FPS = 30 # Saniyedeki Kare Sayı

# Nesneler
uzayli = Actor('uzayli', (50, 240))
arkaplan = Actor("arkaplan")
kutu = Actor('kutu', (550, 265))
yeni_resim = 'uzayli' # Anlık görüntüyü takip eder
ari = Actor('ari', (850, 175))
ob = Actor("OB")
gemi = Actor("gemi", (300, 400))
uzay = Actor("uzay")
dusmanlar = []
gezegenler = [Actor("gezegen1", (random.randint(0, 600), -100)), Actor("gezegen2", (random.randint(0, 600), -100)), Actor("gezegen3", (random.randint(0, 600), -100))]
meteorlar = []
fuzeler = []
mod = 'menu'
gemi1 = Actor("gemi1", (100, 200))
gemi2 = Actor("gemi2", (300, 200))
gemi3 = Actor("gemi3", (500, 200))
# Değişkenler
oyun_sonu = 0
puan = 0
dusman = random.randint(1,2)
hiz = 5

def doldurma():
    # Düşmanlar listesini oluşturmak
    for i in range(5):
        x = random.randint(0, 600)
        y = random.randint(-300, -50)
        dusman = Actor("düşman", (x, y))
        dusman.speed = random.randint(2, 8)
        dusmanlar.append(dusman)
        
    # Meteorlar listesini oluşturmak
    for i in range(5):
        x = random.randint(0, 600)
        y = random.randint(-300, -50)
        meteor = Actor("meteor", (x, y))
        meteor.speed = random.randint(2, 10)
        meteorlar.append(meteor)
doldurma()

# Kontroller
def on_mouse_move(pos):
    gemi.pos = pos

# Yeni Düşmanların Eklenmesi
def yeni_dusman():
    x = random.randint(0, 320)
    y = -50
    dusman = Actor("düşman", (x, y))
    dusman.speed = random.randint(2, 8)
    dusmanlar.append(dusman)

# Düşmanların Hareketleri
def dusman_gemisi():
    for i in range(len(dusmanlar)):
        if dusmanlar[i].y < 650:
            dusmanlar[i].y = dusmanlar[i].y + dusmanlar[i].speed
        else:
            dusmanlar.pop(i)
            yeni_dusman()

# Gezegenlerin Hareketleri
def gezegen():
    if gezegenler[0].y < 550:
            gezegenler[0].y = gezegenler[0].y + 1
    else:
        gezegenler[0].y = -100
        gezegenler[0].x = random.randint(0, 600)
        birinci = gezegenler.pop(0)
        gezegenler.append(birinci)

# Meteorların Hareketleri
def meteorlar_hareket():
    for i in range(len(meteorlar)):
        if meteorlar[i].y < 450:
            meteorlar[i].y = meteorlar[i].y + meteorlar[i].speed
        else:
            meteorlar[i].x = random.randint(0, 600)
            meteorlar[i].y = -20
            meteorlar[i].speed = random.randint(2, 10)

# Çarpışmalar
def carpismalar():
    global mod
    global puan
    for i in range(len(dusmanlar)):
        if gemi.colliderect(dusmanlar[i]):
            mod = 'son'
        # Füzelerin Çarpışması
        for j in range(len(fuzeler)):
            if fuzeler[j].colliderect(dusmanlar[i]):
                puan = puan + 1
                dusmanlar.pop(i)
                fuzeler.pop(j)
                yeni_dusman()
                break

def kutular():
    global puan
    global dusman
    global hiz
    # Kutu Hareketleri
    if kutu.x > -20:
        kutu.x = kutu.x - 5
        kutu.angle = kutu.angle + 5
    else:
        kutu.x = WIDTH + 20
        puan = puan + 1
        dusman = random.randint(1,2)
        hiz = hiz + 1
        
def arilar():
    global puan
    global dusman
    global hiz
    global ari
    # Arı Hareketleri
    if ari.x > -20:
        ari.x = ari.x - 5
    else:
        ari.x = WIDTH + 20
        puan = puan + 1
        dusman = random.randint(1,2)
        hiz = hiz + 1
        ari.y = random.randint(120, 180)

def draw():
    arkaplan.draw()
    uzayli.draw()
    if dusman == 1:
        kutu.draw()
    else:
        ari.draw()
    Screen.draw.text(puan, pos=(10, 10), color="white", fontsize = 24)
    if oyun_sonu == 1:
        ob.draw()
        Screen.draw.text("Enter'a Basınız", pos=(170, 250), color= "red", fontsize = 36)
    if mod == 'menu':
        uzay.draw()

        Screen.draw.text("Gemi Seçiniz", center = (300, 100), color = "white", fontsize = 36)
        gemi1.draw()
        gemi2.draw()
        gemi3.draw()
    if mod == 'oyun':
        uzay.draw()
        gezegenler[0].draw()
        for i in range(len(meteorlar)):
            meteorlar[i].draw()
        gemi.draw()
        for i in range(len(dusmanlar)):
            dusmanlar[i].draw()
        for i in range(len(fuzeler)):
            fuzeler[i].draw()
        Screen.draw.text(puan, (10, 10), color = "white")
    elif mod == 'son':
        uzay.draw()
        Screen.draw.text("OYUN BİTTİ!", center = (300, 200), color = "white", fontsize = 36)
        Screen.draw.text(puan, center = (300, 250), color = "white", fontsize = 64)
       



    
def update(dt):
    # Değişkenler
    global oyun_sonu
    global puan
    global hiz
    global yeni_resim
    global mod,dusmanlar,gezegenler,meteorlar,fuzeler
    # Fonksiyonların Çağrılması
    if dusman == 1:
        kutular()
    
    else:
        arilar()
    if mod == 'oyun':
        dusman_gemisi()
        gezegen()
        meteorlar_hareket()
        carpismalar()
        for i in range(len(fuzeler)):
            if fuzeler[i].y > 0:
                fuzeler.pop(i)
                break
            else:
                fuzeler[i].y = fuzeler[i].y - 10
    elif mod == 'son' and keyboard.space:
        mod="menu"
        puan=0
        dusmanlar = []
        gezegenler = [Actor("gezegen1", (random.randint(0, 600), -100)), Actor("gezegen2", (random.randint(0, 600), -100)), Actor("gezegen3", (random.randint(0, 600), -100))]
        meteorlar = []
        fuzeler = []
        doldurma()

    # Kontroller
    if (keyboard.left or keyboard.a) and uzayli.x > 20:
        uzayli.x = uzayli.x - 5
        if yeni_resim != 'sol':
            uzayli.image = 'sol'
            yeni_resim = 'sol'
    elif (keyboard.right or keyboard.d) and uzayli.x < 580:
        uzayli.x = uzayli.x + 5
        if yeni_resim != 'sag':
            uzayli.image = 'sag'
            yeni_resim = 'sag'
    elif keyboard.down or keyboard.s:
        if yeni_resim != 'egilme':
            uzayli.image = 'egilme'
            yeni_resim = 'egilme'
            uzayli.y = 250
    else:
        if uzayli.y > 240 and yeni_resim == 'egilme':
            uzayli.image = 'uzayli'
            yeni_resim = 'uzayli'
            uzayli.y = 240
    

    if oyun_sonu == 1 and keyboard.enter:
        oyun_sonu = 0 
        puan = 0
        uzayli.pos = (50, 240)
        kutu.pos = (550, 265)
        ari.pos = (850, 175)
        hiz = 5
    
    # Çarpışma
    if uzayli.colliderect(kutu) or uzayli.colliderect(ari):
        oyun_sonu = 1
        
def on_key_down(key):
    # Zıplama
    if keyboard.space or keyboard.up or keyboard.w:
        uzayli.y = 100
        animate(uzayli, tween='bounce_end', duration=2, y=240)

def on_mouse_down(button, pos):
    global mod, gemi
    if mod == 'menu' and gemi1.collidepoint(pos):
        gemi.image = "gemi1"
        mod = 'oyun'
    elif mod == 'menu' and gemi2.collidepoint(pos):
        gemi.image = "gemi2"
        mod = 'oyun'
    elif mod == 'menu' and gemi3.collidepoint(pos):
        gemi.image = "gemi3"
        mod = 'oyun'
    # Ateş Etmek
    elif mod == 'oyun' and button == mouse.LEFT:
        fuze = Actor("füzeler")
        fuze.pos = gemi.pos
        fuzeler.append(fuze)


#bir değişiklik yaptınf