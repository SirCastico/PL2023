import sys
import re

re_levantar = re.compile(r"^LEVANTAR$")

re_pousar = re.compile(r"^POUSAR$")

re_abortar = re.compile(r"^ABORTAR$")

re_moeda = re.compile(r"^MOEDA (?P<moedas>(?:\d\d?[ec][,.]? ?)+)$")
re_moeda_val = re.compile(r"([125]0?c|[12]e)[,.]?")

re_numero = re.compile(r"T=(00\d+|\d{9})")

num_dict = {
    "601": -1,
    "641": -1,
    "00": 150,
    "2": 25,
    "800": 0,
    "808": 10
}

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
            val = -2
            num = m.group(1)
            for prefix, dval in num_dict.items():
                if num.startswith(prefix):
                    val = dval
                    break
            
            match val:
                case -2:
                    print("número inválido")
                case -1:
                    print("número bloqueado")
                case _:
                    self.money -= val
                    print(f"saldo = {self.money//100}e{self.money%100}c")
        else:
            print("ação não reconhecida")

        
        return ret_state


state = Start()

for line in sys.stdin:
    sline = line.strip()
    state = state.next_state(sline)
