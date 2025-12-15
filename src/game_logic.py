LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


def winner(b):
    for a, c, d in LINES:
        s = b[a] + b[c] + b[d]
        if s == 3:
            return 1, (a, c, d)
        if s == -3:
            return -1, (a, c, d)
    return 0, None


def is_draw(b):
    w, _ = winner(b)
    return w == 0 and all(x != 0 for x in b)
