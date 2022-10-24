import sys

sys.path.append('/home/i42/pro/python/pygrok')
from pygrok import Grok

# text = 'gary is male, 25 years old and weighs 68.5 kilograms'
# pattern = '%{WORD:name} is %{WORD:gender}, %{NUMBER:age:int} years old and weighs %{NUMBER:weight:float} kilograms'
# grok = Grok(pattern)
# print(grok.match(text))


def test_custom_pats():
    custom_pats = {'ID': '%{WORD}-%{INT}'}
    text = 'Beijing-1104,gary 25 "never quit"'
    pat = '%{ID:user_id},%{WORD:name} %{INT:age} %{QUOTEDSTRING:motto}'
    grok = Grok(pat, custom_patterns=custom_pats)
    m = grok.match(text)
    assert m['user_id'] == 'Beijing-1104' and m['name'] == 'gary' and m['age'] == '25' \
        and m['motto'] == '"never quit"', 'grok match failed:%s, %s' % (text, pat, )


test_custom_pats()