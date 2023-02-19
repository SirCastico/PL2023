import sys


class Patient:
    age: int
    gender: str
    tension: int
    cholesterol: int
    heart_beat: int
    has_disease: bool

    def __init__(self, age:int, gender:str, tension:int, cholesterol:int, heart_beat:int, has_disease:bool) -> None:
        self.age = age
        self.gender = gender
        self.tension = tension
        self.cholesterol = cholesterol
        self.heart_beat = heart_beat
        self.has_disease = has_disease
    
    @staticmethod
    def from_string(string:str):
        field_list = []

        sub_str = ""
        for i in range(len(string)):
            c = string[i]
            if c == ',' or i+1 == len(string):
                field_list.append(sub_str);
                sub_str = ""
            else:
                sub_str+=c
        
        if len(field_list)<6:
            return None
        
        age = int(field_list[0])
        gender = field_list[1]
        tension = int(field_list[2])
        cholesterol = int(field_list[3])
        heart_beat = int(field_list[4])
        has_disease = True if int(field_list[5])==1 else False

        return Patient(age, gender, tension, cholesterol, heart_beat, has_disease)


def parsePatientInfo(file_path:str) -> list[Patient]:
    p_list = []
    with open(file_path, "r") as file:
        file.readline()
        lines = file.readlines()
        for line in lines:
            p = Patient.from_string(line)
            if p != None:
                p_list.append(Patient.from_string(line))
    
    return p_list


def diseaseDistributionByGender(p_list:list[Patient]):
    dist = {"M":0, "F":0}
    for patient in p_list:
        dist[patient.gender] += 1
    return dist

def diseaseDistributionByAgeGroup(p_list:list[Patient]):
    dist = {}
    lower_group = 1000
    upper_group = -1
    for patient in p_list:
        group = patient.age // 5

        lower_group = group if group<lower_group else lower_group
        upper_group = group if group>upper_group else upper_group

        g_str = f"[{group*5}]-[{group*5+4}]"
        if g_str not in dist:
            dist[g_str] = 1
        else:
            dist[g_str] += 1
    
    for i in range(lower_group, upper_group):
        g_str = f"[{i*5}]-[{i*5+4}]"
        if g_str not in dist:
            dist[g_str] = 0
    
    return dist

def diseaseDistributionByCholesterol(p_list:list[Patient]):
    dist = {}
    lower_group = 1000
    upper_group = -1
    for patient in p_list:
        group = patient.age // 10

        lower_group = group if group<lower_group else lower_group
        upper_group = group if group>upper_group else upper_group

        g_str = f"[{group*10}]-[{group*10+9}]"
        if g_str not in dist:
            dist[g_str] = 1
        else:
            dist[g_str] += 1
    
    for i in range(lower_group, upper_group):
        g_str = f"[{i*10}]-[{i*10+9}]"
        if g_str not in dist:
            dist[g_str] = 0
    
    return dist

def printDistribution(distribution:dict):
    l = list(distribution.items())
    l.sort()
    for key, value in l:
        print(f"{key}: {value}\n")
    print("\n")

def main():
    if len(sys.argv)<2:
        print("Missing argument: path to csv")
        return

    p_list = parsePatientInfo(sys.argv[1])

    print("Distribution by gender\n")
    printDistribution(diseaseDistributionByGender(p_list))

    print("Distribution by age group\n")
    printDistribution(diseaseDistributionByAgeGroup(p_list))

    print("Distribution by cholesterol levels\n")
    printDistribution(diseaseDistributionByCholesterol(p_list))


main()