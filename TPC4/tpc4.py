
import sys
import re
import json
from collections import deque

class ColumnVal:
    _match_obj = re.compile(r"^(?P<name>\w+)$")
    name: str

    def __init__(self, name) -> None:
        self.name = name

    def formVal(self, deq: deque[str]):
        return deq.popleft()

    @staticmethod
    def fromStr(string):
        m = ColumnVal._match_obj.match(string)
        if m==None:
            return None

        return ColumnVal(m.group("name"))

class ColumnList:
    min_vals: int
    max_vals: int
    name: str
    _match_obj = re.compile(r"^(?P<name>\w+){(?:(?P<min>\d),)?(?P<max>\d)}$")

    def __init__(self, name, maxv, minv=0) -> None:
        self.name = name
        self.min_vals = minv
        self.max_vals = maxv
    
    def formVal(self, deq: deque[str]):
        l = []
        for _ in range(self.min_vals):
            l.append(deq.popleft())
        
        for _ in range(self.min_vals, self.max_vals):
            s = deq.popleft()
            if s!="":
                l.append(s)
        
        return l

    @staticmethod
    def fromStr(string):
        m = ColumnList._match_obj.match(string)
        if m==None:
            return None

        return ColumnList(m.group("name"),
                         int(m.group("max")),
                         0 if "min" in m.groupdict() else int(m.group("min")))


class ColumnListAggregation(ColumnList):
    aggr_str: str
    name: str
    _match_obj = re.compile(r"^(?P<name>\w+){(?:(?P<min>\d),)?(?P<max>\d)}::(?P<aggr>\w+)$")

    def __init__(self, name, maxv, aggr_str, minv=0) -> None:
        super().__init__(name, maxv, minv)
        self.aggr_str = aggr_str

    def formVal(self, deq: deque[str]):
        l = super().formVal(deq)
        red = 0
        match(self.aggr_str):
            case "sum":
                for s in l:
                    red += int(s)
            case "media":
                for s in l:
                    red += int(s)
                red /= len(l)

        return red

    @staticmethod
    def fromStr(string):
        m = ColumnListAggregation._match_obj.match(string)
        if m==None:
            return None

        return ColumnListAggregation(m.group("name"),
                                     int(m.group("max")),
                                     m.group("aggr"),
                                     0 if "min" not in m.groupdict() else int(m.group("min")))



def genParserList(line:str):
    cname_list = re.split(r"(?<!{\d),(?!\d})", line)
    parser_list = []

    i=0
    while (i < len(cname_list)):
        cname = cname_list[i]

        if parser := ColumnVal.fromStr(cname):
            parser_list.append(parser)

        elif parser := ColumnList.fromStr(cname):
            i += parser.max_vals-1
            parser_list.append(parser)
        
        elif parser := ColumnListAggregation.fromStr(cname):
            i += parser.max_vals-1
            parser_list.append(parser)

        i+=1
    
    return parser_list





if len(sys.argv)<3:
    print("receives input file and output file arguments")
    exit(1)

file = open(sys.argv[1],"r")

parser_list = genParserList(file.readline().strip())

entries = []

for line in file:
    dt = {}

    dq = deque(line.strip().split(","))

    for parser in parser_list:
        dt[parser.name] = parser.formVal(dq)
    
    entries.append(dt)

file.close()
output = open(sys.argv[2],"w")

json.dump(entries, output)

output.close()

