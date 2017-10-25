import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class csn_aes_crypto(object):

    def __init__(self, key):
        self.bs = 32                                        #block size
        self.key = hashlib.sha256(key.encode()).digest()    #AES key, SHA256'd -> digest.

    def encrypt(self, raw):
        raw = self._pad(raw)                                #take input and pad to correct length for encryption
        iv = Random.new().read(AES.block_size)              #generate IV based on block size
        cipher = AES.new(self.key, AES.MODE_CBC, iv)        #setup encryptor
        return base64.b64encode(iv + cipher.encrypt(raw.encode("UTF-8")))   #return the base64 value of the encrypted conent.

    def decrypt(self, enc):
        enc = base64.b64decode(enc)                                                 #base64 -> plain AES
        iv = enc[:AES.block_size]                                                   #get IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)                                #setup decryptor
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))    #return the unpadded version of the original text.

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)   #padding function.
        #return string + block_size - length string % block_size   *  block_size - length string % block_size

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]                       #unpad data
        #removes the trailing 0x00 bytes from the package.
