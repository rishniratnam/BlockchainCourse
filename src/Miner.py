import SocketUtils

wallet_list = ['10.0.0.3']
def minerServer(my_ip, wallet_list):
    server = SocketUtils.newServerConnection()
    transactions = SocketUtils.recvObj(server)
    # Collect into block
    # Find the nonce
    # Send that block to each in wallet list
    return False

