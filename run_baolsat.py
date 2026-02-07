import socket, qrcode, os

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally: s.close()
    return IP

if __name__ == "__main__":
    ip = get_ip()
    url = f"http://{ip}:5000"
    print(f"\n🚀 BAOLSAT ACTIVÉ\n🔗 ACCÈS : {url}\n")
    qr = qrcode.QRCode(box_size=1)
    qr.add_data(url)
    qr.print_ascii(invert=True)
    os.system("python app.py")