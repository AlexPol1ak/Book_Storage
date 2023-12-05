# from dataclasses import dataclass
#
#
# @dataclass(frozen=True)
# class Constraint:
#     def __init__(self, **kwargs):
#         for key, value in kwargs.items():
#             self.__dict__[key] = value
#
#     def __str__(self):
#         return self.__dict__.__str__()
#
#
# c = Constraint(n=1, b='dsf')
# print(c)
# c.b = 4