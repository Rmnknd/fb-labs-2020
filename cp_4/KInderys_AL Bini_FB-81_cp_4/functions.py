import numpy as np
import math
import random
import requests


def inverse_a_mod_n(a, n):
    if a == 0:
        return 0
    m = n
    q = np.zeros(10000, dtype=int)
    i = 0
    while n % a:
        q[i] = -(n / a)
        i += 1
        n, a = a, n % a
    q[i] = -(n / a)
    a_1 = np.zeros(len(q), dtype=int)
    a_1[1] = 1
    a_1[2] = q[0]
    for j in range(2, i + 1):
        j += 1
        a_1[j] = q[j - 2] * a_1[j - 1] + a_1[j - 2]
    return a_1[i + 1] % m


def x2d_mod_p(x, d, p):
    bin_d = bin(d)[:1:-1]
    result = x
    x2bin_d_i = x
    for i in range(1, len(bin_d)):
        x2bin_d_i = x2bin_d_i ** 2 % p
        if bin_d[i] == '1':
            result = (result * x2bin_d_i) % p
    return result


def miller_rabin(p):
    k = 64
    s = 0
    d = p - 1
    while d % 2 == 0:
        s += 1
        d = d // 2
    for i in range(k):
        x = random.randint(2, p - 1)
        if math.gcd(x, p) > 1:
            return False
        else:
            x_r = x2d_mod_p(x, d, p)
            if x_r == 1 or x_r == p - 1:
                continue
            for r in range(1, s):
                x_r = (x_r ** 2) % p
                if x_r == -1:
                    break
                elif x_r == 1:
                    return False
    return True


def prime(length):
    n0 = 2 ** length
    n1 = 2 ** (length + 1) - 1
    # print("prime from ", n0, " to ", n1)
    p = random.randint(n0, n1)
    if p % 2 == 0:
        p += 1
    while not miller_rabin(p):
        p += 2
    return p


def generate_key_pair(key_len):
    mIn = 2 ** key_len
    mAx = 2 ** (key_len + 1) - 1
    p = prime(key_len // 2)
    q = prime(key_len // 2)
    while mIn <= p * q <= mAx:
        q = prime(key_len // 2)
    n = p * q
    fi_n = (p - 1) * (q - 1)
    e = random.randint(2, fi_n - 1)
    while math.gcd(e, fi_n) > 1:
        e = random.randint(2, fi_n - 1)
    d = inverse_a_mod_n(e, fi_n)
    open_key = [n, e]
    secret_key = [d, p, q]
    return [open_key, secret_key]


def encrypt(pub_k, msg):
    cipher_msg = x2d_mod_p(msg, pub_k[1], pub_k[0])
    return cipher_msg


def decrypt(C, d, n):
    M = x2d_mod_p(C, d, n)
    return M


def sign(k, n1, e1, d, n):
    k1 = x2d_mod_p(k, e1, n1)
    S = x2d_mod_p(k, d, n)
    S1 = x2d_mod_p(S, e1, n1)
    return [hex(k1)[2:], hex(S1)[2:]]


def verify(k1, S1, n1, d1, e, n):
    k = x2d_mod_p(k1, d1, n1)
    S = x2d_mod_p(S1, d1, n1)
    k2check = x2d_mod_p(S, e, n)
    if k2check == k:
        return [True, k]
    else:
        return [False, k]

def receive():
    """тут код через получающий ключ шифртекст и подпись с сайта http://asymcryptwebservice.appspot.com/?section=rsa
    пускай S полученый шифр текст, k подаись, pk открытый ключ с сайта все получаем в 16 системе
    """
    keysender = requests.get("http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize=512")
    modul = (int(keysender.json()["modulus"],16))
    publicE = (int(keysender.json()["publicExponent"], 16))
    return (modul, publicE)
def send(modul, publicE):
    [public_key1, private_key1] = generate_key_pair(512)
    [public_key, private_key] = generate_key_pair(512)
    if public_key[0] > public_key1[0]:
        [public_key, private_key] = generate_key_pair(512)
    M = random.randint(2, 99999)
    print("M = ", M)
    msg = sign(M, public_key1[0], public_key1[1], private_key[0], public_key[0])
    print(msg)
    """тут код отправляющий ключи шифртекст и подаись на сайт http://asymcryptwebservice.appspot.com/?section=rsa """
    destination = requests.get('http://asymcryptwebservice.appspot.com/?section=rsa')
    print(destination.status_code)
   # if destination.status_code == 200:
    payload = {"message":(msg[0]),"type":"BYTES","signature":(msg[1]),"modulus":hex(public_key1[1])[2:],"publicExponent":hex(public_key1[0])[2:]}
    payloadgen =  {"message":(msg[0]),"type":"BYTES","signature":(msg[1]),"modulus":modul,"publicExponent":publicE}
    sender = requests.get("http://asymcryptwebservice.appspot.com/rsa/verify",params=payload)
    print(sender.json())
    sendgen = requests.get('http://asymcryptwebservice.appspot.com/rsa/verify',params=payloadgen,cookies=sendgen.cookies)
    #sendgen = requests.get('http://asymcryptwebservice.appspot.com/rsa/verify',cookies=sendgen.cookies)


"""
[public_key, private_key] = generate_key_pair(512)
print(public_key[0], hex(public_key[0]))
print()
print(public_key[1], hex(public_key[1]))
print()
print(private_key[0], hex(private_key[0]))
print()
msg = random.randint(2, 99999)
print(msg, hex(msg))
print()
C = encrypt(public_key, msg)
print(hex(C))
"""