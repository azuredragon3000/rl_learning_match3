
from Pair import Pair

class PotentialY:
    def __init__(self, col, pos, value, x, y):
        self.col = col
        self.pos = pos
        self.value = value
        #print("cuong here ",x,y)
        self.x = y
        self.y = x+col
        #input()
        
        self.pairs = []
        pair = self.poten1() 
        if pair is not None: 
            self.pairs.append(pair)

        pair = self.poten2() 
        if pair is not None: 
            self.pairs.append(pair) 

        pair = self.poten3() 
        if pair is not None: 
            self.pairs.append(pair) 

        pair = self.poten4() 
        if pair is not None: 
            self.pairs.append(pair)

        pair = self.poten5() 
        if pair is not None: 
            self.pairs.append(pair)

        pair = self.poten6() 
        if pair is not None: 
            self.pairs.append(pair)
            
    def __str__(self): 
        pairs_str = ', '.join(str(pair) for pair in self.pairs)
        return f'Position(col={self.col},pos={self.pos}, value={self.value},x={self.x},y={self.y},pairs={pairs_str})'

    def poten1(self):
        if self.x + 2 > 6 or self.y - 1 < 0:
            return None
        return Pair(self.x + 2,self.y - 1 ,1)

            
    def poten2(self):
        if self.x + 2 > 6 or self.y + 1 > 6:
            return None
        return Pair(self.x + 2,self.y + 1 ,2)

    def poten3(self):
        if self.x - 1 < 0 or self.y + 1 > 6:
            return None
        return Pair(self.x - 1,self.y + 1 ,3)

    def poten4(self):
        if self.x - 1 < 0 or self.y -1 < 0:
            return None
        return Pair(self.x - 1,self.y - 1 ,4)

    def poten5(self):
        if self.x + 3 > 6:
            return None
        return Pair(self.x+3, self.y,5)
        
    def poten6(self):
        if self.x - 2 < 0:
            return None
        return Pair(self.x-2, self.y,6)    