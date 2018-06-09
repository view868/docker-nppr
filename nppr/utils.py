import re


class AttributeDict(dict):
    """

    """

    def __getattr__(self, key):
        """
        重写get方法
        :param key:
        :return:
        """
        try:
            text = self[key]
            # 解决需要替换的字符
            ary = re.findall('{(.*?)}', str(text))
            if len(ary) > 0:
                rep = {}
                for item in ary:
                    rep.update({item: self[item]})
                text = text.format(**rep)
            return text
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *names):
        for name in names:
            value = self.get(name)
            if value:
                return value
