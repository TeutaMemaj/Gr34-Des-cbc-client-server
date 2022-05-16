import socket
from Crypto.Cipher import DES


k3 = b'maNumescRebeccaa'

SERVER = "127.0.0.1"
PORT = 7000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


#Është marrë çelësi i enkriptimit
key =  client.recv(1024)
decipher = DES.new(k3, DES.MODE_ECB)
key_deciphered=decipher.decrypt(key)
print("The key received is :" , key_deciphered)

#Merret vektori i inicializimit
iv =  client.recv(1024)
decipher_iv = DES.new(k3, DES.MODE_ECB)
iv_deciphered=decipher_iv.decrypt(iv)
print("The iv received is :" , iv_deciphered)

#këtu doja të dërgoja modalitetin e enkriptimit nga KM, por nuk munda sepse nuk kishte sinkronizim në dërgimin e paketave, kështu që kërkova të rifusja modalitetin
print("Reenter the chosen mode ")
mode = input()

confirmation_message= b'maLumescBebeccaa'

#encrypt mesazh konfirmimi
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
clientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT2 = 7075

#inicializon komunikimin e drejtpërdrejtë me nyjen A nëse përgjigja KM është pozitive
if msg=='Initiate communication':
    blocks=[]
    clientA.connect((SERVER, PORT2))
    block_recv=clientA.recv(1024)
    # deshifroni çdo bllok dhe rikrijoni mesazhin përmes një liste në të cilën varet çdo bllok pas deshifrimit
    if mode == 'CBC':
        cipher_CBC = DES.new(key_deciphered,DES.MODE_CBC,iv_deciphered)
        block_dec=cipher_CBC.decrypt(block_recv)
        blocks.append(block_dec)
    if mode == 'CFB':
        cipher_CFB = DES.new(key_deciphered,DES.MODE_CFB,iv_deciphered)
        block_dec=cipher_CFB.decrypt(block_recv)
        blocks.append(block_dec)
    client.sendall(bytes(len(blocks)))
    for block in blocks:
        print (block)
    clientA.close()

client.close()
