import socket
import requests
import threading

#Obtetncion de nombre e IP del equipo
hostname = socket.gethostname() #Obtiene el nombre del equipo
ip = socket.gethostbyname(hostname) #Traduce el nombre en una IP

clave = {
    "usuario" : "daniel",
    "contraseña" : "den1"
}

def manejo(client_socket, address):
    while True:

        try:
            client_socket.send("hola, te envio saludo desde el servidor.".encode())

            pregunta_00 = "Ingrese su usuario:"
            client_socket.send(pregunta_00.encode())

            #Recibir repuesta
            respuesta_00 = client_socket.recv(1024).decode()
            print("Usuario del cliente: ", respuesta_00)

            #verifica el usuario y contraseña
            if respuesta_00 == clave["usuario"]:
                print("acceso concedido.")

                #Envio algo
                client_socket.send(b"\n=== Bienvenido al Chat ===\n1. /repos (para pedir los movimientos de combate de la region de kanto)\n2. /adios (fin de la comunicacion)\nElige una opcion: ")

                #Recibir repuesta
                respuesta_01 = client_socket.recv(1024).decode()

                if respuesta_01 == "/repos":
                    url = 'https://pokeapi.co/api/v2/generation/1/'
                    data = requests.get(url)

                    if(data.status_code == 200):
                        data = data.json()
                        asd_00 = data.get("moves")
                        asd_01 = asd_00[0]["name"]

                        print(asd_01)
                        client_socket.send(f"Estos son todos los movimientos de la region de kanto {asd_01}".encode())
                        

                elif respuesta_01 == "/adios":
                    mensaje_adios = "Hasta luego."
                    client_socket.send(mensaje_adios.encode())
                    client_socket.close()
            else:
                print("acceso denegado.")
                client_socket.send("Acceso denegado. Cerrando conexión.".encode())
                client_socket.close()
        except Exception as e:
            print(e)
            break
    client_socket.close()


#Configuraciones del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF.INET = protocolo IPv4, SOCK_STREAM = tipo de socket TCP.
server_socket.bind((ip, 12345)) #se asigna ip y puerto definido donde se escucha
server_socket.listen() #Indica cuantas conexiones puede mantener
while True:
    
    client_socket, address = server_socket.accept()
    print("server escuchando en el puerto 12345")

    hilo = threading.Thread(target=manejo , args=(client_socket, address))
    hilo.start()

            
            