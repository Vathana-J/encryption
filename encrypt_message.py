from AES_Master import AES_methods
import numpy as np
import binascii

text = raw_input("Enter the message to encrypt: ")
if len(text) < 16:
    text = '{:16}'.format(text)
print text
text_ascii = [ord(x) for x in list(text)]
text_hex = [hex(n) for n in text_ascii]
text_words = [[text_hex[n], text_hex[n + 1], text_hex[n + 2], text_hex[n + 3]]
                   for n in range(0, len(text_hex), 4)]

key = raw_input("Enter the 16-bit Key that would be used to encrypt the message: ")
#key = 'Thats my Kung Fu'


while len(key) != 16:
    print ("Key Length is not 16bits")
    key = raw_input("Enter the 16-bit Key that would be used to encrypt the message: ")
myObj = AES_methods(key)
myObj.generate_roundKeys()
#for i in range(11):
#    print myObj.RoundKey[i]
number_of_rounds = myObj.getNumberOfRounds(myObj.key)
for round_no in range(number_of_rounds+1):
    if round_no == 0:
        current_state = myObj.addRoundKey(text_words,0)
    elif round_no > 0 and round_no <10:
        current_state = [myObj.byteSub(current_state[i]) for i in range(len(current_state))]
        current_state = np.array(current_state).T
        current_state = myObj.shiftRows_encrypt(current_state)
        current_state = current_state.T
        current_state = myObj.mixColumns(current_state)
        current_state = myObj.addRoundKey(current_state, round_no)
    elif round_no == 10:
        current_state = [myObj.byteSub(current_state[i]) for i in range(len(current_state))]
        current_state = np.array(current_state).T
        current_state = myObj.shiftRows_encrypt(current_state)
        current_state = current_state.T
        current_state = myObj.addRoundKey(current_state, round_no)
print "Final State"
print list(current_state)
print [(int(x,16)) for x in current_state.flatten()]
print "Encrypted Message"
print ''.join([unichr(int(x,16)) for x in current_state.flatten()])
flat = current_state.flatten()
print flat
print "Encrypted message as Hex array"
print ([hex(int(x,16)) for x in flat])
test = [x[2:] if len(x) > 3 else '0'+x[2] for x in flat]
test = ''.join(test)
print test