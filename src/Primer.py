def myFunc(int_in):
    return int_in/5
print ("Hello!")
class myClass:
    oneval = 17
    def div(self, int_in):
        return int_in/self.oneval
    def __init__(self, inval):
        self.oneval = inval
class newClass (myClass):
    name = 'Levi'
    def __repr__(self):
        name = "Jeff"
        return (self.name + ": oneval is equal to " +
                str(self.oneval))
C = myClass(4)
B = myClass(10)
C.oneval = 4
print(C.oneval)
print(C.div(34))
print(B.div(10))
N = newClass(12)
print (N.name)
print(N.div(36))
print(N)

if __name__ == '__main__':
    print(myFunc(21))
else:
    print("primer imported, not invoked")