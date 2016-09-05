import string

# The given permutation tables
first_PCtable_String = "57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4"
second_PCtable_String = "14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32"
IPtableString = "58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7"
EBit_table = "32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1"
P_table = "16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25"

# The given S-boxes
S1 = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7], 
      [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8], 
      [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0], 
      [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]]
S2 = [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10], 
      [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5], 
      [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15], 
      [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]]
S3 = [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8], 
      [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1], 
      [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7], 
      [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]]
S4 = [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15], 
      [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9], 
      [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4], 
      [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
S5 = [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9], 
      [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6], 
      [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14], 
      [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]]
S6 = [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11], 
      [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8], 
      [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6], 
      [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]]
S7 = [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1], 
      [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6], 
      [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2], 
      [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]]
S8 = [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7], 
      [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2], 
      [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8], 
      [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]


# This function applies a permutation table to a binary string when the permutation table is given as a comma-separated string
def apply_permutation(binary, permutation_table):
  table_array = permutation_table.split(",")
  table_length = len(table_array)
  result = ""
  
  for i in range(0, table_length):
    result += binary[int(table_array[i]) - 1]

  return result


# This function shifts a given binary string to the left by one
def left_shift(string):
  return string[1: len(string)] + string[0]


# This function implements an XOR operation on two binary input strings.
def xor(binary1, binary2):
  if(len(binary1) != len(binary2)):
    print "ERROR: XOR inputs not the same length (length = " + str(len(binary1)) + ", length = " + str(len(binary2)) + ")"
    exit()

  result = ""
  length = len(binary1)

  for i in range(0, length):
    if(binary1[i] == binary2[i]):
      result += "0"
    else:
      result += "1"

  return result


# This function turns a binary value to a decimal
def binary_to_dec(binary):
  if len(binary) == 4:
    return 8*int(binary[0]) + 4*int(binary[1]) + 2*int(binary[2]) + 1*int(binary[3])
  elif len(binary) == 2:
    return 2*int(binary[0]) + 1*int(binary[1])
  else:
    print "ERROR: Faulty binary value in binary_to_dec(): " + binary


# This function turns a decimal value into a binary value
def dec_to_binary(decimal):
  get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n) # taken from stackexchange
  return get_bin(decimal, 4)


# This function implements an S-box
def sbox(block, sbox_type):
  i = binary_to_dec(block[0] + block[5])
  j = binary_to_dec(block[1:5])

  return dec_to_binary(int( sbox_type[i][j] ))


# The mangler function
def f(Rn, Kn):
  # expand R1 with the E Bit-selection table
  expandedRn = apply_permutation(Rn, EBit_table)
  print "     E(R0)        : " + expandedRn

  # xor the expanded result with K1
  xorResult = xor(expandedRn, Kn)
  print "     K1 XOR E(R0) : " + xorResult

  # split the binary string into eight parts
  B1 = xorResult[ 0 : 6 ]
  B2 = xorResult[ 6 : 12 ]
  B3 = xorResult[ 12 : 18 ]
  B4 = xorResult[ 18 : 24 ]
  B5 = xorResult[ 24 : 30 ]
  B6 = xorResult[ 30 : 36 ]
  B7 = xorResult[ 36 : 42 ]
  B8 = xorResult[ 42 : 48 ]

  print " "
  print "Segmented binary:"
  print "    B1:{0} B2:{1} B3:{2} B4:{3} B5:{4} B6:{5} B7:{6} B8:{7}".format(B1, B2, B3, B4, B5, B6, B7, B8)

  # apply the respective S-boxes to each binary part
  SB1 = sbox(B1, S1)
  SB2 = sbox(B2 ,S2)
  SB3 = sbox(B3 ,S3)
  SB4 = sbox(B4 ,S4)
  SB5 = sbox(B5 ,S5)
  SB6 = sbox(B6 ,S6)
  SB7 = sbox(B7 ,S7)
  SB8 = sbox(B8 ,S8)

  print " "
  print "S-box results:"
  print "    S1: {0}  S2: {1}  S3: {2}  S4: {3}  S5: {4}  S6: {5}  S7: {6}  S8: {7}  ".format(SB1, SB2, SB3, SB4, SB5, SB6, SB7, SB8)

  P = apply_permutation( (SB1 + SB2 + SB3 + SB4 + SB5 + SB6 + SB7 + SB8), P_table)

  return P


##########################
#      Main method       #
##########################


# Notes:
# request user input, and use an external library to turn the message into binary

# need to supply example message and key
message = ""
key =     ""

print " "
print "message : " + message
print "key     : " + key
print "-" * 86

# Apply permutation to K+
K_plus = apply_permutation(key, first_PCtable_String)
print "     K+ : " + K_plus

C0 = K_plus[ 0 : (len(K_plus)/2) ]		          # first half of K_plus
D0 = K_plus[ (len(K_plus)/2) : len(K_plus) ]    # second half of K_plus
print "     C0 : " + C0
print "     D0 : " + " "*len(C0) + D0
print "-" * 86

# Shift C1 and D1, combine them, and permute them to get K1
C1 = left_shift(C0)
D1 = left_shift(D0)
C1D1 = str(C1 + D1)
K1 = apply_permutation(C1D1, second_PCtable_String)
print "     C1 : " + C1
print "     D1 : " + " "*len(C1) + D1
print "   C1D1 : " + C1D1
print "     K1 : " + K1
print "-" * 86

# Apply the initial permutation to the message
IP = apply_permutation(message, IPtableString)

L0 = IP[ 0 : (len(IP)/2) ]		     # first half of IP
R0 = IP[ (len(IP)/2) : len(IP) ] 	 # second half of IP
print "     IP : " + IP
print "     L0 : " + L0
print "     R0 : " + " "*len(L0) + R0
print "-" * 86


L1 = R0
f_result = f(R0, K1)
R1 = xor(L0, f_result)
print " "
print "Mangler function output: " + f_result
print "-" * 86
print " "
print "----- Result of R1 (one round of DES): " + R1
