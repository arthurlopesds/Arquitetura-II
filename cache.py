class Cache:

    def __init__(self,tag,end,valMem,valInst):
        self.tag = tag
        self.end = end
        self.valMem = valMem
        self.valInst = valInst

    def ObterTag(self):
        return self.tag

    def ObterEnd(self):
        return self.end

    def ObterValMem(self):
        return self.valMem

    def ObterValInst(self):
        return self.valInst

