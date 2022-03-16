import socket
from time import sleep
from math import sqrt
from secrets import randbelow


# ---------------------->>to find primittive root<<------------------
# Returns True if n is prime
def isPrime( n):

	# Corner cases
	if (n <= 1):
		return False
	if (n <= 3):
		return True

	# This is checked so that we can skip
	# middle five numbers in below loop
	if (n % 2 == 0 or n % 3 == 0):
		return False
	i = 5
	while(i * i <= n):
		if (n % i == 0 or n % (i + 2) == 0) :
			return False
		i = i + 6

	return True

""" Iterative Function to calculate (x^n)%p
	in O(logy) */"""
def power( x, y, p):

	res = 1 # Initialize result

	x = x % p # Update x if it is more
			# than or equal to p

	while (y > 0):

		# If y is odd, multiply x with result
		if (y & 1):
			res = (res * x) % p

		# y must be even now
		y = y >> 1 # y = y/2
		x = (x * x) % p

	return res

# Utility function to store prime
# factors of a number
def findPrimefactors(s, n) :

	# Print the number of 2s that divide n
	while (n % 2 == 0) :
		s.add(2)
		n = n // 2

	# n must be odd at this po. So we can
	# skip one element (Note i = i +2)
	for i in range(3, int(sqrt(n)), 2):
		
		# While i divides n, print i and divide n
		while (n % i == 0) :

			s.add(i)
			n = n // i
		
	# This condition is to handle the case
	# when n is a prime number greater than 2
	if (n > 2) :
		s.add(n)

# Function to find smallest primitive
# root of n
def findPrimitive( n) :
	s = set()

	# Check if n is prime or not
	if (isPrime(n) == False):
		print("try again!! (not prime)")
		return -1

	# Find value of Euler Totient function
	# of n. Since n is a prime number, the
	# value of Euler Totient function is n-1
	# as there are n-1 relatively prime numbers.
	phi = n - 1

	# Find prime factors of phi and store in a set
	findPrimefactors(s, phi)

	# Check for every number from 2 to phi
	for r in range(2, phi + 1):

		# Iterate through all prime factors of phi.
		# and check if we found a power with value 1
		flag = False
		for it in s:

			# Check if r^((phi)/primefactors)
			# mod n is 1 or not
			if (power(r, phi // it, n) == 1):

				flag = True
				break
			
		# If there was no power with value 1.
		if (flag == False):
			return r

	# If no primitive root found
	return -1
# ---------------------->>to find primittive root<<------------------



# -----------> PRIME N. AND PRIMITTIVE ROOT GENERATOR + private key<---------
global prime_number, prim_root, private_key_of_server, public_server	# 4 keys final
prime_number = int(input("ENTER A PRIME NUMBER = "))		# final prime number
prim_root = int(findPrimitive(prime_number))				# fianl prim_root
if prim_root == -1:
        sleep(2)
        exit()
print("CALCULATING PRIMITTIVE ROOT...\n")
sleep(0.5)


#-------> private number generator <---------------
private_key_of_server = randbelow(prime_number)				# final private key 
#-------> private number generator <---------------

# --->PRINTING THE DATA OF ALL THE THREE KEYS<----
print("-->   PRIME NUMBER = ",prime_number," <-----") 
print("-->   PRIMITTIVE ROOT = ",prim_root," <-----") 
print("-->   PRIVATE KEY OF SERVER = ",private_key_of_server," <-----") 
# --->PRINTING THE DATA OF ALL THE THREE KEYS<----
# -----------> PRIME N. AND PRIMITTIVE ROOT GENERATOR + private key<---------


# -------------->generating and receiving connection<---------------
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("\n--------------->SERVER GENERATING<-----------------")
ip = "127.0.0.1"
port = 8080

s.bind((ip,port))
s.listen(2)
print("--------->CONNECTING... WITH THE CLIENT<--------")
conn,addr = s.accept()
print("connected!!\n")
# -------------->generating and receiving connection<---------------


# # ----------> after connecting with the client    (sending pr_n. and prim_root) <-----------------
# print("\n -->SENDING PRIME NUMBER AND PRIMMITVE ROOT TO THE CLIENT <--\n")
conn.send(str(prime_number).encode("utf-8"))
conn.send(str(prim_root).encode("utf-8"))
# # ----------> after connecting with the client    (sending pr_n. and prim_root) <-----------------


## -------------------> GENERATING PUBLIC KEY  + sending<------------------
public_server = int(pow(prim_root,private_key_of_server,prime_number))		#generating
print("   ---> GENERATED PUBLIC_SERVER KEY = ",public_server,"<---" )

conn.send(str(public_server).encode("utf-8"))					#sending

global public_client
key_string = conn.recv(1024)
public_client = int(key_string.decode("utf-8"))		#RECEIVED
print("   ---> RECEIVED PUBLIC_CLIENT KEY  = ",public_client,"<---" )
## -------------------> GENERATING PUBLIC KEY  + sending<------------------

##------------>> GENERATING SECRET_KEY <<-------------
global SECRET_KEY 
SECRET_KEY = int(pow(public_client,private_key_of_server,prime_number))
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
	



# ---------------->>THE SERVER CODE<<-----------------
print("---------->SERVER PORTAL FOR CHAT<---------\n")
while True:
	#for sending message
	message = input("SERVER - ")
	if message == "exit()":
                exit()
	message = cipher_encrypt(message, SECRET_KEY)
	message = message.encode("utf-8")
	conn.send(message)
	
	
	#for receiving message
	rec_msg = conn.recv(1024)
	rec_msg = rec_msg.decode("utf-8")
	print("CLIENT -",rec_msg,"    //",cipher_decrypt(rec_msg, SECRET_KEY))
# ---------------->>THE SERVER CODE<<-----------------

	print("pranshu");

		
	

