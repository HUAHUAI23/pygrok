import regex as re

type_mapper = {}
m = re.findall(r'%{(\w+):(\w+):(\w+)}', '%{NUMBER:weight:float}')
print(m)
for n in m:
    type_mapper[n[1]] = n[2]
print(type_mapper)