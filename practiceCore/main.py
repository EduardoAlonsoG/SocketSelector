import socket
import sys
import threading


def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr, listaconexiones])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def close_conn(conn):
    addr = conn.getpeername()
    print(f"Conexion liberada {addr}")
    conn.close()

def gestion_conexiones(listaconexiones):
    print("Actualizando conexiones...")
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    #print(listaconexiones)


def recibir_datos(conn, addr, lista_conexiones):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            data = conn.recv(1024)
            response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            if not data or data == b"exit":
                close_conn(conn)
                gestion_conexiones(lista_conexiones)
                break
            conn.sendall(response)
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = []
host, port, numConn = ("localhost", 65432, 100)

"""
if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)
"""

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones)