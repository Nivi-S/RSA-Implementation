import math
import base64
import random
import sys

systemRandom = random.SystemRandom()
i1 = systemRandom.randrange(0,100)
i2 = systemRandom.randrange(0,100)


KEY_INT = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# we define the near max value to get its random number for key



def miller_rabin_prime(n):    
	# Miller-Rabin primality test.
 
	# A return value of False means n is certainly not prime. A return value of
	# True means n is very likely a prime.
	
	num_trials = 5 # number of bases to test
	assert n >= 2 # make sure n >= 2 else throw error
	# special case 2
	if n == 2:
		return True
	# ensure n is odd
	if n % 2 == 0:
		return False
	# write n-1 as 2**s * d
	# repeatedly try to divide n-1 by 2
	s = 0
	d = n-1
	while True:
		quotient, remainder = divmod(d, 2) # here we get the quotient and the remainder
		if remainder == 1:
			break
		s += 1
		d = quotient
	assert(2**s * d == n-1) # make sure 2**s*d = n-1
 
	# test the base a to see whether it is a witness for the compositeness of n
	def try_composite(a):
		if pow(a, d, n) == 1: # defined as pow(x, y) % z = 1
			return False
		for i in range(s):
			if pow(a, 2**i * d, n) == n-1:
				return False
		return True # n is definitely composite
 
	for i in range(num_trials):
		# try several trials to check for composite
		a = random.randrange(2, n)
		if try_composite(a):
			return False
 
	return True # no base tested showed n as composite

def compute_pqnt():
	# Generate two random prime numbers, get n and compute the totient also

	# generate p and q primes
	try:
		p = findAPrime(2, KEY_INT)
		while True:
			q = findAPrime(2, KEY_INT)
			if q != p:
				break
	except:
		raise ValueError
	#compute for n
	n = p * q
	# get the totient
	t = (p-1) * (q-1)
	#print (t)
	# return p, q, n and the totient
	return(p, q, n, t)

def findAPrime(a, b):
	# Return a pseudo prime number roughly between a and b, (could be larger than b). 
	# Raise ValueError if cannot find a pseudo prime after 10 * ln(x) + 3 tries.
	x = random.randint(a, b)
	for i in range(0, int(10 * math.log(x) + 3)):
		if miller_rabin_prime(x):
			return x
		else:
			x += 1 #increase x with 1 and try again
	raise ValueError

def coprime(a):
	# find the coprime of a in range 1-a'''
	# we will choose a prime number so we can only check that e is not a divisor of t    
	while True:
		co_p = findAPrime(1, a) # try to find a prime number
		# make surethe gcd is 1
		g, x, y = extended_gcd(co_p, a)
		# g is the remainder (last)
		if co_p < a and g == 1:
			break
	return co_p


def compute_e(t):
	# get a number between 1 and the toient that is coprime of the totient

	e = coprime(t)
	return e

def compute_d(e, t):
	# get d which is e(mod φ(n)) where φ(n) is the totient (t)

	d = modinv(e, t) # get the mod inverse
	return d

def extended_gcd(aa, bb):
	# using Extended Euclidean algorithm to
	# calculate gcd (greatest common divisor)

	lastremainder, remainder = abs(aa), abs(bb)
	x, lastx, y, lasty = 0, 1, 1, 0
	while remainder:
		lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder) # get the remainder and quotient
		x, lastx = lastx - quotient*x, x
		y, lasty = lasty - quotient*y, y
	return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
	# compute modular multiplicative inverse 
	# implementation of gcd with modulo, the last 
	# remainder should be 1 and lastx mod m is the mod inverse
	
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

#Write the public and private keys into the filename specifies by cmd argument
def print_keys():
	#print ("\nPublic Key (n, e)")
	p, q, n, t = compute_pqnt()
	e = compute_e(t)
	# print the public key
	print('Writing public key to file: '+ str(sys.argv[1])+'.pub')
	f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+ str(sys.argv[1])+".pub", "w")   # 'r' for reading and 'w' for writing
	f.write(str(n) + str(e))

	# compute e and d cos e is required for generating d
	d = compute_d(e, t)
	# print the private key
	print('Writing private key to file: '+ str(sys.argv[1])+'.prv')
	f = open("C:\\Users\\Singh\\OneDrive\\Desktop\\"+ str(sys.argv[1])+".prv", "w")   # 'r' for reading and 'w' for writing
	f.write(str(n) + str(d))

def main():
	print_keys()
	quit()


if __name__ == '__main__':
	main()