class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.result = {}
        self.count = 0

    def is_consistent(self, variable, assignment):
        for neighbor in self.constraints[variable]:
            if neighbor in assignment:
                f = self.constraints[variable][neighbor]
                if not f(assignment[variable], assignment[neighbor]):
                    return False
        return True

    def dfs_search(self, k):
        if k == len(self.variables):
            self.count += 1
            print(self.count, self.result)
            return

        var = self.variables[k]
        for val in self.domains[var]:
            self.result[var] = val
            if self.is_consistent(var, self.result):
                self.dfs_search(k + 1)
        if var in self.result:
            del self.result[var]


def create_knight_csp(n, k):
    variables = [f'k{i}' for i in range(k)]
    positions = [(i, j) for i in range(n) for j in range(n)]

    domains = {}
    for v in variables:
        domains[v] = positions.copy()

    constraints = {v: {} for v in variables}

    def knight_attack(a, b):
        if a == b:
            return False
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return not ((dx == 1 and dy == 2) or (dx == 2 and dy == 1))

    for v1 in variables:
        for v2 in variables:
            if v1 != v2:
                constraints[v1][v2] = knight_attack

    return CSP(variables, domains, constraints)


# ======================
# 4x4棋盘，放6个骑士
# ======================
csp = create_knight_csp(4, 6)
csp.dfs_search(0)
print("最终正确解数：", csp.count)