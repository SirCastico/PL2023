import sys
import re

re_levantar = re.compile(r"^LEVANTAR$")

re_pousar = re.compile(r"^POUSAR$")

re_abortar = re.compile(r"^ABORTAR$")

re_moeda = re.compile(r"^MOEDA (?P<moedas>(?:\d\d?[ec][,.]? ?)+)$")
re_moeda_val = re.compile(r"([125]0?c|[12]e)[,.]?")

re_numero = re.compile(r"T=\d{9}")

class Start:
    def next_state(self, line:str):
        if line == "LEVANTAR":
            print("introduza moedas")
            return Running()
        else:
            print("ação não reconhecida")
            return self

class Running:

    def __init__(self) -> None:
        self.money = 0

    def next_state(self, line:str):
        ret_state = self

        if re_pousar.match(line):
            print(f"troco = {self.money//100}e{self.money%100}c; Volte sempre!")
            ret_state = Start()

        elif re_abortar.match(line):
            print(f"devolução = {self.money//100}e{self.money%100}c")
            self.money = 0
        
        elif m := re_moeda.match(line):
            msplit = m.group("moedas").split(",")
            
            for moeda in msplit:
                if mm := re_moeda_val.search(moeda):
                    mstr = mm.group(1)
                    if mstr[-1] == "e":
                        self.money += int(mstr.rstrip("e")) * 100
                    else:
                        self.money += int(mstr.rstrip("c"))
                else:
                    print(f"{moeda.strip()} - moeda inválida")
            
            print(f"saldo = {self.money//100}e{self.money%100}c")

        elif m := re_numero.match(line):
            ...
        
        else:
            print("ação não reconhecida")

        
        return ret_state


state = Start()

for line in sys.stdin:
    sline = line.strip()
    state = state.next_state(sline)
