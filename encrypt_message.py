from AES_Master import AES_methods
import numpy as np

key = "Thats my Kung Fu"
text = "Two One Nine Two"
myObj = AES_methods(key,text)
myObj.generate_roundKeys()
#for i in range(11):
#    print myObj.RoundKey[i]
number_of_rounds = myObj.getNumberOfRounds(myObj.key)
for round_no in range(number_of_rounds+1):
    if round_no == 0:
        current_state = myObj.addRoundKey(myObj.text_words,0)
    elif round_no > 0 and round_no <10:
        current_state = [myObj.byteSub(current_state[i]) for i in range(len(current_state))]
        current_state = np.array(current_state).T
        current_state = myObj.shiftRows(current_state)
        current_state = current_state.T
        current_state = myObj.mixColumns(current_state)
        current_state = myObj.addRoundKey(current_state, round_no)
    elif round_no == 10:
        current_state = [myObj.byteSub(current_state[i]) for i in range(len(current_state))]
        current_state = np.array(current_state).T
        current_state = myObj.shiftRows(current_state)
        current_state = current_state.T
        current_state = myObj.addRoundKey(current_state, round_no)

print "Encrypted Message"
print current_state
