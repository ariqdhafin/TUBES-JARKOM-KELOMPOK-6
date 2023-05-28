from socket import *    # Modul socket berfungsi untuk membuat soket server
from threading import * # Modul threading berfungsi untuk membuat dan mengelola thread
import sys              # akan digunakan sys.exit() yang berfungsi menghentikan program

serverSocket = socket(AF_INET, SOCK_STREAM) # Membuat socket server yang disebut serverSocket. AF_INET menandakan jaringan menggunakan IPv4. SOCK_STREAM menandakan soket bertipe SOCK_STREAM yang berarti soket TCP
serverHost = '192.168.56.1'     # Menetapkan IP menjadi '192.168.56.1' dan dimasukan kedalam variabel serverHost
serverPort = 8080               # Menetapkan port menjadi '8080' dan dimasukan kedalam variabel serverHost
serverSocket.bind((serverHost, serverPort)) # Mengikat serverSocket dengan serverHost dan serverPort
serverSocket.listen(1)                      # Server akan mulai mendengarkan permintaan koneksi TCP dari klien. Parameter menentukan jumlah maksimum koneksi antrian (setidaknya 1).
print("[STARTING] Server is starting...")   # Menandakan server akan mulai
print(f"[LISTENING] Server is listening on {serverHost}:{serverPort}")  # Menampilkan IP dan port server

def content_type(filename):                 # Fungsi untuk mengetahui tipe file yang dimina client
    type = filename[1:].split('.')[1]
    if type=="html":
        return "text/html"
    elif type=="css":
        return "text/css"
    elif type=="jpg" or type=="jpeg":
        return "image/jpeg"
    elif type=="gif":
        return "image/gif"
    elif type=="png":
        return "image/png"
    else:
        return "text/plain"

def handle_client(connectionSocket, addr):                              # Fungsi untuk mengurusi request dari klien
    print(f"[NEW CONNECTION] {addr} connected.")                        # Menampilkan IP dan port koneksi yang baru
    
    try:
        message = connectionSocket.recv(9999).decode()                  # Menerima data dari klien dan mengubahnya menjadi string
        filename = message.split()[1]                                   # Memisah message dan dipilih kata idex 1
        f = open(filename[1:], "rb")                                    # Membuka filename dalam format biner 
        outputdata = f.read()                                           # Membaca file yan diminta
        
        print(f"FROM [{addr}] REQUEST {filename[1:]}")                  # Menampilkan nama file yang diminta oleh suatu klien
        
        tipe = content_type(filename)                                   # Memanggil fungsi content_type
        panjang = str(len(outputdata)) 
        header = 'HTTP/1.1 200 OK\r\nContent-Type: ' + tipe + '\r\nContent-Length: ' + panjang + '\r\n\r\n'# Menyusun header http 

        response = header.encode() + outputdata                         # Memasukkan header dan ouputdata ke dalam response 
        connectionSocket.send(response)                                 # Mengirimkan response ke klien
        connectionSocket.send("\r\n".encode())                          # Menutup connectionSocket
        connectionSocket.close()
    except IOError:
        print(f"FROM [{addr}] REQUEST {filename[1:]}")                  # Menampilkan nama file yang diminta oleh suatu klien
        header = 'HTTP/1.1 404 Not Found\r\n\r\n'                       # Mengirimkan 404 Not Found jika file tidak ditemukan
        html = '<h1>404 Not Found</h1><p>The requested file was not found.</p>' # Menampilkan halaman 404 Not Found
        response = (header + html).encode()                             # Memasukkan header dan html kedalam response
        connectionSocket.send(response)                                 # Mengirimkan response
        connectionSocket.close()                                        # Menutup connectionSoscket
    print(f"[CONNECTION CLOSED ] {addr} Connection is closed.")           # Menampilkan bahwa koneksi dengan klien sudah berakhir
    print(f"[ACTIVE CONNECTIONS] {active_count()-2}\n")                   # Menampilkan berapa koneksi yang aktif

while True:                                             # Program akan berjalan terus menerus
    print(f"[ACTIVE CONNECTIONS] {active_count()-1}\n")   # Menampilkan berapa koneksi yang aktif 
    connectionSocket, addr = serverSocket.accept()      # Ketika menerima koneksi dari client metode accept() akan dipanggil untuk membuat soket baru yang disebut connectionSocket khusus untuk klien ini
    thread = Thread(target=handle_client, args=(connectionSocket, addr))    # Membuat thread baru deangan parameter target handle_client dan argumenya connectionSocket, addr
    thread.start() # Memulai eksekusi thread
    
serverSocket.close()
sys.exit()


