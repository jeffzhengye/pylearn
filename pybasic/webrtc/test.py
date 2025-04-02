class Student(object):
    count = 0  # 类属性，初始化时赋值为0

    def __init__(self, name):
        self.name = name  # 实例属性
        Student.count += 1  # 新增：每次实例化时类属性加1


# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败1!')
    else:
        lisa = Student('Lisa')  # 注意这里应该是'Lisa'而不是再次使用'Bart'
        if Student.count != 2:
            print('测试失败2!')
        else:
            print('Students:', Student.count)
            print('测试通过!')