from CSP._old.CSP import CSP


def revise(constraint, xi, xj) -> bool:
    """
    PSEUDO CODE FROM THE BOOK, ARTIFICIAL INTELLIGENCE, A MODERN APPROACH:
    Section 6.3 page 209

    function REVISE(csp, Xi, Xj) returns true if we revise the domain of Xi revised ← false
        for each x in Di do
            if no value y in Dj allows (x,y) to satisfy the constraint between Xi and Xj then
                delete x from Di
                revised ← true
        return revised

    """
    pass



##########
# SÅ VIDT JEG FORSTÅR:
# Man queuer alle variabler med fulle domener. Målet med algoritmen er å gjøre domenene mindre.
# Alle domener må dermed sammenliknes med andre for å finne mulige feil i domenene. på denne
# måten skal man klare å gjøre domenene til størrelse 1
#
# Det skal kun være mulig å ha et valg per domene.
#
# Når det er kun en verdi igjen i domenet for alle variabler er løsningen funnet.

# Revise algoritmen skal gjøre denne sammenlikningen for å finne de ulovlige verdiene i
# domenet.
##########

dummy_constraint = lambda current, size, next: \
        current + size < next + 1


def arc_consistancy(queue: list):
    """
    PSEUDO CODE FROM THE BOOK, ARTIFICIAL INTELLIGENCE, A MODERN APPROACH:
    Section 6.3 page 209

    function AC-3(csp) returns false if an inconsistency is found and true otherwise inputs: csp, a binary CSP with components (X, D, C)
        local variables: queue, a queue of arcs, initially all the arcs in csp
        while queue is not empty do
            (Xi, Xj)←REMOVE-FIRST(queue)
            if REVISE(csp, Xi, Xj) then
                if size of Di = 0 then return false
                    for each Xk in Xi.NEIGHBORS - {Xj} do
                        add (Xk, Xi) to queue
        return true
    """
    pass
    # while queue:
    #     xi = queue.pop(0) # type: CSP
    #     xj = queue.pop(1) # type: CSP
    #     if not revise(dummy_constraint, xi, xj):
    #         if len(xi.d) == 0: return False
    #             # add_children...
    #
    # return True


