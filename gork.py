try:
    import regex as re
except ImportError as e:
    # If you import re, grok_match can't handle regular expression containing atomic group(?>)
    import re
import codecs
import os
import pkg_resources


class Grok(object):

    def __init__(self,
                 pattern,
                 custom_patterns_dir=None,
                 custom_patterns={},
                 fullmatch=True):
        self.pattern = pattern
        self.custom_patterns_dir = custom_patterns_dir
        self.predefined_patterns = {}
        self.fullmatch = fullmatch
        self.regex_obj = []
        custom_pats = {}
        # {'ID':'%{WORD}-%{INT}'}
        # custom_pats = {'ID': pattern}
        # <Pattern:pattern_name  pattern.regex_str  sub_patterns
        # <Pattern:ID,  %{WORD}-%{INT}  >

        if custom_patterns_dir is not None:
            custom_pats = _reload_patterns([custom_patterns_dir])

        for pat_name, regex_str in custom_patterns.items():
            custom_pats[pat_name] = Pattern(pat_name, regex_str)

        if len(custom_pats) > 0:
            self.predefined_patterns.update(custom_pats)

        self._load_search_pattern()

    def match(self, text):
        """If text is matched with pattern, return variable names specified(%{pattern:variable name})
        in pattern and their corresponding values.If not matched, return None.
        custom patterns can be passed in by custom_patterns(pattern name, pattern regular expression pair)
        or custom_patterns_dir.
        """

        match_obj = None
        for regex_obj in self.regex_obj:
            if self.fullmatch:
                match_obj = regex_obj[0].fullmatch(text)
            else:
                match_obj = regex_obj[0].search(text)
            if not match_obj == None:
                matches = match_obj.groupdict()
                for key, match in matches.items():
                    try:
                        if regex_obj[1][key] == 'int':
                            matches[key] = int(match)
                        if regex_obj[1][key] == 'float':
                            matches[key] = float(match)
                    except (TypeError, KeyError) as e:
                        pass
                break

        if match_obj == None:
            return None

        return matches

    def add_search_pattern(self, pattern=None):
        if type(pattern) is not str:
            raise ValueError("Please supply a valid pattern")
        self.pattern = pattern
        self._load_search_pattern()

    def _load_search_pattern(self):
        type_mapper = {}
        py_regex_pattern = self.pattern
        while True:
            # Finding all types specified in the groks
            m = re.findall(r'%{(\w+):(\w+):(\w+)}', py_regex_pattern)
            for n in m:
                type_mapper[n[1]] = n[2]
            #replace %{pattern_name:custom_name} (or %{pattern_name:custom_name:type}
            # with regex and regex group name

            py_regex_pattern = re.sub(
                r'%{(\w+):(\w+)(?::\w+)?}',  # 采用懒模式，大多数时候是 %{pattern_name:custom_name}这种形式，所以采用懒模式
                lambda m: "(?P<" + m.group(2) + ">" + self.predefined_patterns[
                    m.group(1)].regex_str + ")",
                py_regex_pattern)

            py_regex_pattern = re.sub(
                r'%{(\w+)}', lambda m: "(" + self.predefined_patterns[m.group(
                    1)].regex_str + ")", py_regex_pattern)

            if re.search('%{\w+(:\w+)?}', py_regex_pattern) is None:
                break

        self.regex_obj.append((re.compile(py_regex_pattern), type_mapper))


def _reload_patterns(patterns_dirs):
    """
    """
    all_patterns = {}
    for dir in patterns_dirs:
        for f in os.listdir(dir):
            patterns = _load_patterns_from_file(os.path.join(dir, f))
            all_patterns.update(patterns)

    return all_patterns


def _load_patterns_from_file(file):
    """
    """
    patterns = {}
    with codecs.open(file, 'r', encoding='utf-8') as f:
        for l in f:
            l = l.strip()
            if l == '' or l.startswith('#'):
                continue

            sep = l.find(' ')
            pat_name = l[:sep]
            regex_str = l[sep:].strip()
            pat = Pattern(pat_name, regex_str)
            patterns[pat.pattern_name] = pat
    return patterns


class Pattern(object):
    """
    """

    def __init__(self, pattern_name, regex_str, sub_patterns={}):
        self.pattern_name = pattern_name
        self.regex_str = regex_str
        self.sub_patterns = sub_patterns  # sub_pattern name list

    def __str__(self):
        return '<Pattern:%s,  %s,  %s>' % (self.pattern_name, self.regex_str,
                                           self.sub_patterns)