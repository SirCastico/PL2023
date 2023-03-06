import re

def proc_year_freq(path:str) -> dict:
    f = open(path, "r")
    d = {}
    er = re.compile(r"^\d+::(\d+?)-")
    for line in f:
        m = er.match(line)
        if not m:
            continue
        year = int(m.group(1))
        if year not in d:
            d[year] = 1
        else:
            d[year] += 1 
    
    return d

def name_freq(path:str):
    f = open(path, "r")
    d = {}
    er = re.compile(r"^.+?::(\d\d)\d\d.+?::(\w*).*?(\w*)::(\w*).*?(\w*)::(\w*).*?(\w*)::")
    # fname_er = re.compile(r"(?::|(?:\s\s))([A-Z]\w+)")
    # lname_er = re.compile(r"[A-Z]\w+?\s([A-Z]\w+)(?::|,|\s\s)")
    # century_er = re.compile(r"^.+?::(\d\d)\d\d")
    for line in f:
        m = er.match(line)
        if not m:
            continue
        century = int(m.group(1))+1
        if century not in d:
            d[century] = [{},{}]
        first_d, last_d = d[century]
        for i in range(2,7,2):
            f_name = m.group(i)
            if f_name not in first_d:
                first_d[f_name] = 1
            else:
                first_d[f_name] += 1
        for i in range(3,8,2):
            l_name = m.group(i)
            if l_name not in last_d:
                last_d[l_name] = 1
            else:
                last_d[l_name] += 1
    
    for century in d:
        for j in range(2):
            occ_arr = [-1,-1,-1,-1,-1]
            name_arr = ["","","","",""]

            for name, occurrences in d[century][j].items():
                for i in range(1,5):
                    if occurrences>occ_arr[i-1] and occurrences<=occ_arr[i]:
                        occ_arr[i-1] = occurrences
                        name_arr[i-1] = name
                        break
                    if i == 4:
                        occ_arr[i] = occurrences
                        name_arr[i] = name

            d[century][j] = {}

            for i in range(5):        
                d[century][j][name_arr[i]] = occ_arr[i]

    
    return d

def relation_freq(path:str) -> dict:
    f = open(path, "r")
    d = {}
    er = re.compile(r"[A-Z][a-z]+,([A-Z](?:\w|\s)+?)[.]")

    for line in f:
        ml = er.findall(line)
        for rel in ml:
            if rel not in d:
                d[rel] = 1
            else:
                d[rel] += 1
    
    return d

def to_json(path:str):
    f = open(path, "r")
    l = []
    er = re.compile(r"^(?P<n_proc>.+?)::(?P<date>.+?)::(?P<name1>.+?)::(?P<name2>.*?)::(?P<name3>.*?)::(?P<desc>.*?)::$")
    i = 0
    for line in f:
        m = er.match(line)
        if not m:
            continue
        l.append(m.groupdict())
        if len(l)>20:
            break
    
    return str(l).replace("'", "\"") 
        




path = "TPC3/processos.txt"

print("proc freq per year\n")

d1 = proc_year_freq(path)
l1 = list(d1.items())
l1.sort()

for year, freq in l1:
    print(f"{year} -> {freq}")

print("\n")


print("name freq\n")

d2 = name_freq(path)

ld2 = list(d2.keys())
ld2.sort()

for century in ld2:
    print("century: ",century)
    print("first names:")
    l2 = list(d2[century][0].items())
    l2.sort(key=lambda x:x[1], reverse=True)

    for name, freq in l2:
        print(f"{name} -> {freq}")
    
    print("\nlast names:")
    l2 = list(d2[century][1].items())
    l2.sort(key=lambda x:x[1], reverse=True)

    for name, freq in l2:
        print(f"{name} -> {freq}")
    
    print("")


print("\n")


print("relation freq\n")

d3 = relation_freq(path)
l3 = list(d3.items())
l3.sort(key=lambda x:x[1], reverse=True)

for relation, freq in l3:
    print(f"{relation} -> freq: {freq}")

print("\n")


print("20 entries json\n")

js = to_json(path)

print(js)