import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print("El nombre de su computadora es: " + hostname)
print("La dirección IP de su computadora es: " + ip)

#Crea socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF.INET = IPv4, SOCK_STREAM = TCP.
client_socket.connect((ip, 12345))  #se conecta a una ip, y un puerto definido que se usa para conectarse

while True:
    #Recibe pregunta del servidor
    respuesta = client_socket.recv(1024).decode()

    #Recibe pregunta del servidor
    respuesta_00 = input(respuesta + " ")

    #Envio respuesta
    client_socket.send(respuesta_00.encode())
    
    if (respuesta_00 == "/adios"):
        break

#cierre de conexion
client_socket.close()