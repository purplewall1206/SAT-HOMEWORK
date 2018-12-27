from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
import requests

with PyCallGraph(output=GraphvizOutput()):
    r = requests.get('http://www.baidu.com')