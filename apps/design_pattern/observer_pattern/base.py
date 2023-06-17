from abc import ABCMeta


# 引入ABCMeta和 来定义抽象类和抽象方法

class Observer(metaclass=ABCMeta):
    """观察者的基类"""

    def update(self, observable, obj):
        pass


class Observable(object):
    """被观察者的基类"""

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self, obj=0):
        for o in self.__observers:
            if hasattr(o, "update"):
                o.update(self, obj)
