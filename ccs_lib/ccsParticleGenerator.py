from .utils.PyBinaryReader.binary_reader import *
from enum import Enum


class ccsParticleGenerator(BrStruct):
    def __init__(self):
        self.name = ""
        self.type = "ParticleGenerator"
        self.path = ""
        self.resourceCount = 0
        self.forceFieldCount = 0
        self.generatorParam = None
        self.forceField = []
        self.resource = []

    def __br_read__(self, br: BinaryReader, indexTable, version):
        self.index = br.read_uint32()
        self.name = indexTable.Names[self.index][0]
        self.path = indexTable.Names[self.index][1]
        print(f'PartGen | Name {self.name}')

        unk = br.read_uint32()

        self.generatorParam = br.read_struct(GeneratorParam, None)
        print(f'PartGen | HEX flags {self.generatorParam.flags:#08x}')

        self.resourceCount = ((self.generatorParam.flags >> 0x0c) & 0x0f)
        print(f'PartGen | {self.name} resourceCount = {self.resourceCount}')
        self.forceFieldCount = ((self.generatorParam.flags >> 0x10) & 0x0f)
        print(f'PartGen | {self.name} forceFieldCount = {self.forceFieldCount}')
        
        self.fade_400 = br.read_float()
        self.clip_50 = br.read_float()
        self.fade_4000 = br.read_float()
        self.clip_5000 = br.read_float()
        self.unk1 = br.read_float()
        self.unk2 = br.read_float()
        self.unk3 = br.read_float()

        # Read and append forceFieldParam
        for i in range(self.forceFieldCount):
            self.forceField.append(br.read_struct(ForceField, None))
            print(f'PartGen | forceField# {i} Type ({self.forceField[i].type.value:#04x}) {self.forceField[i].type.name}')

        # Read and append forceFieldParam
        for i in range(self.resourceCount):
            self.resource.append(br.read_struct(Resource, None))
            print(f'PartGen | resource# {i} index {self.resource[i].resourceIndex}')
    
    def finalize(self, chunks):
        #print("PartGen | finalize() called")  # Debug line
        for i in range(self.resourceCount):
            self.resource[i] = chunks.get(self.resource[i].resourceIndex)
            print(f'PartGen finalize | {self.name} resource # {i} index {self.resource[i].name}')


class GeneratorParam(BrStruct):
    def __init__(self):
        self.flags = 0

    def __br_read__(self, br: BinaryReader):
        self.flags = br.read_uint32()
        self.unk01 = br.read_int16()
        br.seek(2, 1)  # Skip CCCC
        self.unk02 = br.read_uint32()
        self.unk03 = br.read_uint16()
        self.unk04 = br.read_uint16()
        self.unk05 = br.read_uint16()
        self.unk06 = br.read_uint16()
        self.unk07 = br.read_float()
        self.unk08 = br.read_float()
        self.unk09 = br.read_float()
        self.unk10 = br.read_float()
        self.unk11 = br.read_float()
        self.unk12 = br.read_uint16()
        self.unk13 = br.read_uint16()
        self.unk14 = br.read_uint16()
        self.unk15 = br.read_uint16()


class Resource(BrStruct):
    def __init__(self):
        self.resource = None
        self.unk1 = 0
        self.unk2 = 0
        self.unk3 = 0

    def __br_read__(self, br: BinaryReader):
        self.resourceIndex = br.read_uint32()   # CMP ANM EFF
        self.unk1 = br.read_int8()
        self.unk2 = br.read_int8()
        self.unk3 = br.read_int8()
        br.seek(1, 1)  # Skip CC


class ForceField(BrStruct):
    def __init__(self):
        self.type = None
        self.Param = None

    def __br_read__(self, br: BinaryReader):
        br.seek(4, 1)  # Skip padding
        self.unk1 = br.read_uint8() # may not be used, need to check
        br.seek(1, 1)  # Skip padding & CC
        self.type = ForceFieldTypes(br.read_uint16())
        self.unk2 = br.read_uint16()
        br.seek(2, 1)  # Skip CCCC
        self.Param = br.read_struct(ForceFieldParam, None, self.type)
     
