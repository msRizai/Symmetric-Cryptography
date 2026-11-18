#!/usr/bin/env python3
from datetime import datetime, timedelta
import requests

def request_cookie():
    r = requests.get("http://aes.cryptohack.org/flipping_cookie/get_cookie/")
    return r.json()["cookie"]

def request_check_admin(cookie, iv):
    r = requests.get("http://aes.cryptohack.org/flipping_cookie/check_admin/{}/{}/".format(cookie, iv))
    return r.json()

expire_date = (datetime.today() + timedelta(days=1)).strftime("%s")
plain = f"admin=False;expiry={expire_date}".encode()
cookie = request_cookie()
cookie = bytes.fromhex(cookie)
fake_iv = [0x00]*16
cipher_fake = list(cookie)
fake = b';admin=True;' #True is 4 char but False is 5 so yo put a ; to even out
for i in range(len(fake)):
    cipher_fake[16+i] = plain[16+i] ^ cookie[16+i] ^ fake[i]
    fake_iv[i] = plain[i] ^ cookie[i] ^ fake[i]

cipher_fake = bytes(cipher_fake).hex()
fake_iv = bytes(fake_iv).hex()
print(request_check_admin(cipher_fake, fake_iv))