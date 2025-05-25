from .utils.PyBinaryReader.binary_reader import *


class ccsParticleAnmCtrl(BrStruct):
    def __init__(self):
        self.name = ""
        self.type = "ParticleAnmCtrl"
        self.path = ""
        self.animation = None
        self.ctrlCount = 0
        self.partAnmCtrlSub = []

    def __br_read__(self, br: BinaryReader, indexTable, version):
        self.index = br.read_uint32()
        self.name = indexTable.Names[self.index][0]
        self.path = indexTable.Names[self.index][1]
        print(f'PartAnmCtrl | Name {self.name} index {self.index}')

        self.animationIndex = br.read_uint32()
        print(f'PartAnmCtrl | animationIndex {self.animationIndex}')

        self.ctrlCount = br.read_uint16()
        print(f'PartAnmCtrl | ctrlCount {self.ctrlCount}')
        br.seek(2, 1)  # Skip CCCC

        # Read and append forceFieldParam
        for i in range(self.ctrlCount):
            self.partAnmCtrlSub.append(br.read_struct(PartAnmCtrlSub, None))
            print(f'PartAnmCtrl | partAnmCtrlSub # {i}')
        

    def finalize(self, chunks):
        self.animation = chunks.get(self.animationIndex)
        print(f'PartAnmCtrl finalize | {self.name} animation {self.animation.name}')


class PartAnmCtrlSub(BrStruct):
    def __init__(self):
        self.partGenerator = None
        self.parent = None
        self.frameCount  = 0
        self.frames = []

    def __br_read__(self, br: BinaryReader):
        self.partGeneratorIndex = br.read_uint32()
        self.parentIndex = br.read_uint32()
        self.unk1 = br.read_uint32()
        self.unk2 = br.read_uint32() # padding?
        self.frameCount = br.read_uint16()
        br.seek(2, 1)  # Skip CCCC
        print(f'PartAnmCtrl | PartAnmCtrlSub frameCount {self.frameCount}')
        self.frames = br.read_uint8(self.frameCount)
        br.align_pos(4)