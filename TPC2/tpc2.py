import sys

class StringAggregateCompare:
    string: str
    comp: str
    i: int

    def __init__(self, string:str) -> None:
        self.string = string.lower()
        self.comp = ""
        self.i = 0

    def addAndCompare(self, char) -> bool:
        if(self.i==len(self.string)):
            return True
        
        char = char.lower()
        if(self.string[self.i]==char):
            self.i += 1
            self.comp += char
            return self.comp==self.string
        else:
            self.i = 0
            self.comp = ""
            return False
    
    def reset(self):
        self.comp = ""
        self.i = 0


class Somador:
    soma: int = 0
    is_on: bool = True

    def sum_line(self, line:str):
        on_cmp = StringAggregateCompare("On")
        off_cmp = StringAggregateCompare("Off")
        cur_digit_str: str = ""

        for c in line:
            if(on_cmp.addAndCompare(c)):
                self.is_on = True
                on_cmp.reset()
            elif(off_cmp.addAndCompare(c)):
                self.is_on = False
                off_cmp.reset()
            elif(c=="="):
                print(self.soma)
            
            if(not self.is_on):
                continue
            
            if(c.isdigit()):
                cur_digit_str += c
            elif(cur_digit_str != ""):
                self.soma += int(cur_digit_str)
                cur_digit_str = ""


somador = Somador()

for line in sys.stdin:
    somador.sum_line(line)

