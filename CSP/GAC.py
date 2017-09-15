_ROW = 0
_COL = 1


def revise(variable) -> bool:
    initial_number_of_domains = len(variable.domain)
    for domain in variable.domain:
        positive = 0
        for constraint in domain.constraints:
            if constraint(): positive += 1
        if positive == 0:
            # No legal move found for this domain value:
            variable.delete(domain)
    return initial_number_of_domains > len(variable.domain)

def GAC_loop(queue):
    if __name__ == '__main__':
        while queue:
            todo = queue.pop(0)
            if revise(todo):
                if todo.type == _ROW:
                    # Queue up all columns if a row changed
                    # its domain.
                    pass
                else: # todo.type = _COL:
                    # Queue up all rows if a column changed
                    # its domain.
                    pass

                # Domain has changed, do something with children..
                pass # no thank you. no children for me.
