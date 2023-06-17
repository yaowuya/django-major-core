# 需求
"""
在寒冷的冬天，Tony坐2个小时的“地铁+公交”回到住处，拖着疲惫的身体，准备洗一个热水澡暖暖身体，
奈何简陋的房子中用的还是20世纪90年代的热水器。因为热水器没有警报，更没有自动切换模式的功能，
所以烧热水必须得守着，不然时间长了成“杀猪烫”，时间短了又“冷成狗”。无奈的 Tony 背靠着墙，头望着天花板，
深夜中做起了白日梦：一定要努力工作，过两个月我就可以自己买一个智能热水器了，水烧好了就发一个警报，我就可以直接去洗澡。
还要能自己设定模式，既可以烧开了用来喝，又可以烧暖了用来洗澡……
"""
from apps.design_pattern.observer_pattern.base import Observable, Observer


class WaterHeater(Observable):
    def __init__(self):
        super(WaterHeater, self).__init__()
        self.__temperature = 25

    def get_temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = temperature
        print(f"当前温度是:{self.__temperature}℃")
        self.notify_observers()


class WashingMode(Observer):
    """该模式用于洗澡"""

    def update(self, observable, obj):
        if isinstance(observable, WaterHeater) and 50 <= observable.get_temperature() < 70:
            print("水已烧好！温度正好，可以用来洗澡了。")


class DrinkingMode(Observer):
    """该模式用于饮用"""

    def update(self, observable, obj):
        if isinstance(observable, WaterHeater) and observable.get_temperature() >= 100:
            print("水已经烧开！可以用来饮用了。")


if __name__ == "__main__":
    heater = WaterHeater()
    washing_observable = WashingMode()
    drinking_observable = DrinkingMode()
    heater.add_observer(washing_observable)
    heater.add_observer(drinking_observable)
    heater.set_temperature(40)
    heater.set_temperature(60)
    heater.set_temperature(100)
