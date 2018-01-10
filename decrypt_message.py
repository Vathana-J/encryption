from AES_Master import AES_methods
import numpy as np
import binascii
#encrypted_message = [raw_input()] #Not working.. Need to research
encrypted_message = ['0xda', '0x1f', '0x9c', '0x88', '0x6c', '0xd4', '0xad', '0x30', '0x61', '0x3e', '0x3a', '0x22', '0xb6', '0xd6', '0x4b', '0xaa']
encrypted_message_words = [[encrypted_message[n], encrypted_message[n + 1], encrypted_message[n + 2], encrypted_message[n + 3]]
                   for n in range(0, 16, 4)]
key = raw_input("Enter the 16-bit Key that would be used to encrypt the message: ")
while len(key) != 16:
    print ("Key Length is not 16bits")
    key = raw_input("Enter the 16-bit Key that would be used to decrypt the message: ")
#key = 'Thats my Kung Fu'
myObj = AES_methods(key)
myObj.generate_roundKeys()
number_of_rounds = myObj.getNumberOfRounds(myObj.key)
for round_no in range(number_of_rounds,-1,-1):
    print round_no
    if round_no == 10:
        current_state = myObj.addRoundKey(encrypted_message_words,10)
    elif round_no > 0 and round_no < 10:
        current_state = np.array(current_state).T
        current_state = myObj.shiftRows_decrypt(current_state)
        current_state = current_state.T
        current_state = [myObj.byteSubInverse(current_state[i]) for i in range(len(current_state))]
        current_state = myObj.addRoundKey(current_state, round_no)
        current_state = myObj.inverseMixColumns(current_state)
    elif round_no == 0:
        current_state = np.array(current_state).T
        current_state = myObj.shiftRows_decrypt(current_state)
        current_state = current_state.T
        current_state = [myObj.byteSubInverse(current_state[i]) for i in range(len(current_state))]
        current_state = myObj.addRoundKey(current_state, round_no)

#print "Final State"
#print current_state
print "Decrypted Message"
print ''.join([unichr(int(x,16)) for x in np.array(current_state).flatten()])
