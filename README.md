# RSA-Implementation with AES

This project implements a system that uses AES to encrypt data and RSA to protect AES keys. 

It consists of two programs one to generate the RSA Public and Private keys and another to encrypt and decrypt the data using AES. 

genkeys.py:
<br/>The program genkeys.py is used to generate the RSA Public and Private keys (e, N) and (d, N) where N is the product of two prime numbers p and q. N is 2048 bits. p and q are prime numbers generated using Miller-Rabin primality test and random() function. The Private and Public keys are stored in the output files alice.prv and alice.pub respectively.

crypt.py:
<br/>The second program crypt.py performs the encryption using AES. This program uses the pycrypto library to implement AES encryption. The AES key of 128 bits is generated using a random function random.SystemRandom(). This key is then encrypted using RSA encryption. The keys generated by the first program are used by the RSA encryption for encrypting the AES key. 
The program takes four command line arguments: a single flag –e or –d indicating whether the program will encrypt or decrypt a message, the name of the public or private key file to use generated by keygen.py, the name of the file to encrypt or decrypt, and the name of the output file to save the encrypted or decrypted data. 


Usage:<br/>
```./genkeys.py alice```
<br/>to generate public and private keys for alice and store it in the files alice.pub and alice.prv respectively

```./crypt.py -e alice.pub message.txt message.cip```
<br/>to encrypt the contents of message.txt using the public key and save the encryption in message.cip

```./crypt.py -d alice.prv message.cip message.txt```
<br/>to decrypt the contents of message.cip using the ptivate key and save the encryption in message.txt

