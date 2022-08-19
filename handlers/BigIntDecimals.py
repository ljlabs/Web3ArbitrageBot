from decimal import Decimal


class BigIntDecimals:
    def __init__(self, value, decimals):
        self.decimals = decimals
        self.rawValue = value
        self.value = Decimal(value) / Decimal(10 ** self.decimals)

    @property
    def int_value(self):
        return int(Decimal(self.rawValue) // Decimal(10 ** self.decimals))

    @property
    def decimal_value(self):
        return int(Decimal(self.rawValue) % Decimal(10 ** self.decimals))

    def __truediv__(self, other):
        return self.value / other

    def __rtruediv__(self, other):
        return other / self.value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __mul__(self, other):
        return other * self.value

    def __rmul__(self, other):
        return other * self.value

    def __eq__(self, other):
        return other.value == self.value

    def __gt__(self, other):
        if type(other) == type(self):
            return self.value > other.value
        return self.value > other

    def __lt__(self, other):
        if type(other) == type(self):
            return self.value < other.value
        return self.value < other


if __name__ == '__main__':
    a = BigIntDecimals(20, 18)
    a_p = BigIntDecimals(20, 18)
    b = BigIntDecimals(32, 6)
    c = BigIntDecimals(432, 1)
    print(f"Test Div We expect {20e-18 / 32e-6} : {a / b}")
    print(f"Test Add We expect {20e-18 + 32e-6} : {a + b}")
    print(f"Test Sub We expect {20e-18 - 32e-6} : {a - b}")
    print(f"Test Mul We expect {20e-18 * 32e-6} : {a * b}")
    print(f"Test Equal We expect 20e-18 == 20e-18 : {20e-18 == 20e-18} : {a == a_p}")
    print(f"Test Equal We expect 20e-18 == 32e-6 :{20e-18 == 32e-6} : {a == b}")
    print(f"Test > Than We expect {20e-18 > 32e-6} : {a > b}")
    print(f"Test < Than We expect {20e-18 < 32e-6} : {a < b}")
    print(f"Test Int {c.int_value}")
    print(f"Test Decimals {c.decimal_value}")
