import socket
import sys
import pyDes

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)


txt = open("mensajeentrada.txt","r")
menEntrtxt = txt.read()
txt.close()
# P=primo G= 0<G<P  a,b = 0<a,b<P-1
a = 15
P = 103
G = 35

A=(G**a)%P

K = 0  #inicialmente no hay llave
salt = "Kryzpo-T0ma2-tiuque-12"

try:

    # Send data
    num=str(G)+","+str(P)+","+str(A)
    mes =bytes(num, 'utf-8') #G,P,A
    print('sending {!r}'.format(mes))
    sock.sendall(mes)

    # Look for the response
    amount_received = 0
    
    # El cliente ha enviado el mensaje a server?
    sendmens = False

    while amount_received <= 0:
        data = sock.recv(16)
        amount_received += len(data)
        #print('received {!r}'.format(data))

        # resuesta (B) a datos
        res = data.decode("utf-8")

        try:
            B=int(res)
            
            # hacemos llave
            K = (B**a)%P
            #print("key is: ",K)
        except:
            pass

        if sendmens == False:
            key = bytes(str(K)+salt, 'utf-8')
            k = pyDes.triple_des(key, pad=None, padmode=pyDes.PAD_PKCS5)
            message = bytes(menEntrtxt, 'utf-8')
            
            #print('sending {!r}'.format(message))
            
            d = k.encrypt(message)
            print ("Encrypted: %r" % d)
            sock.sendall(d)

finally:
    print('closing socket')
    sock.close()
