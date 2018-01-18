import numpy as np
from AES_CONSTANTS import constants
class AES_methods(object):
    num_of_roundkeys = 0 #variable to hold the number of rounds to be performed, based on the key length
    RoundKey = [] #To hold the Roundkeys generated for manipulation in each round

    def __init__(self, key):
        self.key = key
        key_ascii = [ord(x) for x in list(key)]
        key_hex = [hex(n) for n in key_ascii]
        self.key_word = [[key_hex[n], key_hex[n + 1], key_hex[n + 2], key_hex[n + 3]]
                         for n in range(0, len(key_hex), 4)]
        AES_methods.num_of_roundkeys = self.getNumberOfRounds(key)
        AES_methods.RoundKey.append(self.key_word) #First RoundKey is the Key itself


    def generate_roundKeys(self):
        # Assign the number of rounds, based on the Key length
        #cls.num_of_roundkeys = cls.getNumberOfRounds(cls.key)
        for roundkeys_num in range(self.num_of_roundkeys):

            rotated_word = self.rot_word_left(self.RoundKey[roundkeys_num][3])
            sub_word = self.byteSub(rotated_word)
            rcon_word = self.addRoundConstant(sub_word,roundkeys_num)

            self.RoundKey.append([])
            self.RoundKey[roundkeys_num+1].append([hex(x) for x in [int(x, 16) for x in rcon_word] ^ np.array(
                [int(x, 16) for x in self.RoundKey[roundkeys_num][0]])])
            self.RoundKey[roundkeys_num+1].append([hex (x) for x in np.array([int(x, 16) for x in self.RoundKey[roundkeys_num + 1][0]]) ^ np.array(
                [int(x, 16) for x in self.RoundKey[roundkeys_num][1]])])
            self.RoundKey[roundkeys_num+1].append([hex(x) for x in np.array([int(x, 16) for x in self.RoundKey[roundkeys_num + 1][1]]) ^ np.array(
                [int(x, 16) for x in self.RoundKey[roundkeys_num][2]])])
            self.RoundKey[roundkeys_num+1].append([hex(x) for x in np.array([int(x, 16) for x in self.RoundKey[roundkeys_num + 1][2]]) ^ np.array(
                [int(x, 16) for x in self.RoundKey[roundkeys_num][3]])])
            #print cls.RoundKey[roundkeys_num+1]


        return

    def getNumberOfRounds(self,Key):
    # The amount of rounds of the algorithm depends on the key size. In this function, we set the number of rounds
    # based on the key size.
        if len(Key) == 16: #if the key size is 16, then the number of rounds to be performed is 10
            return 10
        elif len(Key) == 24: #if the key size is 24, then the number of rounds to be performed is 12
            return 12
        elif len(Key) == 32: #if the key size is 32, then the number of rounds to be performed is 14
            return 14
        else:
            return "error"

    @staticmethod
    def rot_word_left(word):
        # This does a circular shift i.e. just moves each byte of the word one space over left
        new_word = [word[1],word[2],word[3],word[0]]
        return new_word

    @staticmethod
    def rot_word_right(word):
        # This does a circular shift i.e. just moves each byte of the word one space over right
        new_word = [word[3], word[0], word[1], word[2]]
        return new_word

    @staticmethod
    def byteSub(word):
        # Each value of the byte of the word is replaced with the corresponding SBOX value
        new_word=[]
        # Run iteration for each byte of the word i.e. 4 times (4 bytes)
        for i in range(4):
            # If the byte is a 2 digit hex like '0xfc', then extract the last 2 bits (1st bit to Row and 2nd bit to
            # column) to do the look-up in the sbox
            if len(word[i]) == 4:
                int_word = [int(word[i][2],16),int(word[i][3],16)]
                new_word.append(hex(constants.sbox[int_word[0]][int_word[1]]))
            # If the byte is a 1 digit hex like '0xc', then extract the last bit (and use 0 for Rows and last bit to
            # column) to do the look-up in the sbox
            elif len(word[i]) == 3:
                new_word.append(hex(constants.sbox[0][int(word[i][2],16)]))
        return new_word

    @staticmethod
    def byteSubInverse(word):
        # Each value of the byte of the word is replaced with the corresponding SBOX value
        new_word = []
        # Run iteration for each byte of the word i.e. 4 times (4 bytes)
        for i in range(4):
            # If the byte is a 2 digit hex like '0xfc', then extract the last 2 bits (1st bit to Row and 2nd bit to
            # column) to do the look-up in the sbox
            if len(word[i]) == 4:
                int_word = [int(word[i][2], 16), int(word[i][3], 16)]
                new_word.append(hex(constants.inv_sbox[int_word[0]][int_word[1]]))
            # If the byte is a 1 digit hex like '0xc', then extract the last bit (and use 0 for Rows and last bit to
            # column) to do the look-up in the sbox
            elif len(word[i]) == 3:
                new_word.append(hex(constants.inv_sbox[0][int(word[i][2], 16)]))
        return new_word

    @staticmethod
    def addRoundConstant(word,n):
        # XOR the corresponding RCon value to the 1st byte in each word
        # n is the value of the current number of the RoundKey that is being calculated
        adding_round_constant = hex(int(word[0], 16) ^ constants.Rcon[n])
        word [0] = adding_round_constant
        return word

    @classmethod
    def shiftRows_encrypt(self,state):
        # Arranges the state in a matrix and then performs a circular shift for each row. This is not a bit wise shift.
        # The circular shift just moves each byte one space over. A byte that was in the second position may end up in
        # the first position after the shift. The circular part of it specifies that the byte in the last position
        # shifted one space will end up in the second position in the same row.
        for i in range(1,len(state)):
            for n in range(i):  # keep rotating based on the row number, which would meet the requirement
                state[i]=self.rot_word_left(state[i])
        return state

    @classmethod
    def shiftRows_decrypt(self, state):
        # Arranges the state in a matrix and then performs a circular shift for each row to right. This is not a bit wise shift.
        # The circular shift just moves each byte one space over to right. A byte that was in the second position may end up in
        # the third position after the shift. The circular part of it specifies that the byte in the last position
        # shifted one space will end up in the first position in the same row.
        for i in range(1, len(state)):
            for n in range(i):  # keep rotating based on the row number, which would meet the requirement
                state[i] = self.rot_word_right(state[i])
        return state

    @classmethod
    def addRoundKey(self,state,roundKey_num):
        # Each of the 16 bytes of the state is XORed against each of the 16 bytes of a portion of the expanded key for
        # the current round.
        for i in range(len(state)):
            state[i] = [hex(n) for n in np.array([int(a,16) for a in state[i]])^np.array([int(a,16) for a in self.RoundKey[roundKey_num][i]])]
        return state

    @staticmethod
    def mixColumns(state):
        # Done using Rijndael implementations to use pre-calculated lookup tables to perform the byte multiplication by 2, 3
        new_state = []
        matrix = constants.MixColumns
        for i in range(4):
            current_row = []
            for j in range(4):
                r = [0,0,0,0]
                for k in range(4):
                    # If the hex string is of length, then use '0' for the row and the last bit for the column look-up
                    if matrix[j][k] == 0x02: r[k] = constants.table_2[int(state[i][k][2],16) if len(state[i][k]) == 4 else
                    int(state[i][k][0],16)][int(state[i][k][3],16) if len(state[i][k]) == 4 else int(state[i][k][2],16)]
                    if matrix[j][k] == 0x03: r[k] = constants.table_3[int(state[i][k][2],16) if len(state[i][k]) == 4 else
                    int(state[i][k][0],16)][int(state[i][k][3],16) if len(state[i][k]) == 4 else int(state[i][k][2],16)]
                    if matrix[j][k] == 0x01: r[k] = int(state[i][k],16)
                current_row.append(r[0]^r[1]^r[2]^r[3]) # the multplication result of each row to column is then XORed
            current_row = [hex(x) for x in current_row]
            new_state.append(current_row)
        return new_state

    @staticmethod
    def inverseMixColumns(state):
        # Done using Rijndael implementations to use pre-calculated lookup tables to perform the byte multiplication by 2, 3
        new_state = []
        matrix = constants.InverseMixColumns
        for i in range(4):
            current_row = []
            for j in range(4):
                r = [0, 0, 0, 0]
                for k in range(4):
                    # If the hex string is of length, then use '0' for the row and the last bit for the column look-up
                    if matrix[j][k] == 0x09: r[k] = \
                    constants.table_9[int(state[i][k][2], 16) if len(state[i][k]) == 4 else
                    int(state[i][k][0], 16)][
                        int(state[i][k][3], 16) if len(state[i][k]) == 4 else int(state[i][k][2], 16)]
                    if matrix[j][k] == 0x11: r[k] = \
                    constants.table_11[int(state[i][k][2], 16) if len(state[i][k]) == 4 else
                    int(state[i][k][0], 16)][
                        int(state[i][k][3], 16) if len(state[i][k]) == 4 else int(state[i][k][2], 16)]
                    if matrix[j][k] == 0x13: r[k] = \
                    constants.table_13[int(state[i][k][2], 16) if len(state[i][k]) == 4 else
                    int(state[i][k][0], 16)][
                        int(state[i][k][3], 16) if len(state[i][k]) == 4 else int(state[i][k][2], 16)]
                    if matrix[j][k] == 0x14: r[k] = \
                    constants.table_14[int(state[i][k][2], 16) if len(state[i][k]) == 4 else
                    int(state[i][k][0], 16)][
                        int(state[i][k][3], 16) if len(state[i][k]) == 4 else int(state[i][k][2], 16)]
                current_row.append(r[0] ^ r[1] ^ r[2] ^ r[3])  # the multplication result of each row to column is then XORed
            current_row = [hex(x) for x in current_row]
            new_state.append(current_row)
        return new_state


