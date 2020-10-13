import socket
import sys
import pyDes

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# b
b = 67
K = 0  #inicialmente no hay llave
salt = "Kryzpo"

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            try:
                # revisamos si hay mensaje de client
                datarecv = connection.recv(16)
                #print('received {!r}'.format(datarecv))

                if K <= 0: # se recive (G,P,A)
                    #mensaje (G,P,A) a datos
                    men = format(datarecv).replace("b","").replace("'","").split(",")
                    try:
                        G = int(men[0])
                        P = int(men[1])
                        A = int(men[2])
                    
                        B = str((G**b)%P)
                        data = bytes(B, 'utf-8')

                        # hacemos llave
                        K = (A**b)%P
                        #print("key is: ",K)
                    except:
                        pass
                else:
                    key = bytes(str(K)+salt, 'utf-8')
                    k = pyDes.des(key, pad=None, padmode=pyDes.PAD_PKCS5)

                    #mencrip = format(datarecv)
                    print('received {!r}'.format(datarecv))
                    print("Decrypted: %r" % k.decrypt(datarecv))
    
            except:
                # no hay mensaje
                data = False

                     
            if data:
                # enviamos B a client
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
