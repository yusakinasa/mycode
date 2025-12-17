# 默认参数
def power(x, n=2):
    print(f"x={x}, n={n}")

power(5)  # 使用默认参数 n=2
power(5, 3)  # 覆盖默认参数 n=3

# 注意： 默认参数的定义必须在必选参数的后面
# def wrong_power(n=2, x):  # 这样定义会报错

#------------------------------------------------

#global 关键字
APPLE = 10
a = None   # 仍然需要先定义 a
def func():
    global a  # 声明使用全局变量 a
    a = 5
    return a + 100

print(a)  # 调用 func 之前，a 还是 None
print(func())
print(a)  # 调用 func 之后，a 变成了 5