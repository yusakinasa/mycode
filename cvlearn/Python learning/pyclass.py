class Calculator:
    name = "Simple Calculator"
    price = 100


    def __init__(self,name,price,weight):   #也可以指定默认值
        self.name = name
        self.price = price
        self.weight = weight
        print("这是一个初始化方法")   #这个方法会在创建对象时自动调用

    def add(self,x,y):
        print(self.name)
        print(x+y)


    #假如你有一个类称为MyClass和这个类的一个实例MyObject。
    # 当你调用这个对象的方法MyObject.method(arg1, arg2)的时候，
    # 这会由Python自动转为MyClass.method(MyObject, arg1, arg2)——这就是self的原理了。


# cal  = Calculator()
# print(cal.name)

# cal.add(1,2)


cal2 = Calculator("高级计算器",200,1.5) 
print(cal2.name)