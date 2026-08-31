class CalculateWACC:
    """
    Calculate the Weighted Average Cost of Capital

    Attributes:
        coe: The cost of equity of the company
        cod: The cost of debt of the company
        g: The gearing ratio of the company
        t: The company tax rate
    """

    def __init__(self, coe: float, cod: float, g: float, t: float=0.3):
        self.coe = coe
        self.cod = cod
        self.g = g
        self.t = t

    def pre_tax(self) -> float:
        return self.g * self.cod + 1 / (1 - self.t) * self.coe * (1 - self.g)

    def vanilla(self) -> float:
        return self.g * self.cod + self.coe * (1 - self.g)

    def post_tax(self) -> float:
        return (1 - self.t) * self.g * self.cod + self.coe * (1 - self.g)
