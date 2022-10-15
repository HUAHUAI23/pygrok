import sys
sys.path.append('/home/i42/pro/python/pygrok')
from pygrok import Grok

text = 'gary is male, 25 years old and weighs 68.5 kilograms'
pattern = '%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old and weighs %{NUMBER:weight:float} kilograms'
grok = Grok(pattern)
print(grok.match(text))
