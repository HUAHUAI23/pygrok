import regex as re
# NOTE re can't handle redefinition of group name
types = {
    'WORD': r'\w+',
    'NUMBER': r'\d+',
    # todo: extend me
}


def compile(pat):
    return re.sub(
        r'%{(\w+):(\w+)}',
        lambda m: "(?P<" + m.group(2) + ">" + types[m.group(1)] + ")", pat)


patterCompiled = compile("%{WORD:method}-%{NUMBER:bytes}-%{NUMBER:duration}")
# patterCompiled: (?P<method>\w+)-(?P<bytes>\d+)-(?P<duration>\d+)
print(patterCompiled)
# groups group groupdict
print(re.search(patterCompiled, "hello-123-456").groupdict())
# {'duration': '456', 'bytes': '123', 'method': 'hello'}

# TODO Dissection
# Dissection
# pat = r"\b([^\W\d_])([^\W\d_]*)([^\W\d_])\b"
# s = "Testers"
# print(re.sub(pat, (lambda m: "{0}{1}{2}".format(m.group(1), len(''.join(set(m.group(2)))), m.group(3))), s))
