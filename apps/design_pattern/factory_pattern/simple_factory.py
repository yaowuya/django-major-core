from abc import ABCMeta, abstractmethod

from apps.design_pattern.factory_pattern.constant import PenType

"""
简单工厂方法
优点：
（1）实现简单、结构清晰。
（2）抽象出一个专门的类来负责某类对象的创建，分割出创建的职责，不能直接创建具体的对象，只需传入适当的参数即可。
（3）使用者可以不关注具体对象的类名称，只需知道传入什么参数可以创建哪些需要的对象。
缺点：
（1）不易拓展，一旦添加新的产品类型，就不得不修改工厂的创建逻辑。不符合“开放封闭”原则，
如果要增加或删除一个产品类型，就要修改switch...case...（或if...else...）的判断代码。
（2）当产品类型较多时，工厂的创建逻辑可能过于复杂，switch...case...（或if...else...）判断会变得非常多。
一旦出错可能造成所有产品创建失败，不利于系统的维护。
"""
"""
在众多的在线教育产品和视频教学产品中都会有一个白板功能（用电子白板来模拟线下的黑板功能），
白板功能中需要不同类型的画笔，比如直线、矩形、椭圆等，但在一个白板中我们只需要一支画笔。
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


class PenFactory:
    """画笔工厂类"""

    def __init__(self):
        """定义一个字典，来存放对象，确保每个类型只有一个对象"""
        self.__pens = {}

    def get_single_obj(self, pen_type, name):
        """获得唯一实例的对象"""
        pass

    def create_pen(self, pen_type):
        """创建画笔"""
        if self.__pens.get(pen_type) is None:
            if pen_type == PenType.PenTypeLine:
                pen = LinePen("直线画笔")
            elif pen_type == PenType.PenTypeRect:
                pen = RectanglePen("矩形画笔")
            elif pen_type == PenType.PenTypeEllipse:
                pen = EllipsePen("椭圆画笔")
            else:
                pen = Pen("")
            self.__pens[pen_type] = pen
        return self.__pens[pen_type]


if __name__ == "__main__":
    factory = PenFactory()
    line_pen = factory.create_pen(PenType.PenTypeLine)
    print(f"创建了{line_pen.get_name()}. 对象id:{id(line_pen)}. 类型:{line_pen.get_type()}")

    rect_pen = factory.create_pen(PenType.PenTypeRect)
    print(f"创建了{rect_pen.get_name()}. 对象id:{id(rect_pen)}. 类型:{rect_pen.get_type()}")

    ellipsis_pen = factory.create_pen(PenType.PenTypeEllipse)
    print(f"创建了{ellipsis_pen.get_name()}. 对象id:{id(ellipsis_pen)}. 类型:{ellipsis_pen.get_type()}")
