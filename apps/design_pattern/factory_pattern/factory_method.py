from abc import ABCMeta, abstractmethod

from apps.design_pattern.factory_pattern.constant import PenType

"""
工厂方法模式
优点：
（1）解决了简单工厂模式不符合“开放-封闭”原则的问题，使程序更容易拓展。
（2）实现简单。
缺点：
对于有多种分类的产品，或具有二级分类的产品，工厂方法模式并不适用。

多种分类：
如我们有一个电子白板程序，可以绘制各种图形，那么画笔的绘制功能可以理解为一个工厂，而图形可以理解为一种产品；
图形可以根据形状分为直线、矩形、椭圆等，也可以根据颜色分为红色图形、绿色图形、蓝色图形等。
二级分类：
如一个家电工厂，它可能同时生产冰箱、空调和洗衣机，那么冰箱、空调、洗衣机属于一级分类；
而洗衣机又可分为高效型的和节能型的，高效型洗衣机和节能型洗衣机就属于二级分类。
"""


class Pen(metaclass=ABCMeta):
    """画笔"""

    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def get_type(self):
        pass

    def get_name(self):
        return self.__name


class LinePen(Pen):
    """直线画笔"""

    def __init__(self, name):
        super().__init__(name)

    def get_type(self):
        return PenType.PenTypeLine


class RectanglePen(Pen):
    """矩形画笔"""

    def __init__(self, name):
        super().__init__(name)

    def get_type(self):
        return PenType.PenTypeRect


class EllipsePen(Pen):
    """椭圆画笔"""

    def __init__(self, name):
        super().__init__(name)

    def get_type(self):
        return PenType.PenTypeEllipse


class AbstractFactory(metaclass=ABCMeta):
    """抽象工厂"""

    @abstractmethod
    def create_pen(self):
        pass


class LinePenFactory(AbstractFactory):
    def create_pen(self):
        return LinePen("直线画笔")


class RectanglePenFactory(AbstractFactory):
    def create_pen(self):
        return LinePen("矩形画笔")


class EllipsePenFactory(AbstractFactory):
    def create_pen(self):
        return LinePen("椭圆画笔")


if __name__ == "__main__":
    line_pen_factory = LinePenFactory()
    line_pen = line_pen_factory.create_pen()
    print(f"创建了{line_pen.get_name()}. 对象id:{id(line_pen)}. 类型:{line_pen.get_type()}")

    rect_pen_factory = RectanglePenFactory()
    rect_pen = rect_pen_factory.create_pen()
    print(f"创建了{rect_pen.get_name()}. 对象id:{id(rect_pen)}. 类型:{rect_pen.get_type()}")

    ellipsis_pen_factory = EllipsePenFactory()
    ellipsis_pen = ellipsis_pen_factory.create_pen()
    print(f"创建了{ellipsis_pen.get_name()}. 对象id:{id(ellipsis_pen)}. 类型:{ellipsis_pen.get_type()}")
