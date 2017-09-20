

def constraint_factory(x, xi, xc, xt, y, yi, yc, yt):
    """ Creates a constraint based on variables given: """
    def intersection():
        expression = (xt != yt) and ((x <= yi) and (yi < x + xc))  and (  (y <= xi) and (xi < y + yc) )
        return expression

    def space_inbetween():
        # debug = str(x+xc) + " < " + str(y)
        expression = xt == yt and x + xc < y
        return expression

    if xt == yt:
        return space_inbetween
    else:
        return intersection

def revise(m, n):
    initial_domain = len(m.domain)
    for mx in m.domain:
        remove = True
        for nx in n.domain:
            constraint = constraint_factory(mx, m.index, m.constant, m.type, nx, n.index, n.constant, n.type)
            if constraint():
                dont_remove=False
                break
        if remove:
            m.domain.remove(mx)
            break

        # Hvis det eksisterer en constraint som tilfredstilles, ikke endre domene.
        # if all([ not constraint() for constraint in constraints ] ):
        #     m.domain.remove(mx)

    return len(m.domain) != initial_domain

# def revise(m, n):
#     initial_domain = len(m.domain)
#     for nx in n.domain:
#         constraint = constraint_factory(m.domain[0], m.index, m.constant, m.type, nx, n.index, n.constant, n.type)
#         if constraint(): return False
#
#     m.domain.remove(m.domain[0])
#     return len(m.domain) != initial_domain


def GAC( queue: list ) -> bool :

    seen = []
    while queue:
        x1, x2 = queue.pop(0)
        if revise(x1, x2):
            if len(x1.domain) == 0: return False
            for node1, node2 in seen:
                # if node2 == x1 or node1 == x1: queue.append((node1, node2))
                if node2 == x1: queue.append((node1, node2))

        seen.append((x1,x2))
    return True