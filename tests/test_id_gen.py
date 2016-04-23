import StringIO
from unittest import TestCase

import binascii

from id_gen import *
from java_deser.ser import *

from ser import serial_uid, serial, serial_objid, Serializer


class TestIdGen(TestCase):
    def test_uid(self):
        uid_gen = UIDGenerator()
        uid = uid_gen.generate()
        out = StringIO.StringIO()
        serial_uid(out, uid)
        result = binascii.hexlify(out.getvalue())
        assert 28 == len(result), 'wrong len ' + result

    def test_vmid(self):
        uid_gen = UIDGenerator()
        vmid_gen = VMIDGenerator(uid_gen)
        vmid = vmid_gen.generate()
        out = StringIO.StringIO()
        serial(out, [vmid])
        result = binascii.hexlify(out.getvalue())
        assert 362 == len(result), 'wrong len ' + result

    def test_objid(self):
        objid_gen = ObjIDGenerator()
        objid = objid_gen.create_well_known(2)
        out = StringIO.StringIO()
        serial_objid(out, objid)
        result = binascii.hexlify(out.getvalue())
        assert '00000000000000020000000000000000000000000000' == result, 'wrong ' + result

    def test_tmp(self):
        print ts(12525169067719228231L, 8)

    def test_objid_array(self):
        objid_gen = ObjIDGenerator()
        objid = objid_gen.create_well_known(2)
        objid_array = build_obj_array([objid], -8713620060265225090)
        out = StringIO.StringIO()
        ser = Serializer(out, True)
        ser.serial_obj(objid_array)
        result = binascii.hexlify(out.getvalue())
        assert '757200185b4c6a6176612e726d692e7365727665722e4f626a49443b871300b8d02c647e02000070787000000001737200156a6176612e726d692e7365727665722e4f626a4944a75efa128ddce55c0200024a00066f626a4e756d4c000573706163657400154c6a6176612f726d692f7365727665722f5549443b7078700000000000000002737200136a6176612e726d692e7365727665722e5549440f12700dbf364f12020003530005636f756e744a000474696d65490006756e697175657078700000000000000000000000000000' == result, 'wrong ' + result