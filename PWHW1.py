class Meta(type):
    def __new__(meta_class, class_name, parents, attributes):
        attributes['class_number'] = Meta.children_number
        Meta.children_number += 1
        return type.__new__(meta_class, class_name, parents, attributes)


Meta.children_number = 0


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls3(metaclass=Meta):
    def __init__(self, data):
        self.data = data

class Cls4(metaclass=Meta):
    def __init__(self, data):
        self.data = data


#проверка
print(Cls1.class_number, Cls2.class_number)
assert(Cls1.class_number, Cls2.class_number) == (0, 1)

a, b = Cls1(''), Cls2('')

#проверка
print(a.class_number, b.class_number)
print(Meta.children_number)
assert(a.class_number, b.class_number) == (0, 1)

#AssertionError
#assert(a.class_number, b.class_number) == (1, 2)

c = Cls3('')
print(c.class_number)

d = Cls4('')
print(d.class_number)


