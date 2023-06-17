import sqlite3
import functools
import time


def cached_connection(func):
    """
    装饰器函数，用于缓存数据库连接。

    Args:
        func: 被装饰的函数。

    Returns:
        wrapper: 内部函数，用于执行被装饰的函数。
    """
    conn = None

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # nonlocal 关键字仅适用于嵌套函数的情况，用于访问外部函数的局部变量。
        nonlocal conn
        if conn is None:
            # 建立数据库连接
            conn = sqlite3.connect("mydatabase.db")
        try:
            # 执行被装饰的函数
            result = func(conn, *args, **kwargs)
            conn.commit()  # 提交事务
            return result
        except Exception as e:
            conn.rollback()  # 回滚事务
            print(f"Database Error: {e}")
        finally:
            # 不关闭数据库连接，在需要时可以继续使用
            pass

    def close_connection():
        """
        关闭数据库连接的函数。
        """
        nonlocal conn
        if conn is not None:
            print('关闭数据库连接')
            # 因为编辑器无法通过静态分析获取到 conn 对象在 close_connection 函数中的引用
            # 因此会有一个警告，但是不影响程序正常的运行
            conn.close()

    wrapper.close_connection = close_connection
    return wrapper


@cached_connection
def insert_data(conn, data):
    """
    插入数据的函数，被装饰器装饰。
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mytable VALUES (?)", (data,))
    cursor.close()


if __name__ == '__main__':
    # 调用被装饰的函数
    insert_data("Hello, World0")
    time.sleep(2)
    # 下面的函数很坑，编辑器不能获取所在的位置，但是可以正常运行
    # 编辑器通常使用静态分析来提供代码导航和自动补全等功能。
    # 对于在运行时动态添加的函数或属性，编辑器无法通过静态分析获取到它们的位置信息。
    # 因为 close_connection 函数是在运行时动态添加到装饰器函数的 wrapper 对象上的，而不是在代码静态分析阶段就存在的。
    insert_data.close_connection()
