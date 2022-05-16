import socket, threading
from Crypto.Cipher import DES


LOCALHOST = "127.0.0.1"
PORT = 7000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))


k3 = b'maNumescRebeccaa'
k1_CBC = b'numeleMeuEsteRbk'
k2_CFB = b'nuStiuSaFacTema!'
iv = b'amNevoieDeAjutor'

#krijoni shifrën për enkriptimin e çelësave dhe iv
des = DES.new(k3, DES.MODE_ECB)


#çelësat enkriptues dhe iv
k1_CBC=des.encrypt(k1_CBC)
#print ("cheia1 criptata este ",k1_CBC)

k2_CFB=des.encrypt(k2_CFB)
#print ("cheia2 criptata este ",k2_CFB)

iv=des.encrypt(iv)
#print ("iv-ul criptat este ",iv)

#decipher = DES.new(k3, DES.MODE_ECB)
#print("cheia1 decriptata este",decipher.decrypt(k1_ECB))

#Filloni komunikimin
server.listen(2)
print("Server started")
print("Waiting for client request..")

#krijo lidhjen me nyjen A
clientsockA, clientAddress = server.accept()
print ("New connection added: ", clientAddress)
print("Choose between CBC or CFB")
nodeA =  threading.Thread()
nodeA.start()

#merr mënyrën e dëshiruar të enkriptimit
data = clientsockA.recv(1024)
received_enc_mode = data.decode()
print ("Wanted ecryption mode ", received_enc_mode)


#krijo lidhjen me nyjen B
clientsockB, clientAddress = server.accept()
print ("New connection added: ", clientAddress)
nodeB = threading.Thread()
nodeB.start()


#dërgo çelësin e duhur në modalitetin e zgjedhur
if received_enc_mode == 'CBC':
    
    clientsockA.sendall(k1_CBC)
    clientsockA.sendall(iv) 
    clientsockB.sendall(k1_CBC)
    clientsockB.sendall(iv)
elif received_enc_mode == 'CFB':
    
    clientsockA.sendall(k2_CFB)
    clientsockA.sendall(iv) 
    clientsockB.sendall(k2_CFB)
    clientsockB.sendall(iv)
  
mode2=received_enc_mode

confirmation_message_cyphered_CBC=''
confirmation_message_cyphered_CFB=''

# Krahasoni mesazhet e marra nga secila nyje dhe jepni ok për komunikim të sigurt
if mode2 == 'CBC':
   
    testA_recv = clientsockA.recv(1024)
    cipher_CBC = DES.new(k1_CBC,DES.MODE_CBC,iv)
    testA = cipher_CBC.decrypt(testA_recv)

    testB_recv = clientsockB.recv(1024)
    cipher_CBC = DES.new(k1_CBC,DES.MODE_CBC,iv)
    testB = cipher_CBC.decrypt(testB_recv)
  
    if testA == testB:
         print("criptare cu succes")
         clientsockA.sendall(bytes('Initiate communication','UTF-8'))
    else:
        print("nu a avut loc o criptare corecta")
elif mode2 == 'CFB':
    testA_recv = clientsockA.recv(1024)
    cipher_CFB =DES.new(k2_CFB,DES.MODE_CFB,iv)
    testA = cipher_CFB.decrypt(testA_recv)

    testB_recv = clientsockB.recv(1024)
    cipher_CFB = DES.new(k2_CFB,DES.MODE_CFB,iv)
    testB = cipher_CFB.decrypt(testB_recv)

    if testA == testB:
         print("criptare cu succes")
         clientsockA.sendall(bytes('Initiate communication','UTF-8'))
         clientsockB.sendall(bytes('Initiate communication','UTF-8'))

    else:
        print("nu a avut loc o criptare corecta")

# merr numrin e blloqeve të koduara nga A

blocksA=clientsockA.recv(1024)
nr_blocksA=blocksA.decode()
print(nr_blocksA," were send and decrypted from A")

#se primeste numarul de blocuri criptate de la B
blocksB=clientsockB.recv(1024)
nr_blocksB=blocksB.decode()
print(nr_blocksB," were send and decrypted from A")

# krahasoni numrin e blloqeve të enkriptuara nga çdo nyje dhe jepni një mesazh specifik
if nr_blocksA == nr_blocksB:
  print("File successfully encrypted")
else:
  print("Failed to encrypt the file")


nodeA.join()
nodeB.join()
