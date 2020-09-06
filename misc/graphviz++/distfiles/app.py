#!/usr/bin/env python3
import flask
from dotmerger import merge

app = flask.Flask(__name__)

SAMPLE_1 = '''
digraph g1 {
  subgraph cluster_0 {
    style=filled;
    color=lightgrey;
    node [style=filled, color=white];
    a0 -> a1 -> a2 -> a3;
  }
  start -> a0;
  a3 -> end;
  a1 -> b3;
  a3 -> a0;
  start [shape=doublecircle];
  end [shape=doublecircle];
}
'''.strip()
SAMPLE_2 = '''
digraph g2 {
  subgraph cluster_01{
    node [style=filled];
    b0 -> b1 -> b2 -> b3;
    color=blue;
  }
  start -> b0;
  b3 -> end;
  b2 -> a3;
  start [shape=Mdiamond]; // Definitions in the second graph will be prior
  end [shape=Msquare];
}
'''.strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    g1 = flask.request.form.get('g1', None)
    g2 = flask.request.form.get('g2', None)
    r = e = None

    if g1 is None and g2 is None:
        g1 = SAMPLE_1
        g2 = SAMPLE_2
    elif g1 is not None and g2 is not None:
        try:
            r, e = merge(g1, g2)
        except:
            e = 'Error: Unhandled exception'
    else:
        if g1 is None: g1 = ''
        if g2 is None: g2 = ''

    return flask.render_template('index.html', g1=g1, g2=g2, r=r, e=e)

if __name__ == '__main__':
    app.run(
        debug = False,
        host = '0.0.0.0',
        port = 10001,
        threaded = True
    )
