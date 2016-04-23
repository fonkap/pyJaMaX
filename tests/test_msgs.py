from unittest import TestCase

from msgs import *


import StringIO
import json
from unittest import TestCase

import binascii

from des import parse_uid, h, parse, Deserializer
from jmx import read_rmi_server
from ser import Serializer, get_bytes, serial_objid, serial_obj


class TestMsgs(TestCase):
    def test_r18(self):
        input = binascii.unhexlify('51aced0005770f01b4090e33000001533cd4a8d28039737200326a617661782e6d616e6167656d656e742e72656d6f74652e726d692e524d49436f6e6e656374696f6e496d706c5f537475620000000000000002020000707872001a6a6176612e726d692e7365727665722e52656d6f746553747562e9fedcc98be1651a020000707872001c6a6176612e726d692e7365727665722e52656d6f74654f626a656374d361b4910c61331e0300007078707738000a556e6963617374526566000f666f6e6b2e6c696e6b70632e6e6574000004a6fba308c523713db4b4090e33000001533cd4a8d280380178')
        uid_18, rmiserver_18, objid_18 = read_rmi_server(input)
        a = 1

    def test_r2(self):
        input = StringIO.StringIO(binascii.unhexlify('51ACED0005770F01B4090E33000001533CD4A8D280367372002E6A617661782E6D616E6167656D656E742E72656D6F74652E726D692E524D49536572766572496D706C5F537475620000000000000002020000707872001A6A6176612E726D692E7365727665722E52656D6F746553747562E9FEDCC98BE1651A020000707872001C6A6176612E726D692E7365727665722E52656D6F74654F626A656374D361B4910C61331E0300007078707738000A556E6963617374526566000F74657374646F6D61696E312E6E6574000004A611B42F2D498A4BA5B4090E33000001533CD4A8D280010178'))
        b = input.read(1);
        assert b == '\x51'
        magic = input.read(2)
        assert magic == '\xAC\xED', h(magic)  # STREAM_MAGIC
        assert p(input.read(2)) == 5  # STREAM_VERSION
        b = input.read(1);
        assert b == '\x77', "Block stream"
        b = input.read(1);
        assert b == '\x0f', "Size"
        b = input.read(1);
        assert b == '\x01', "Normal return"
        uid = parse_uid(input)
        out = StringIO.StringIO()
        json.dump(uid, out)
        expected = '{"time": 1457014483154, "count": -32714, "unique": -1274474957, "_cls": {"fields": [["count", "S", ""], ["time", "J", ""], ["unique", "I", ""]], "_uid": 1086053664494604050, "flags": "\u0002", "parent": null, "_name": "java.rmi.server.UID"}, "_name": "java.rmi.server.UID"}'
        assert expected == out.getvalue(), out.getvalue()
        rmiserver = parse(input)
        out = StringIO.StringIO()
        json.dump(rmiserver, out)
        expected = '[{"data": {"ref": {"objId": {"objNum": 1275696466006526885, "space": {"time": 1457014483154, "count": -32767, "unique": -1274474957, "_cls": {"fields": [["count", "S", ""], ["time", "J", ""], ["unique", "I", ""]], "_uid": 1086053664494604050, "flags": "\u0002", "parent": null, "_name": "java.rmi.server.UID"}, "_name": "java.rmi.server.UID"}, "_cls": {"fields": [["objNum", "J", ""], ["space", "L", "Ljava/rmi/server/UID;"]], "_uid": -6386392263968365220, "flags": "\u0002", "parent": null, "_name": "java.rmi.server.ObjID"}, "_name": "java.rmi.server.ObjID"}, "endpoint": {"port": 1190, "host": "testdomain1.net", "_cls": {"fields": [["host", "L", "String;"], ["port", "I", ""]], "flags": "\u0002", "parent": null, "_name": "TCPEndpoint"}, "_name": "TCPEndpoint"}, "_cls": {"fields": [["endpoint", "L", "TCPEndpoint"], ["objId", "L", "ObjID"]], "flags": "\u0002", "parent": null, "_name": "UnicastRef"}, "_name": "UnicastRef"}, "_cls": {"fields": [["ref", "L", "UnicastRef"]], "flags": "\u0002", "parent": null, "_name": "RemoteObject"}, "_name": "RemoteObject"}, "_cls": {"fields": [], "_uid": 2, "flags": "\u0002", "parent": {"fields": [], "_uid": -1585587260594494182, "flags": "\u0002", "parent": {"fields": [], "_uid": -3215090123894869218, "flags": "\u0003", "parent": null, "_name": "java.rmi.server.RemoteObject"}, "_name": "java.rmi.server.RemoteStub"}, "_name": "javax.management.remote.rmi.RMIServerImpl_Stub"}, "_name": "javax.management.remote.rmi.RMIServerImpl_Stub"}]'
        assert expected == out.getvalue(), out.getvalue()


    def test_des_obj2(self):
        expected = '{"data": [{"objNum": 1275696466006526885, "space": {"count": -32767, "unique": -1274474957, "time": 1457014483154, "_cls": {"fields": [["count", "S", ""], ["time", "J", ""], ["unique", "I", ""]], "_uid": 1086053664494604050, "flags": "\u0002", "parent": null, "_name": "java.rmi.server.UID"}, "_name": "java.rmi.server.UID"}, "_cls": {"fields": [["objNum", "J", ""], ["space", "L", "Ljava/rmi/server/UID;"]], "_uid": -6386392263968365220, "flags": "\u0002", "parent": null, "_name": "java.rmi.server.ObjID"}, "_name": "java.rmi.server.ObjID"}], "_cls": {"fields": [], "_uid": -8713620060265225090, "flags": "\u0002", "parent": null, "_name": "[Ljava.rmi.server.ObjID;"}, "_name": "[Ljava.rmi.server.ObjID;"}'
        str = '757200185b4c6a6176612e726d692e7365727665722e4f626a49443b871300b8d02c647e02000070787000000001737200156a6176612e726d692e7365727665722e4f626a4944a75efa128ddce55c0200024a00066f626a4e756d4c000573706163657400154c6a6176612f726d692f7365727665722f5549443b70787011b42f2d498a4ba5737200136a6176612e726d692e7365727665722e5549440f12700dbf364f12020003530005636f756e744a000474696d65490006756e697175657078708001000001533cd4a8d2b4090e3377088000000000000000737200126a6176612e726d692e6467632e4c65617365b0b5e2660c4adc340200024a000576616c75654c0004766d69647400134c6a6176612f726d692f6467632f564d49443b70787000000000000927c0737200116a6176612e726d692e6467632e564d4944f8865bafa4a56db60200025b0004616464727400025b424c000375696471007e0003707870757200025b42acf317f8060854e0020000707870000000086b6b6b6b6b6b6b6b7371007e00058001000001533ce1d6cf0e99868b'
        input = StringIO.StringIO(binascii.unhexlify(str))
        out = StringIO.StringIO()
        des = Deserializer(input)
        par = des.parse_obj()
        json.dump(par, out)
        assert expected == out.getvalue(), out.getvalue()
        seq = des.read_long()
        assert -0x8000000000000000 == seq, ("%08x" % seq)
        par = des.parse_obj()
        out = StringIO.StringIO()
        json.dump(par, out)
        expected = '{"vmid": {"uid": {"count": -32767, "unique": 244942475, "time": 1457015346895, "_cls": {"fields": [["count", "S", ""], ["time", "J", ""], ["unique", "I", ""]], "_uid": 1086053664494604050, "flags": "\u0002", "parent": null, "_name": "java.rmi.server.UID"}, "_name": "java.rmi.server.UID"}, "addr": {"data": ["k", "k", "k", "k", "k", "k", "k", "k"], "_cls": {"fields": [], "_uid": -5984413125824719648, "flags": "\u0002", "parent": null, "_name": "[B"}, "_name": "[B"}, "_cls": {"fields": [["addr", "[", "[B"], ["uid", "L", "Ljava/rmi/server/UID;"]], "_uid": -538642295484486218, "flags": "\u0002", "parent": null, "_name": "java.rmi.dgc.VMID"}, "_name": "java.rmi.dgc.VMID"}, "_cls": {"fields": [["value", "J", ""], ["vmid", "L", "Ljava/rmi/dgc/VMID;"]], "_uid": -5713411624328831948, "flags": "\u0002", "parent": null, "_name": "java.rmi.dgc.Lease"}, "value": 600000, "_name": "java.rmi.dgc.Lease"}'
        assert expected == out.getvalue(), out.getvalue()

    def test_msg25(self):
        expected = {'data': u'FOO:name=HelloBean', '_cls': {'fields': [], '_uid': 1081892073854801359L, 'flags': '\x03', 'parent': None, '_name': 'javax.management.ObjectName'}, '_name': 'javax.management.ObjectName'}
        string = '7372001b6a617661782e6d616e6167656d656e742e4f626a6563744e616d650f03a71beb6d15cf030000707870740012464f4f3a6e616d653d48656c6c6f4265616e7874000873617948656c6c6f737200196a6176612e726d692e4d61727368616c6c65644f626a6563747cbd1e97ed63fc3e020003490004686173685b00086c6f6342797465737400025b425b00086f626a427974657371007e0005707870d8c9639970757200025b42acf317f8060854e002000070787000000033aced0005757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c0200007870000000017400046d736731757200135b4c6a6176612e6c616e672e537472696e673badd256e7e91d7b47020000707870000000017400106a6176612e6c616e672e537472696e6770'
        input = StringIO.StringIO(binascii.unhexlify(string))
        des = Deserializer(input)
        par = des.parse_obj()
        assert expected == par, par

        par = des.parse_obj()
        expected = 'sayHello'
        assert expected == par, par

        par = des.parse_obj()
        expected = {'objBytes': {'data': ['\xac', '\xed', '\x00', '\x05', 'u', 'r', '\x00', '\x13', '[', 'L', 'j', 'a', 'v', 'a', '.', 'l', 'a', 'n', 'g', '.', 'O', 'b', 'j', 'e', 'c', 't', ';', '\x90', '\xce', 'X', '\x9f', '\x10', 's', ')', 'l', '\x02', '\x00', '\x00', 'x', 'p', '\x00', '\x00', '\x00', '\x01', 't', '\x00', '\x04', 'm', 's', 'g', '1'], '_cls': {'fields': [], '_uid': -5984413125824719648L, 'flags': '\x02', 'parent': None, '_name': '[B'}, '_name': '[B'}, 'locBytes': None, 'hash': -657890407, '_cls': {'fields': [('hash', 'I', ''), ('locBytes', '[', u'[B'), ('objBytes', '[', u'[B')], '_uid': 8988374069173025854L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.MarshalledObject'}, '_name': 'java.rmi.MarshalledObject'}
        assert expected == par, par
        i2 = StringIO.StringIO(''.join(par['objBytes']['data']))
        head = i2.read(4)
        assert binascii.unhexlify('aced0005') == head, head
        par = parse(i2)
        expected = [{'data': [u'msg1'], '_cls': {'fields': [], '_uid': -8012369246846506644L, 'flags': '\x02', 'parent': None, '_name': '[Ljava.lang.Object;'}, '_name': '[Ljava.lang.Object;'}]
        assert expected == par, par

        par = des.parse_obj()
        expected = {'data': [u'java.lang.String'], '_cls': {'fields': [], '_uid': -5921575005990323385L, 'flags': '\x02', 'parent': None, '_name': '[Ljava.lang.String;'}, '_name': '[Ljava.lang.String;'}
        assert expected == par, par

        par = des.parse_obj()
        expected = None
        assert expected == par, par

    def test_ser_msg13(self):
        out = StringIO.StringIO()
        ser = Serializer(out, True)
        obj = {'_name': 'java.rmi.server.ObjID', 'space': {'count': 0, '_name': 'java.rmi.server.UID', 'unique': 0, '_cls': {'fields': [['count', 'S', ''], ['time', 'J', ''], ['unique', 'I', '']], '_uid': 1086053664494604050L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.UID'}, 'time': 0}, '_cls': {'fields': [['objNum', 'J', ''], ['space', 'L', 'Ljava/rmi/server/UID;']], '_uid': 12060351809741186396L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.ObjID'}, 'objNum': 2}
        ser.write_bytes(get_bytes(serial_objid, obj))
        ser.write_int(1)
        ser.write_ulong(0xf6b6898d8bf28643)
        ser.flush_buffer()
        result = binascii.hexlify(out.getvalue())
        expected = '77220000000000000002000000000000000000000000000000000001f6b6898d8bf28643'
        assert expected == result, result

        obj = {'data': [{'objNum': 1275696466006526885L, 'space': {'count': -32767, 'unique': -1274474957, 'time': 1457014483154L, '_cls': {'fields': [('count', 'S', ''), ('time', 'J', ''), ('unique', 'I', '')], '_uid': 1086053664494604050L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.UID'}, '_name': 'java.rmi.server.UID'}, '_cls': {'fields': [('objNum', 'J', ''), ('space', 'L', u'Ljava/rmi/server/UID;')], '_uid': -6386392263968365220L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.ObjID'}, '_name': 'java.rmi.server.ObjID'}], '_cls': {'fields': [], '_uid': -8713620060265225090L, 'flags': '\x02', 'parent': None, '_name': '[Ljava.rmi.server.ObjID;'}, '_name': '[Ljava.rmi.server.ObjID;'}
        expected += '757200185b4c6a6176612e726d692e7365727665722e4f626a49443b871300b8d02c647e02000070787000000001737200156a6176612e726d692e7365727665722e4f626a4944a75efa128ddce55c0200024a00066f626a4e756d4c000573706163657400154c6a6176612f726d692f7365727665722f5549443b70787011b42f2d498a4ba5737200136a6176612e726d692e7365727665722e5549440f12700dbf364f12020003530005636f756e744a000474696d65490006756e697175657078708001000001533cd4a8d2b4090e33'

        ser.serial_obj(obj)
        result = binascii.hexlify(out.getvalue())
        assert expected == result, result

        expected += '77088000000000000000'
        ser.write_ulong(0x8000000000000000)
        ser.flush_buffer()
        result = binascii.hexlify(out.getvalue())
        assert expected == result, result

        expected += '737200126a6176612e726d692e6467632e4c65617365b0b5e2660c4adc340200024a000576616c75654c0004766d69647400134c6a6176612f726d692f6467632f564d49443b70787000000000000927c0737200116a6176612e726d692e6467632e564d4944f8865bafa4a56db60200025b0004616464727400025b424c000375696471007e0003707870757200025b42acf317f8060854e0020000707870000000086b6b6b6b6b6b6b6b7371007e00058001000001533ce1d6cf0e99868b'
        obj = {'vmid': {'_name': 'java.rmi.dgc.VMID', '_cls': {'fields': [['addr', '[', '[B'], ['uid', 'L', 'Ljava/rmi/server/UID;']], '_uid': -538642295484486218, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.dgc.VMID'}, 'uid': {'count': -32767, '_name': 'java.rmi.server.UID', 'unique': 244942475, '_cls': {'fields': [('count', 'S', ''), ('time', 'J', ''), ('unique', 'I', '')], '_uid': 1086053664494604050L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.UID'}, 'time': 1457015346895L}, 'addr': {'data': ['k', 'k', 'k', 'k', 'k', 'k', 'k', 'k'], '_cls': {'fields': [], '_uid': -5984413125824719648L, 'flags': '\x02', 'parent': None, '_name': '[B'}, '_name': '[B'}}, '_cls': {'fields': [['value', 'J', ''], ['vmid', 'L', 'Ljava/rmi/dgc/VMID;']], '_uid': -5713411624328831948, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.dgc.Lease'}, 'value': 600000, '_name': 'java.rmi.dgc.Lease'}

        ser.serial_obj(obj)
        result = binascii.hexlify(out.getvalue())
        assert expected == result, result


    def test_ser_msg25(self):
        #expected = '7372001b6a617661782e6d616e6167656d656e742e4f626a6563744e616d650f03a71beb6d15cf030000707870740012464f4f3a6e616d653d48656c6c6f4265616e7874000873617948656c6c6f737200196a6176612e726d692e4d61727368616c6c65644f626a6563747cbd1e97ed63fc3e020003490004686173685b00086c6f6342797465737400025b425b00086f626a427974657371007e0005707870d8c9639970757200025b42acf317f8060854e002000070787000000033aced0005757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c0200007870000000017400046d736731757200135b4c6a6176612e6c616e672e537472696e673badd256e7e91d7b47020000707870000000017400106a6176612e6c616e672e537472696e6770'
        expected = '7372001b6a617661782e6d616e6167656d656e742e4f626a6563744e616d650f03a71beb6d15cf030000707870740012464f4f3a6e616d653d48656c6c6f4265616e78'
        obj = {'data': 'FOO:name=HelloBean', '_cls': {'fields': [], '_uid': 1081892073854801359L, 'flags': '\x03', 'parent': None, '_name': 'javax.management.ObjectName'}, '_name': 'javax.management.ObjectName'}

        out = StringIO.StringIO()
        ser = Serializer(out, True)
        ser.serial_obj(obj)

        result = binascii.hexlify(out.getvalue())
        assert expected == result, result

        expected += '74000873617948656c6c6f'
        obj = 'sayHello'
        ser.serial_obj(obj)
        result = binascii.hexlify(out.getvalue())
        assert expected == result, result

        obj = {'objBytes': {'data': ['\xac', '\xed', '\x00', '\x05', 'u', 'r', '\x00', '\x13', '[', 'L', 'j', 'a', 'v', 'a', '.', 'l', 'a', 'n', 'g', '.', 'O', 'b', 'j', 'e', 'c', 't', ';', '\x90', '\xce', 'X', '\x9f', '\x10', 's', ')', 'l', '\x02', '\x00', '\x00', 'x', 'p', '\x00', '\x00', '\x00', '\x01', 't', '\x00', '\x04', 'm', 's', 'g', '1'], '_cls': {'fields': [], '_uid': -5984413125824719648, 'flags': '\x02', 'parent': None, '_name': '[B'}, '_name': '[B'}, 'locBytes': None, 'hash': -657890407, '_cls': {'fields': [('hash', 'I', ''), ('locBytes', '[', u'[B'), ('objBytes', '[', u'[B')], '_uid': 8988374069173025854L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.MarshalledObject'}, '_name': 'java.rmi.MarshalledObject'}
        ser.serial_obj(obj)
        result = binascii.hexlify(out.getvalue())
        expected += '737200196a6176612e726d692e4d61727368616c6c65644f626a6563747cbd1e97ed63fc3e020003490004686173685b00086c6f6342797465737400025b425b00086f626a427974657371007e0005707870d8c9639970757200025b42acf317f8060854e002000070787000000033aced0005757200135b4c6a6176612e6c616e672e4f626a6563743b90ce589f1073296c0200007870000000017400046d736731'
        assert expected == result, result

        out2 = StringIO.StringIO()
        obj2 = {'data': ['msg1'], '_cls': {'fields': [], '_uid': -8012369246846506644, 'flags': '\x02', 'parent': None, '_name': '[Ljava.lang.Object;'}, '_name': '[Ljava.lang.Object;'}
        serial_obj(out2, obj2)
        expected2 = obj['objBytes']['data']
        result =  list(binascii.unhexlify('aced0005') + out2.getvalue())
        assert expected2 == result, result
        #
        obj = {'data': ['java.lang.String'], '_cls': {'fields': [], '_uid': -5921575005990323385, 'flags': '\x02', 'parent': None, '_name': '[Ljava.lang.String;'}, '_name': '[Ljava.lang.String;'}
        ser.serial_obj(obj)
        result = binascii.hexlify(out.getvalue())
        expected += '757200135b4c6a6176612e6c616e672e537472696e673badd256e7e91d7b47020000707870000000017400106a6176612e6c616e672e537472696e67'
        assert expected == result, result

        obj = None
        ser.serial_obj(obj)
        result = binascii.hexlify(out.getvalue())
        expected += '70'
        assert expected == result, result

    def test_read_suggested_hostname(self):
        inp = binascii.unhexlify('4e000f3130302e3130312e3130322e3130330000d919')
        sh, sp = read_suggested_hostname(inp)
        assert (u'100.101.102.103', 55577) == (sh, sp), (sh, sp)

    def test_create_protocol_msg(self):
        expected = '4a524d4900024b'
        msg = create_protocol_msg()
        assert expected == binascii.hexlify(msg), binascii.hexlify(msg)

    def test_create_local_hostname_msg(self):
        expected = '000b3139322e3136382e302e3500000000'
        msg = create_local_hostname_msg('192.168.0.5')
        assert expected == binascii.hexlify(msg), binascii.hexlify(msg)

    def test_create_lookup_msg(self):
        expected = '50aced00057722000000000000000000000000000000000000000000000000000244154dc9d4e63bdf7400066a6d78726d69'
        msg = create_lookup_msg()
        assert expected == binascii.hexlify(msg), binascii.hexlify(msg)

