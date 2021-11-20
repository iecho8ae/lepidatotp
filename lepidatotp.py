#!/usr/bin/python3

import argparse
from urllib.parse import urlparse, parse_qs
import webbrowser
import os

import qrcode

START_URL = 'https://id.lepida.it/lepidaid/app/associaAppLogin?1-1.0-loginSMS-loginDiv-loginForm-entra&X-App-Id=PROD-LEPIDAIDAPP-A&X-App-Version=2.0.0'

def decode_secret(secret: str) -> str:
    encoded = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    decoded = 'ORJ2LCE4BPSHAWFTU7YD3NZ5M6IXQGVK'
    res = []
    for c in secret:
        idx = encoded.find(c.upper())
        if idx == -1:
            raise RuntimeError(f"secret has character {c!r} not from the right set")
        else:
            res.append(decoded[idx])

    return "".join(res)

def main():
    parser = argparse.ArgumentParser(description='Uso di LepidaID con app TOTP standard e sicure')
    parser.add_argument("url", nargs="?", action="store", help="""URL con le
                        informazioni TOTP; se non specificato, fornisce
                        istruzioni per ottenerlo""")
    args = parser.parse_args()

    if args.url is not None:
        auth_url = args.url
    else:
        print(f'Vai su {START_URL} e segui le istruzioni.')
        print(f'Quando raggiungi una pagina che dice "end login page", incolla l\'URL qui:')
        webbrowser.open(START_URL, new=2)
        auth_url = input('URL: ')

    url = urlparse(auth_url)
    qs = parse_qs(url.query)
    key = qs["secretKey"][0]
    secret = decode_secret(key)

    otpauth = f"otpauth://totp/LepidaID?secret={secret}&algorithm=SHA1&period=30&digits=6&issuer=id.lepida.it"

    img = qrcode.make(otpauth)
    img.save("/tmp/qr.png")
    print("Scritto /tmp/qr.png. Ricordati di rimuoverlo.")
    webbrowser.open("/tmp/qr.png")

if __name__ == "__main__":
    main()
