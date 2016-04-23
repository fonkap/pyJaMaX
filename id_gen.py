import copy
import random
import time

from tool import qu, p

current_time_millis = lambda: int(time.time() * 1000)

class UIDGenerator:
    mould = {'count': 0, '_name': 'java.rmi.server.UID', 'unique': 0, '_cls': {'fields': [['count', 'S', ''], ['time', 'J', ''], ['unique', 'I', '']], '_uid': 1086053664494604050L, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.UID'}, 'time': 0}

    def __init__(self):
        self.hostUnique = p(qu(random.getrandbits(32), 4))
        self.lastCount = -32767  # UID.lastCount line 78
        self.lastTime = current_time_millis()

    def generate(self):
        uid = copy.copy(UIDGenerator.mould)
        uid['unique'] = self.hostUnique
        uid['time'] = self.lastTime
        uid['count'] = self.lastCount
        self.lastCount += 1
        return uid

    @staticmethod
    def create_well_known(num):
        uid = copy.copy(UIDGenerator.mould)
        uid['unique'] = 0
        uid['time'] = 0
        uid['count'] = num
        return uid


class VMIDGenerator:
    def __init__(self, uidgen):
        self.randomBytes = [chr(random.randint(0,255)) for _ in range(8)]
        self.mould = {'_name': 'java.rmi.dgc.VMID', '_cls': {'fields': [['addr', '[', '[B'], ['uid', 'L', 'Ljava/rmi/server/UID;']], '_uid': -538642295484486218, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.dgc.VMID'}, 'uid': None, 'addr': {'data': [], '_cls': {'fields': [], '_uid': -5984413125824719648, 'flags': '\x02', 'parent': None, '_name': '[B'}, '_name': '[B'}}
        self.uidgen = uidgen

    def generate(self):
        vmid = copy.copy(self.mould)
        vmid['addr']['data'] = self.randomBytes
        vmid['uid'] = self.uidgen.generate()
        return vmid


class ObjIDGenerator:
    mould = {'_name': 'java.rmi.server.ObjID', 'space': None, '_cls': {'fields': [['objNum', 'J', ''], ['space', 'L', 'Ljava/rmi/server/UID;']], '_uid': -6386392263968365220, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.server.ObjID'}, 'objNum': 0}

    @staticmethod
    def create_well_known(num):
        objid = copy.copy(ObjIDGenerator.mould)
        objid['space'] = UIDGenerator.create_well_known(0)
        objid['objNum'] = num
        return objid


def build_obj_array(items, uid):
    mould = {'data': None, '_cls': {'fields': [], '_uid': 0, 'flags': '\x02', 'parent': None, '_name': None}, '_name': None}
    cls = mould['_cls']
    cls['_uid'] = uid
    cls['_name'] = '[L' + items[0]['_cls']['_name'] + ';'
    mould['_name'] = cls['_name']
    mould['data'] = items
    return mould


def build_lease(vmid, duration):
    mould = {'vmid': None, '_cls': {'fields': [['value', 'J', ''], ['vmid', 'L', 'Ljava/rmi/dgc/VMID;']], '_uid': -5713411624328831948, 'flags': '\x02', 'parent': None, '_name': 'java.rmi.dgc.Lease'}, 'value': 0, '_name': 'java.rmi.dgc.Lease'}
    cls = mould['_cls']
    mould['vmid'] = vmid
    mould['value'] = duration
    return mould


