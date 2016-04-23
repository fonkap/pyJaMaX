import socket

from id_gen import UIDGenerator, ObjIDGenerator, VMIDGenerator
from msgs import *


if __name__ == "__main__":
    host = socket.gethostbyname("localhost")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 1190))

    #TODO set handshake timeout
    msg4 = create_protocol_msg()
    sock.send(msg4)
    msg6 = sock.recv(21)
    suggHostName, suggHostPort = read_suggested_hostname(msg6)
    print 'server suggested : ' + suggHostName + ':' + str(suggHostPort)

    localEpHost = sock.getsockname()[0]

    msg7 = create_local_hostname_msg(localEpHost)
    msg8 = create_lookup_msg()
    sock.send(msg7)
    sock.send(msg8)

    msg6 = sock.recv(1024)
    uid_10, rmiserver_10, objid_10 = read_rmi_server(msg6)

    #0x52 - Ping
    msg11 = binascii.unhexlify('52')
    sock.send(msg11)
    r12 = sock.recv(1)
    assert r12 == '\x53', "Pong"

    uid_gen = UIDGenerator()
    vmid_gen = VMIDGenerator(uid_gen)

    objid_dcg = ObjIDGenerator.create_well_known(2)
    vmid = vmid_gen.generate()

    msg13 = create_lease_msg(objid_dcg, objid_10, vmid)

    sock.send(msg13)
    r14 = sock.recv(1024)
    #TODO parse msg (Lease object)

    msg15 = create_dcg_ack_msg(uid_10)
    sock.send(msg15)

    msg16 = create_call_msg(objid_10, -1, 0xf0e074eaad0caea8, [None]) #RMIServerImpl_Stub.newClient
    sock.send(msg16)

    r18 = sock.recv(1024)
    uid_18, rmiserver_18, objid_18 = read_rmi_server(r18)

    msg19 = create_lease_msg(objid_dcg, objid_18, vmid)
    sock.send(msg19)
    r20 = sock.recv(1024)
    #TODO parse msg (Lease object)

    msg21 = create_dcg_ack_msg(uid_18)
    sock.send(msg21)
    msg22 = create_call_msg(objid_18, -1, 0xff0ebec77dc65363, []) #RMIConnectionImpl_Stub.getConnectionId() line: not available
    sock.send(msg22)
    r24 = sock.recv(1024)
    uid_24, connection_id = read_remote_object(r24)
    print 'connection_id: ' + connection_id

    msg25 = create_invoke_msg(objid_18, -1, 0x13e7d69417e5da20, 'FOO:name=HelloBean', 'sayHello', ['msg1'], ['java.lang.String'])
    sock.send(msg25)
    r26 = sock.recv(1024)

    sock.close()