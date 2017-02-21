rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal1 = [x[0]+x[1] for x in zip(rows, cols)]
diagonal2 = [x[0]+x[1] for x in zip(rows, cols[::-1])]
unitlist = row_units + column_units + square_units + [diagonal1] + [diagonal2]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)