import sys

sys.path.append('/home/i42/pro/python/pygrok')
from gork import Grok

text = 'gary is male, 25 years old and weighs 68.5 kilograms'
text1 = 'Beijing-1104,gary 25 "never quit"'
text2 = 'fasfsafsafasfas'
pattern = '%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old and weighs %{NUMBER:weight:float} kilograms'
pattern1 = '%{ID:user_id},%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
grok = Grok(pattern,
            custom_patterns_dir='/home/i42/pro/python/pygrok/pygrok/patterns',
            custom_patterns={'ID': '%{WORD}-%{INT}'})
grok.add_search_pattern(pattern1)
print(grok.match(text2))
