import datetime
import functools
import time


def cache_result(func):
    """
    装饰器函数，用于缓存函数的结果。
    """
    cache = {}
    """
    使用@functools.wraps(func)装饰内部函数可以继承被装饰函数的元数据，确保被装饰函数的名称、文档字符串等信息不会被修改或丢失。
    这对于调试和文档生成非常有用。
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


@cache_result
def expensive_operation(n):
    """
    被装饰的函数，模拟一个耗时的操作。
    """
    time.sleep(5)
    return n * 2


def add_prefix(arg_prefix, res_prefix):
    """
    装饰器工厂函数，接受两个参数arg_prefix和res_prefix，返回装饰器函数decorator。
    """

    def decorator(func):
        """
        装饰器函数，接受一个函数func作为参数，定义内部函数wrapper。
        """

        def wrapper(*args, **kwargs):
            """
            内部函数wrapper，对传入的参数进行修改，然后调用func函数，并对返回值进行修改。
            """
            print('arg_prefix', arg_prefix)
            print('res_prefix', res_prefix)
            modified_args = [f"{arg_prefix}{arg}" for arg in args]  # 修改位置参数，添加前缀
            print('修改了传入参数，给参数加上了前缀：', modified_args)
            modified_kwargs = {key: f"{arg_prefix}{value}" for key, value in kwargs.items()}  # 修改关键字参数，添加前缀
            print('修改了关键字参数，给参数加上了前缀：', modified_kwargs)
            result = func(*modified_args, **modified_kwargs)  # 调用原函数并获取返回值
            return f"{res_prefix}{result}"  # 修改返回结果，添加前缀

        return wrapper

    return decorator


@add_prefix(arg_prefix="=参数前缀=", res_prefix="=结果前缀=")
def greet(name, **kwargs):
    """
    被装饰的函数greet，用于生成欢迎消息。
    """
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    return '函数结果{}'.format(name)


if __name__ == '__main__':
    """
    - 装饰器可以修改函数的输入参数，关键字参数，函数运行结束的返回值
      - 输入验证
      - 函数运行的计时器
      - 日志记录、性能监控、输入转换
      - 异常处理
    """

    message = greet("Alice", a=1, b=2)
    print(message)

    """
    - 装饰器可以用于缓存函数运行结果，避免重复计算
      - 使用@functools.wraps 可以修改函数运行时的全局变量
      - 因此装饰器可以使用到保持数据库的连接
    """
    print('第一次运行开始', datetime.datetime.now())
    result1 = expensive_operation(5)  # 第一次调用，执行耗时操作
    print(result1)
    print('第一次运行结束', datetime.datetime.now())
    print('第二次运行开始', datetime.datetime.now())
    result2 = expensive_operation(5)  # 第二次调用，从缓存中获取结果
    print(result2)
    print('第二次运行结束', datetime.datetime.now())
