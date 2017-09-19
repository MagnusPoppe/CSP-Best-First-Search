

def constraint_factory(x, xi, xc, xt, y, yi, yc, yt):
    """ Creates a constraint based on variables given: """
    def intersection():
        expression = (xt != yt) and ( ( (y <= xi) and (xi < y + yc) ) and ((x <= yi) and (yi < x + xc)) )
        expression_part_1 = (xt != yt)
        expression_part_2 = (y <= xi) and (xi < y + yc)
        expression_part_4 = (x <= yi) and (yi < x + xc)
        return expression

    def space_inbetween():
        expression = xt == yt and x + xc < y
        return expression

    if xt == yt:
        return space_inbetween
    else:
        return intersection

def revise(m, n):
    initial_domain = len(m.domain)
    was = str(m)
    for mx in m.domain:
        constraints = []

        for nx in n.domain:
            constraints.append(
                constraint_factory(
                    mx, m.index, m.constant, m.type,
                    nx, n.index, n.constant, n.type
                )
            )

        # Hvis det eksisterer en constraint som tilfredstilles, ikke endre domene.
        if any([ constraint() for constraint in constraints] ): continue
        else: m.domain.remove(mx)

    _is = str(m)
    return len(m.domain) == initial_domain

def GAC( queue ):

    seen = []
    while queue:
        x1, x2 = queue.pop(0)
        if len(x1.domain) == 0:
            return False

        if revise(x1, x2):
            for node1, node2 in seen:
                if node2 == x1: queue.append((node1, node2))

        seen.append((x1,x2))
    return True