import socket
from time import sleep
from secrets import randbelow


print("---------->> GENERATING CLIENT SERVER <<---------")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip = "127.0.0.1"
port = 8080

s.connect((ip,port))
print("\n-->CLIENT IS CONNECTED TO THE SERVER<---\n")

# # ------------->> RECEIVING THE PRI_NO. AND PRIM_ROOT + generaitng priv_key_client<<----------------
print("--------> RECEIVING DATA... <----------\n")
global private_key_of_client, prime_number, prim_root, public_client 	#all the 4 keys

rec_prime_number = s.recv(1024)
string = rec_prime_number.decode("utf-8")
prime_number = int(string)						    # final received prime number

rec_prim_root = s.recv(1024)
string_for_pr = rec_prim_root.decode("utf-8")
prim_root = int(string_for_pr)						# final received prim_root
				
private_key_of_client = randbelow(prime_number)		# final generated private key
# # ------------->> RECEIVING THE PRI_NO. AND PRIM_ROOT + generaitng priv_key_client<<----------------


#------>PRINTIGN ALL THE THREE KEYS<----------
print("--->PRIME NUMBER = ", prime_number,"<----")
print("--->PRIMITTIVE ROOT = ", prim_root,"<----")
print("--->PRIVATE KEY OF CLIENT = ",private_key_of_client,"<----\n")
#------>PRINTIGN ALL THE THREE KEYS<----------


#-------------> RECEIVING THE PUBLIC KEY AND SENDING CLIENT'S PUBLIC KEY<------
global public_server
key_string = s.recv(1024)
public_server = int(key_string.decode("utf-8"))		#RECEIVED
print("   ---> RECEIVED PUBLIC_SERVER KEY = ",public_server,"<---" )

public_client = int(pow(prim_root,private_key_of_client,prime_number))		#generating
print("   ---> GENERATED PUBLIC_CLIENT KEY = ",public_client,"<---" )
s.send(str(public_client).encode("utf-8"))			#sending
#-------------> RECEIVING THE PUBLIC KEY AND SENDING CLIENT'S PUBLIC KEY<------


##------------>> GENERATING SECRET_KEY <<-------------
global SECRET_KEY 
SECRET_KEY = int(pow(public_server,private_key_of_client,prime_number))
print("   --->## GENERATED SECRET KEY = ",SECRET_KEY," ##<---\n" )
##------------>> GENERATING SECRET_KEY <<-------------




##--------------->> CIPHER ENCRYPTION & DECRYPTION <<-----------##
def cipher_encrypt(non_encry_msg, encryption_key):
	encr_value = encryption_key
	encry_msg = ""

	series = "abcdefghijklmnopqrstuvwxyz"
	series += series.upper()
	# series += " "

	for letter in non_encry_msg:
		poisition = series.find(letter)
		newp = (poisition+encr_value)%52
		if letter == " ":
			encry_msg += " "
		else:
			encry_msg += series[newp]
	
	# print("encry_msg: - ",encry_msg,"\n")
	return encry_msg
def cipher_decrypt(encry_msg, encryption_key):
	decrypted = ""

	series = "abcdefghijklmnopqrstuvwxyz"
	series += series.upper()
	# series += " "

	for letter in encry_msg:
		poisition = series.find(letter)
		newp = (poisition-encryption_key)%52

		if letter == " ":
			decrypted += " "
		else:
			decrypted += series[newp]
	
	# print("decrypted: - ",decrypted,"\n")
	return decrypted	
##--------------->> CIPHER ENCRYPTION & DECRYPTION <<-----------##
	


# ---------------->>THE CLIENT CODE<<-----------------
print("---------->CLIENT PORTAL FOR CHAT<---------\n")
while True:
	#for receiving message
	rec_msg = s.recv(1024)
	rec_msg = rec_msg.decode("utf-8")	
	print("SERVER -", rec_msg, "    //",cipher_decrypt(rec_msg, SECRET_KEY))

	#for sending message
	message = input("CLIENT - ")
	if message == "exit()":
                exit()
	message = cipher_encrypt(message, SECRET_KEY)
	message = message.encode("utf-8")
	s.send(message)
# ---------------->>THE CLIENT CODE<<-----------------

	

		
	

