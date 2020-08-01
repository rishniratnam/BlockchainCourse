import SocketUtils
import Transaction
import TxBlock
wallets = ['localhost']
tx_list = []
def minerServer(my_ip, wallet_list):
    server = SocketUtils.newServerConnection(my_ip)
    for i in range(10):
        newTx = SocketUtils.recvObj(server)
        if isinstance(newTx, Transaction.Tx):
            tx_list.append(newTx)
            print('Recd tx')
        if len(tx_list) >= 2:
                break
    newBlock = TxBlock.TxBlock(None)
    newBlock.addTx(tx_list[0])
    newBlock.addTx(tx_list[1])
    for i in range(10):
        print('Finding Nonce..."')
        newBlock.find_nonce()
        if newBlock.good_nonce():
            print('Good Nonce found')
            break
    if not newBlock.good_nonce():
        print("Error. Couldn't find nonce")
        return False
    for ip_addr in wallet_list:
        SocketUtils.sendObj(ip_addr, newBlock, 5006)
    return False
minerServer('localhost', wallets)
