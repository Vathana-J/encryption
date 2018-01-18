# encryption
# AES - Advanced Encryption Standard

My final year project was done with AES. Though I did it using C-programming at that time, I just coded it using Python now to fill in the GIT with some nice programming :)

#AES Algorithm

AES is an iterated symmetric block cipher, which means that:

• AES works by repeating the same defined steps multiple times.
• AES is a secret key encryption algorithm.
• AES operates on a fixed number of bytes
  
AES as well as most encryption algorithms is reversible. This means that almost the same steps are performed to
complete both encryption and decryption in reverse order. The AES algorithm operates on bytes, which makes it simpler to
implement and explain.

This key is expanded into individual sub keys, a sub keys for each operation round. This process is called KEY
EXPANSION, which is described at the end of this document.

AES is an iterated block cipher. All that means is that the same operations are performed many times
on a fixed number of bytes. These operations can easily be broken down to the following functions:
ADD ROUND KEY
BYTE SUB
SHIFT ROW
MIX COLUMN

An iteration of the above steps is called a round. The amount of rounds of the algorithm depends on the key size.

The only exception being that in the last round the Mix Column step is not performed, to make the algorithm reversible
during decryption.
