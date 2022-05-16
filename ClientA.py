import socket
from Crypto.Cipher import DES

#ky funksion është ai i mbushjes. llogarisni sa karaktere të tjera nevojiten derisa gjatësia e skedarit të jetë shumëfish i 16, më pas plotësoni me 0 karaktere
def padding(string):
    nr_blocs = (16 - len(text_to_pad) % 16) % 16
    string += chr(0) * nr_blocs
    return string

k3 = b'maNumescRebeccaa'


SERVER = "127.0.0.1"
PORT = 7000
PORT2 = 7075
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

#dërgoni mënyrën e dëshiruar të enkriptimit
mode = input()
client.sendall(bytes(mode,'UTF-8'))

#Çelësi KM u mor
key =  client.recv(1024)
decipher_key = DES.new(k3, DES.MODE_ECB)
key_deciphered=decipher_key.decrypt(key)
print("The key received is :" ,key_deciphered)

#ev merret iv nga KM
iv =  client.recv(1024)
decipher_iv = DES.new(k3, DES.MODE_ECB)
iv_deciphered=decipher_iv.decrypt(iv)
print("The iv received is :" ,iv_deciphered)

confirmation_message= b'maLumescBebeccaa'

#Dërgimi i mesazhit të konfirmimit të koduar sipas modalitetit të dëshiruar
if mode == 'CBC':
    cipher_CBC = DES.new(key_deciphered,DES.MODE_CBC,iv_deciphered)
    confirmation_message_cyphered=cipher_CBC.encrypt(confirmation_message)
    client.sendall(confirmation_message_cyphered)
elif mode == 'CFB':
    cipher_CFB = DES.new(key_deciphered,DES.MODE_CFB,iv_deciphered)
    confirmation_message_cyphered=cipher_CFB.encrypt(confirmation_message)
    client.sendall(confirmation_message_cyphered)

#Mesazh konfirmimi i kartës nga KM ose kundërshtim
data3 = client.recv(1024)
msg=data3.decode()
print(msg)

#Një komunikim i drejtpërdrejtë me nyjen B inicializohet nëse përgjigja KM është pozitive
if msg=='Initiate communication':
   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER, PORT))
    server.listen(1)

    clientB, clientAddress = server.accept()
  
    #krijo një listë që do të marrë blloqet e tekstit
    fileBlocks=[]
#hapni skedarin dhe aplikoni funksionin pad
    uncrypted_file=open('textDeCriptat', 'r')
    padding(uncrypted_file)
    #Ndani skedarin në blloqe 16-bitësh për aq kohë sa të jetë e mundur
    while(uncrypted_file):
        block = file.read(16)
        fileBlocks.append(block)
    # Çdo bllok është i koduar individualisht dhe dërgohet individualisht te B
    if mode == 'CBC':
       cipher_CBC =DES.new(key_deciphered,DES.MODE_CBC,iv_deciphered)
       for block in fileBlocks:
          block=cipher_CBC.encrypt(block)
          clientB.sendall(block)
    if mode == 'CFB':
       cipher_CFB = DES.new(key_deciphered,DES.MODE_CFB,iv_deciphered)
       for block in fileBlocks:
          block=cipher_CFB.encrypt(block)
          clientB.sendall(block)
    clientB.close()
    #se trimite catre KM numarul de blocuri criptate
    client.sendall(bytes(len(fileBlocks)))
else:
    print('We cant communicate any further')

client.close()
