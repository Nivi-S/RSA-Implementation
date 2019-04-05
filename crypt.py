#import libraries
import sys, getopt
import os
from Crypto.Cipher import AES
import random
import base64
from Crypto import Random

import math
import base64


#parsing command line arguments
total = len(sys.argv)
cmdargs = str(sys.argv)
try:
    options, args = getopt.getopt(sys.argv[1:],"e:d:")
except getopt.GetoptError as e:
    print (str(e))
    print("Usage: %s -e to encrypt -d to decrypt" % sys.argv[0])
    sys.exit(2)
	

#set random 128 bit AES key
systemRandom = random.SystemRandom()
key = systemRandom.randrange(1000000000000000,9999999999999999)

key = str(key)
iv = Random.new().read(AES.block_size)


#padding logic
BS = 16
pad = lambda s: bytes(s+(16 - len(s)%16)*chr(BS - len(s) % BS), encoding='utf-8')
unpad = lambda s : s[0:-ord(s[-1:])]


#RSA Encryption
def encrypt(msg, public_key, n):
    n = n
    e = public_key
    n = int(n)
    e = int(e)
    Kprime = ''

    for i in range(len(msg)):
        int_msg = ord(msg[i]) # pick each char and convert to str
        Kprime += str(pow(int_msg,e, n))+ " "

    return Kprime


#RSA decryption
def decrypt(msg, private_key,n):
    n = n 
    d = private_key
    n = int(n)
    d = int(d)
    decrypted = ''

    asc_msg = msg.split(" ")
    del asc_msg[-1]

    for i in range(len(asc_msg)):
        asc_msg[i] = int(asc_msg[i])
    # start looping each numbers
    for num in asc_msg:
        num = int(num) # convert to integer

        decrypted += str(chr(pow(num,d, n))) 

    return decrypted



#define class for AES encryption
class AESCipher:
	def encrypt( self, raw ):
		raw = pad(raw)
		cipher = AES.new( key.encode('utf-8'), AES.MODE_ECB) #, iv )
		return base64.b64encode( cipher.encrypt(raw))
	def decrypt( self, enc ):
		enc = base64.b64decode(enc)
		cipher = AES.new(AESkey.encode('utf-8'), AES.MODE_ECB)#, iv )
		return cipher.decrypt(enc)



#checking for argument parsed from cmd and executing encryption or decryption
for o, a in options:

	#Encrypt if flag is -e
    if o == '-e':
        print('encrypting ...')

        #retreiving data from file
        f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+str(sys.argv[2]), "r")   # 'r' for reading and 'w' for writing
        lines = f.read()
        n = lines[:610]
        e = lines[610:]
        print('retreived e=',e)
        print('retreived n=',n)

        # e = int(e)
        # n = int(n)

        #RSA encryption for AES key
        Kprime = encrypt(key,e,n)
        # cipher = [(pow(ord(a),e,n)) for a in key]
        # s = [str(i) for i in cipher]
        # Kprime = str(''.join(s))


        #retreiving data from file
        f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+str(sys.argv[3]), "r")   # 'r' for reading and 'w' for writing
        data = f.read()

        cipher = AESCipher()
        #AES Encryption
        encrypted = cipher.encrypt(data)
        print ("encrypted=",encrypted)
        E = encrypted.decode() 
        f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+str(sys.argv[4]), "w")   # 'r' for reading and 'w' for writing
        #f.write(E+str(s))    # Write inside file
        f.write(E+str(Kprime))
        f.close()                # Close file 



    #Decrypt if flag is -d
    elif o == '-d':
        print('decrypting ...')

        f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+str(sys.argv[2]), "r")   # 'r' for reading and 'w' for writing
        lines = f.read()
        n = lines[:610]
        d = lines[610:] 
        print('retreived d=',d)
        print('retreived n=',n)
        # d = int(d)
        # n = int(n)

        #retreiving data from file
        f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+str(sys.argv[3]), "r")   # 'r' for reading and 'w' for writing
        E = f.read()
        ke = E[64:]
        encrypteddata = E[:64]
        # keyor = list()
        # for i in range(0,len(ke), 3):
        #     keyor.append((''.join(str(ke[i]))))

        # for i in range(len(keyor)):
        #     keyor[i] = int(keyor[i])


        #RSA decryption
        AESkey = decrypt(ke,d,n)
        #plain = [chr((a**d) % n) for a in keyor]
        # plain = [chr(pow(a,d,n)) for a in keyor]
        # plaint=''.join(plain)
        # print('decrypted AES=', plain)
        # AESkey=plaint.encode('ascii')
        # print('AES key=',AESkey)


        cipher = AESCipher()
        #AES decryption
        decrypted = cipher.decrypt(encrypteddata)
        unpad = unpad(decrypted.decode('utf-8'))
        print ('decrypted=', unpad)
        f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+str(sys.argv[4]), "w")   # 'r' for reading and 'w' for writing
        f.write(unpad)    # Write inside file 
        f.close()



