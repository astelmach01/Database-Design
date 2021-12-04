def execute_query(cur, query):
    cur.execute(query)
    return cur.fetchall()


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]
