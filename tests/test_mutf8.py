import binascii
from unittest import TestCase

from jawa.util.mutf8 import *


class TestMutf8(TestCase):

    def test_encode_utf8_1(self):
        # string containing byte 00
        str1 = u'1\x002'
        bb = encode_modified_utf8(str1)
        assert '31c08032' == binascii.hexlify(bb), binascii.hexlify(bb)

        # Unicode supplementary character U+10400
        str1 = u'\uD801\uDC00'
        bb = encode_modified_utf8(str1)
        assert 'eda081edb080' == binascii.hexlify(bb), binascii.hexlify(bb)

    def test_decode_utf8_1(self):
        str1 = '31c08032'
        str2 = decode_modified_utf8(binascii.unhexlify(str1))
        assert u'1\x002' == str2

        str1 = 'eda081edb080'
        str2 = decode_modified_utf8(binascii.unhexlify(str1))
        assert u'\uD801\uDC00' == str2