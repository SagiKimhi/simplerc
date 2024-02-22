import simplerc as rc
from random import random, randbytes, randint
from dataclasses import dataclass


@dataclass
class DemoClass:
    a: float = 0
    b: int = 0
    c: str = ''


def get_demo():
    demo = DemoClass()
    demo.a = random()
    demo.b = randint(0, 15)
    demo.c = str(randbytes(demo.b))
    return demo


def init_demo():
    for _ in range(5):
        rc.set_(f"immutable_demo{_}", get_demo())
    for _ in range(5):
        rc.set_(f"demo{_}", get_demo(), mutable=True)


def ptitle(title: str):
    print("\n")
    print(title)


def run_demo():

    ptitle("Getting a copy of the dictionary:")
    print(f"\t{rc.rcdict()=}")

    ptitle("Getting a weak reference to the manager:")
    print(f"\t{rc.manager=}")

    ptitle("Iterating Keys:")
    for key in rc.keys():
        print(f"\t{key=}")

    ptitle("Iterating Values:")
    for value in rc.values():
        print(f"\t{value=}")

    ptitle("Iterating Items:")
    for item in rc.items():
        print(f"\t{item=}")

    ptitle("Get only the values:")
    print("for key in rc.manager:")
    for key in rc.manager:
        print(f"\t{rc.get(key)=}")


if __name__ == "__main__":
    init_demo()
    run_demo()
