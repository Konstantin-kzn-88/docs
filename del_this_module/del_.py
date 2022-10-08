CONST = 2

class my_pow:
    def __init__(self, var: int):
        self.var = var
    def var_in_pow(self):
        return pow(self.var, CONST)
