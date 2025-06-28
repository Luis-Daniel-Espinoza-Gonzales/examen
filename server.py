import socket
import requests

clave = {
    "usuario" : "daniel",
    "contraseña" : "den1"
}


#Obtetncion de nombre e IP del equipo
hostname = socket.gethostname() #Obtiene el nombre del equipo
ip = socket.gethostbyname(hostname) #Traduce el nombre en una IP
print("El nombre de su computadora es: " + hostname)
print("La dirección IP de su computadora es: " + ip)

#Configuraciones del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF.INET = protocolo IPv4, SOCK_STREAM = tipo de socket TCP.
server_socket.bind((ip, 12345)) #se asigna ip y puerto definido donde se escucha
server_socket.listen(1) #Indica cuantas conexiones puede mantener

print("server escuchando en el puerto 12345")

while True:

    #Crea socket
    client_socket, address = server_socket.accept()
    print("se establecio una conexion con " + str(address))

    #Envio saludo
    client_socket.send("hola, te envio saludo desde el servidor.".encode())

    #Envio pregunta
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
        client_socket.send("Acceso concedido. Bienvenido.".encode())

        if respuesta_01 == "/repos":
            url = 'https://pokeapi.co/api/v2/generation/1/'
            data = requests.get(url)

            if(data.status_code == 200):
                data = data.json()
                client_socket.send("Estos son todos los movimientos de la region de kanto".encode())
                cant = 0

                print(data["moves"])
                

        elif respuesta_01 == "/adios":
            mensaje_adios = "Hasta luego."
            client_socket.send(mensaje_adios.encode())
            client_socket.close()
    else:
        print("acceso denegado.")
        client_socket.send("Acceso denegado. Cerrando conexión.".encode())
        client_socket.close()