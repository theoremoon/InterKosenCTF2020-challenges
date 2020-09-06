import subprocess
import tempfile
import json

def dotit(g, outfmt):
    """ Convert DOT to JSON """
    assert outfmt in ['json', 'svg']
    p = subprocess.Popen(["dot", "-T{}".format(outfmt)],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.stdin.write(g.encode())
    p.stdin.close()
    try:
        p.wait(timeout=1)
    except subprocess.TimeoutExpired:
        return None, "Error: dot timeout"

    if p.returncode != 0:
        return None, p.stderr.read().decode().strip()

    return p.stdout.read(), None

def m4it(m4):
    p = subprocess.Popen(["m4"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    p.stdin.write(m4.encode())
    p.stdin.close()
    try:
        p.wait(timeout=1)
    except subprocess.TimeoutExpired:
        return None, "Error: m4 timeout"

    if p.returncode != 0:
        return None, p.stderr.read().decode().strip()

    r = p.stdout.read().decode()
    return dotit(r, 'svg')

def listup_nodes(d):
    return set([obj['name'] for obj in d['objects']])

def merge(g1, g2):
    """ Merge 2 graphs """
    m4 = (
        "digraph merged {{\n"
        "define(`digraph', `subgraph')"
        "define(`{graph1}', `sub_{graph1}')"
        "include(`{file1}')"
        "define(`{graph2}', `sub_{graph2}')"
        "include(`{file2}')"
        "}}\n"
    )

    # convert DOT to JSON
    o1, e = dotit(g1, 'json')
    if e is not None:
        return None, e
    d1 = json.loads(o1)

    o2, e = dotit(g2, 'json')
    if e is not None:
        return None, e
    d2 = json.loads(o2)

    # check for intersection
    if len(listup_nodes(d1).intersection(listup_nodes(d2))) == 0:
        return None, "Error: Two graphs are independent (No intersection found)"

    # create and merge dot files
    with tempfile.NamedTemporaryFile() as f1, tempfile.NamedTemporaryFile() as f2:
        f1.write(g1.encode())
        f1.flush()
        f2.write(g2.encode())
        f2.flush()
        r, e = m4it(m4.format(
            graph1 = d1['name'],
            graph2 = d2['name'],
            file1 = f1.name,
            file2 = f2.name
        ))

    if e is None:
        return r.decode(), None
    else:
        return None, e.decode()