class ForceFieldParam(BrStruct):
    def __init__(self):
        self.value0 = 0
        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0
        
    def __br_read__(self, br: BinaryReader, type):

        if type == ForceFieldTypes.ADDITION: # 0x00
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ACCELERATE: # 0x01
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.REVOLUTION: # 0x02
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ROTATE: # 0x03
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ATTRACTIVE: # 0x04
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.SCALE: # 0x05
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.SCALE_X: # 0x06
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.SCALE_Y: # 0x07
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.SCALE_FIX: # 0x08
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.SCALE_CHANGE: # 0x09
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ROTATE_2D: # 0x0a
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ROTATE_2D_FIX: # 0x0b
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ROTATE_3D_FIX: # 0x0c
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.TRACE_POS: # 0x0d
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.FADE_IN_OUT: # 0x0e
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.ROTATE_AXIS: # 0x0f
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.DIST_STOP: # 0x10
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ADDITION: # 0x11
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ACCELERATE: # 0x12
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_float()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_REVOLUTION: # 0x13
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_float()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ROTATE: # 0x14
            self.value0 = br.read_uint32()
            self.value1 = br.read_float()
            self.value2 = br.read_uint32()
            self.value3 = br.read_float()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ATTRACTIVE: # 0x15
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_SCALE: # 0x16
            self.value0 = br.read_uint32()
            self.value1 = br.read_float()   # Scale X
            self.value2 = br.read_float()   # Scale Y
            self.value3 = br.read_float()
            self.value4 = br.read_float()

        elif type == ForceFieldTypes.NEW_SCALE_X: # 0x17
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_SCALE_Y: # 0x18
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_SCALE_FIX: # 0x19
            self.value0 = br.read_uint32()
            self.value1 = br.read_float()
            self.value2 = br.read_float()
            self.value3 = br.read_float()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_SCALE_CHANGE: # 0x1a
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ROTATE_2D: # 0x1b
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ROTATE_2D_FIX: # 0x1c
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ROTATE_3D_FIX: # 0x1d
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_TRACE_POS: # 0x1e
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_FADE_IN_OUT: # 0x1f
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_ROTATE_AXIS: # 0x20
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_float()
            self.value4 = br.read_uint32()

        elif type == ForceFieldTypes.NEW_DIST_STOP: # 0x21
            self.value0 = br.read_uint32()
            self.value1 = br.read_uint32()
            self.value2 = br.read_uint32()
            self.value3 = br.read_uint32()
            self.value4 = br.read_uint32()



class ForceFieldTypes(Enum):
    ADDITION        = 0x00
    ACCELERATE      = 0x01
    REVOLUTION      = 0x02
    ROTATE          = 0x03
    ATTRACTIVE      = 0x04
    SCALE           = 0x05
    SCALE_X         = 0x06
    SCALE_Y         = 0x07
    SCALE_FIX       = 0x08
    SCALE_CHANGE    = 0x09
    ROTATE_2D       = 0x0a
    ROTATE_2D_FIX   = 0x0b
    ROTATE_3D_FIX   = 0x0c
    TRACE_POS       = 0x0d
    FADE_IN_OUT     = 0x0e
    ROTATE_AXIS     = 0x0f
    DIST_STOP       = 0x10

    NEW_ADDITION        = 0x11
    NEW_ACCELERATE      = 0x12
    NEW_REVOLUTION      = 0x13
    NEW_ROTATE          = 0x14
    NEW_ATTRACTIVE      = 0x15
    NEW_SCALE           = 0x16
    NEW_SCALE_X         = 0x17
    NEW_SCALE_Y         = 0x18
    NEW_SCALE_FIX       = 0x19
    NEW_SCALE_CHANGE    = 0x1a
    NEW_ROTATE_2D       = 0x1b
    NEW_ROTATE_2D_FIX   = 0x1c
    NEW_ROTATE_3D_FIX   = 0x1d
    NEW_TRACE_POS       = 0x1e
    NEW_FADE_IN_OUT     = 0x1f
    NEW_ROTATE_AXIS     = 0x20
    NEW_DIST_STOP       = 0x21

