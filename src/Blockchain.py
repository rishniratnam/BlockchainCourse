from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
digest.update(b"abc")
digest.update(b"123")
digest.finalize()

class someClass:
    num = 123
    def __init__(self,mystring):
        self.string = mystring
    def __repr__(self):
        return self.string + str(self.num)



class CBlock:
    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock == None:
            self.previousHash = None
        else:
            self.previousHash = previousBlock.computeHash()
        self.data = data
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data),'utf-8'))
        digest.update(bytes(str(self.previousHash),'utf-8'))
        return digest.finalize()
    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.computeHash() == self.previousHash


if __name__ == '__main__':
    root = CBlock('I am root', None)
    B1 = CBlock('I am a child.', root)
    B2 = CBlock('I am B1s brother', root)
    B3 = CBlock(1234,B1)
    B4 = CBlock(someClass('Hi there'), root)
    print(B4.data)
    print(B4.computeHash())


    for b in [B1, B2, B3, B4]:
        if b.previousBlock.computeHash() == b.previousHash:
            print("Success! Hash is Good")
        else:
            print("ERROR! Hash is no good.")