from abc import ABCMeta, abstractmethod

from apps.design_pattern.factory_pattern.constant import PenType

"""
抽象工厂模式
多种分类：
画笔可以根据类型分为直线、矩形、椭圆等，也可以根据颜色分为红色图形、绿色图形、蓝色图形等。
"""

"""
第一步，先定义类型类这个系列
"""


class PType(metaclass=ABCMeta):
    """画笔类型抽象类"""

    def __init__(self, name):
        self.__name = name

    @abstractmethod
    def get_type(self):
        pass

    def get_name(self):
        return self.__name


class LinePen(PType):
    """直线画笔"""

    def __init__(self, name):
        super().__init__(name)

    def get_type(self):
        return PenType.PenTypeLine


class RectanglePen(PType):
    """矩形画笔"""

    def __init__(self, name):
        super().__init__(name)

    def get_type(self):
        return PenType.PenTypeRect


class EllipsePen(PType):
    """椭圆画笔"""

    def __init__(self, name):
        super().__init__(name)

    def get_type(self):
        return PenType.PenTypeEllipse


"""
第二步，定义颜色类这个系列
"""


class PColor(metaclass=ABCMeta):
    """画笔颜色抽象类"""

    def color(self, name):
        pass


# 定义3个颜色类，都是实现PColor接口，并且每一个图形都有一个可以获取颜色名称的方法，相当于重写接口方法
class Red(PColor):
    def color(self, name):
        print(f'我的颜色是：{name}')


class Blue(PColor):
    def color(self, name):
        print(f'我的颜色是：{name}')


class Black(PColor):
    def color(self, name):
        print(f'我的颜色是：{name}')


"""
第三步，定义抽象工厂以及与每一个系列对应的工厂
"""


class PenFactory(metaclass=ABCMeta):
    def create_type(self, pen_type):
        pass

    def create_color(self, name):
        pass


# 创建形状这一个系列的工厂
class PenTypeFactory(PenFactory):  # 模拟类型实现某一个接口，实际上是类的继承
    def create_type(self, pen_type):  # 重写接口中的方法
        if pen_type == PenType.PenTypeLine:
            pen = LinePen("直线画笔")
        elif pen_type == PenType.PenTypeRect:
            pen = RectanglePen("矩形画笔")
        elif pen_type == PenType.PenTypeEllipse:
            pen = EllipsePen("椭圆画笔")
        else:
            pen = None
        return pen


# 创建颜色这一个系列的工厂
class PenColorFactory(PenFactory):  # 模拟类型实现某一个接口，实际上是类的继承
    def create_color(self, name):  # 重写接口中的方法
        if name == 'Red':
            color = Red()
        elif name == 'Blue':
            color = Blue()
        elif name == 'Black':
            color = Black()
        else:
            color = None
        return color


"""
第四步，定义产生工厂类的类——抽象工厂模式的核心所在
"""


# 定义一个专门产生工厂的类
class FactoryProducer:
    @staticmethod
    def get_factory(name):
        if name == 'Type':
            return PenTypeFactory()
        elif name == 'Color':
            return PenColorFactory()
        else:
            return None


if __name__ == '__main__':
    factory_producer = FactoryProducer()
    pen_type_factory = factory_producer.get_factory("Type")
    pen_color_factory = factory_producer.get_factory("Color")

    line_pen = pen_type_factory.create_type(PenType.PenTypeLine)
    print(f"创建了{line_pen.get_name()}. 对象id:{id(line_pen)}. 类型:{line_pen.get_type()}")

    rect_pen = pen_type_factory.create_type(PenType.PenTypeRect)
    print(f"创建了{rect_pen.get_name()}. 对象id:{id(rect_pen)}. 类型:{rect_pen.get_type()}")

    ellipsis_pen = pen_type_factory.create_type(PenType.PenTypeEllipse)
    print(f"创建了{ellipsis_pen.get_name()}. 对象id:{id(ellipsis_pen)}. 类型:{ellipsis_pen.get_type()}")

    red = pen_color_factory.create_color('Red')
    red.color('红色')

    blue = pen_color_factory.create_color('Blue')
    blue.color('蓝色')

    black = pen_color_factory.create_color('Black')
    black.color('黑色')
