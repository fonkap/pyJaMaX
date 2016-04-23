import binascii

from id_gen import build_obj_array, build_lease, UIDGenerator, ObjIDGenerator
from java_deser.des import *
from java_deser.ser import Serializer, get_bytes, serial_obj, serial_objid, serial_uid, write_string
from jawa.util.mutf8 import decode_modified_utf8


def read_suggested_hostname(msg):
    protocol_ack = b'\x4e'
    assert msg[0] == protocol_ack
    sugg_host_namel = struct.unpack('>h', msg[1:3])[0]
    sugg_host_name = decode_modified_utf8(msg[3:3 + sugg_host_namel])
    sugg_host_port = struct.unpack('>L', msg[3 + sugg_host_namel:3 + sugg_host_namel + 4])[0]
    return sugg_host_name, sugg_host_port


def read_remote_object(r):
    inp = StringIO.StringIO(r)
    b = inp.read(1);
    assert b == '\x51'
    magic = inp.read(2)
    assert magic == '\xAC\xED', h(magic)  # STREAM_MAGIC
    b = inp.read(2)
    assert p(b) == 5  # STREAM_VERSION
    b = inp.read(1);
    assert b == '\x77', "Block stream"
    b = inp.read(1);
    assert b == '\x0f', "Size"
    b = inp.read(1);
    assert b == '\x01', "Normal return"
    uid = parse_uid(inp)
    object = parse(inp)[0]
    return uid, object


def read_rmi_server(r):
    uid, rmiserver = read_remote_object(r)
    objid = rmiserver['data']['ref']['objId']
    return uid, rmiserver, objid


def create_protocol_msg():
    # TCPChannel line - 228
    magic = b'JRMI'
    version = 2
    stream_protocol = b'\x4b'
    msg = magic + struct.pack('>h', version) + stream_protocol
    return msg


def create_local_hostname_msg(local_ep_host):
    f = StringIO.StringIO()
    write_string(f, local_ep_host)
    f.write(struct.pack('>L', 0))  # port 0
    return f.getvalue()


def create_lookup_msg():
    oid = ObjIDGenerator.create_well_known(0)
    op = 2
    registry_impl_stub_interfacehash = 0x44154dc9d4e63bdf
    f = StringIO.StringIO()
    ser = Serializer(f)
    ser.write_bytes(get_bytes(serial_objid, oid))
    ser.write_int(op)
    ser.write_ulong(registry_impl_stub_interfacehash)
    ser.serial_obj('jmxrmi')

    # TODO set response timeout
    # outbound call: [endpoint:[domain:1190](remote),objID:[0:0:0, 0]] : sun.rmi.registry.RegistryImpl_Stub[0:0:0, 0]: java.rmi.Remote lookup(java.lang.String)
    # UnicastRef line - 351
    #             length                                          op       REgistrImpl_Stub.interfacehash jmxrmi
    # 50aced00057722 00000000000000000000000000000000000000000000 00000002 44154dc9d4e63bdf               74 0006 6a6d78726d69
    #   aced00057716 00000000000000000000000000000000000000000000
    msg8 = binascii.unhexlify('50aced0005') + f.getvalue()
    return msg8


def create_lease_msg(objid_dcg, objid, vmid):
    out = StringIO.StringIO()
    ser = Serializer(out, True)

    ser.write_bytes(get_bytes(serial_objid, objid_dcg))
    ser.write_int(1)  # opnum  - DGCImpl_Stub.dirty line: 75
    ser.write_ulong(0xf6b6898d8bf28643)  # DGCImpl_Stub.interfaceHash

    objid_array = build_obj_array([objid], -8713620060265225090)
    ser.serial_obj(objid_array)
    ser.write_ulong(0x8000000000000000)

    lease = build_lease(vmid, 600000)
    ser.serial_obj(lease)

    msg_lease = binascii.unhexlify('50aced0005') + out.getvalue()
    assert 451 == len(msg_lease), 'wrong length' + binascii.hexlify(msg_lease)
    return msg_lease


def create_dcg_ack_msg(uid):
    out = StringIO.StringIO()
    out.write('\x54')  # DGCAck
    serial_uid(out, uid)  # from r10
    msg = out.getvalue()
    return msg


def create_call_msg(obj_id, op_index, stub_hash, params):
    out = StringIO.StringIO()
    ser = Serializer(out, True)
    ser.write_bytes(get_bytes(serial_objid, obj_id))
    ser.write_int(op_index)
    ser.write_ulong(stub_hash)
    for param in params:
        ser.serial_obj(param)
    ser.flush_buffer()
    msg = binascii.unhexlify('50aced0005') + out.getvalue()
    return msg


def create_invoke_msg(obj_id, op_index, stub_hash, bean_name, method_name, params, param_types):
    out = StringIO.StringIO()
    ser = Serializer(out, True)
    ser.write_bytes(get_bytes(serial_objid, obj_id))
    ser.write_int(op_index)
    ser.write_ulong(stub_hash)

    objName = {'data': bean_name, '_cls': {'fields': [], '_uid': 1081892073854801359L, 'flags': '\x03', 'parent': None, '_name': 'javax.management.ObjectName'}, '_name': 'javax.management.ObjectName'}
    ser.serial_obj(objName)
    ser.serial_obj(method_name)

    out2 = StringIO.StringIO()
    obj2 = {'data': params, '_cls': {'fields': [], '_uid': -8012369246846506644, 'flags': '\x02', 'parent': None, '_name': '[Ljava.lang.Object;'}, '_name': '[Ljava.lang.Object;'}
    serial_obj(out2, obj2)
    marshalled_obj =  list(binascii.unhexlify('aced0005') + out2.getvalue())
    obj = {'objBytes': {'data': marshalled_obj, '_cls': {'fields': [], '_uid': -5984413125824719648, 'flags': '\x02', 'parent': None, '_name': '[B'}, '_name': '[B'}, 'locBytes': None, 'hash': -1489593241, '_cls': {'fields': [('hash', 'I', ''), ('locBytes', '[', u'[B'), ('objBytes', '[', u'[B')], '_uid': 8988374069173025854L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.MarshalledObject'}, '_name': 'java.rmi.MarshalledObject'}
    ser.serial_obj(obj)

    obj = {'data': param_types, '_cls': {'fields': [], '_uid': -5921575005990323385, 'flags': '\x02', 'parent': None, '_name': '[Ljava.lang.String;'}, '_name': '[Ljava.lang.String;'}
    ser.serial_obj(obj)
    ser.serial_obj(None)
    ser.flush_buffer()
    msg = binascii.unhexlify('50aced0005') + out.getvalue()
    return msg
