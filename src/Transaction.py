from src import Signatures


class Tx:
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        message = self.__gather()
        self.sigs.append(Signatures.sign(message, private))

    def is_valid(self):
        total_in = 0
        total_out = 0

        message = self.__gather()

        for addr, amount in self.inputs:
            found = False
            for s in self.sigs:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False
            if amount < 0:
                return False

            total_in += amount

        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if Signatures.verify(message, s, addr):
                    found = True
            if not found:
                return False

        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out += amount

        if total_out > total_in:
            return False

        return True

    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data

    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr += str(amt) + " from " + str(addr) + "\n"

        reprstr += "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr += str(amt) + " from " + str(addr) + "\n"

        reprstr += "REQD:\n"
        for req in self.reqd:
            reprstr += str(req) + "\n"

        reprstr += "SIGS:\n"
        for sig in self.sigs:
            reprstr += str(sig) + "\n"

        reprstr += "END\n"

        return reprstr


if __name__ == "__main__":
    pr1, pu1 = Signatures.generate_keys()
    pr2, pu2 = Signatures.generate_keys()
    pr3, pu3 = Signatures.generate_keys()
    pr4, pu4 = Signatures.generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pu3,1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_reqd(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)


    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Success! Tx is valid")
        else:
            print('ERROR! Tx is invalid')

    # wrong signatures
    Tx4 = Tx()
    #print(Tx4.inputs)
    Tx4.add_input(pu1 , 1)
    #print(Tx4.inputs)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # escrow transaction not signed by arbiter
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_reqd(pu4)
    Tx5.sign(pr3)

    # two input addrs, signed by one
    Tx6 = Tx()
    Tx6.add_input(pu3, 1)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu4, 1.1)
    Tx6.sign(pr3)

    # Outputs exceed inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1, 1)
    Tx7.add_output(pu2, 2)
    Tx7.sign(pr4)

    # Negative amounts
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1,-1)
    Tx8.sign(pr2)

    # Modify Tx
    Tx9 = Tx()
    Tx9.add_input(pu1, 1)
    Tx9.add_output(pu2, 1)
    Tx9.sign(pr1)
    Tx9.outputs[0]= (pu3,1)

    for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx9]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print('Success! Bad Tx is invalid')
