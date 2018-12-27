

import tempfile
import os
import textwrap

from ..metadata import __version__
from ..exceptions import PyCallGraphException
from ..color import Color
from .output import Output


class GraphvizOutput(Output):

    def __init__(self, **kwargs):
        self.tool = 'dot'
        self.output_file = 'pycallgraph.png'
        self.output_type = 'png'
        self.font_name = 'Verdana'
        self.font_size = 7
        self.group_font_size = 10
        self.group_border_color = Color(0, 0, 0, 0.8)

        Output.__init__(self, **kwargs)

        self.prepare_graph_attributes()

    @classmethod
    def add_arguments(cls, subparsers, parent_parser, usage):
        defaults = cls()

        subparser = subparsers.add_parser(
            'graphviz', help='Graphviz generation',
            parents=[parent_parser], usage=usage,
        )

        subparser.add_argument(
            '-l', '--tool', dest='tool', default=defaults.tool,
            help='The tool from Graphviz to use, e.g. dot, neato, etc.',
        )

        cls.add_output_file(
            subparser, defaults, 'The generated Graphviz file'
        )

        subparser.add_argument(
            '-f', '--output-format', type=str, default=defaults.output_type,
            help='Image format to produce, e.g. png, ps, dot, etc. '
            'See http://www.graphviz.org/doc/info/output.html for more.',
        )

        subparser.add_argument(
            '--font-name', type=str, default=defaults.font_name,
            help='Name of the font to be used',
        )

        subparser.add_argument(
            '--font-size', type=int, default=defaults.font_size,
            help='Size of the font to be used',
        )

    def sanity_check(self):
        self.ensure_binary(self.tool)

    def prepare_graph_attributes(self):
        generated_message = '\\n'.join([
            r'Generated by Python Call Graph v%s' % __version__,
            r'http://pycallgraph.slowchop.com',
        ])

        self.graph_attributes = {
            'graph': {
                'overlap': 'scalexy',
                'fontname': self.font_name,
                'fontsize': self.font_size,
                'fontcolor': Color(0, 0, 0, 0.5).rgba_web(),
                'label': generated_message,
            },
            'node': {
                'fontname': self.font_name,
                'fontsize': self.font_size,
                'fontcolor': Color(0, 0, 0).rgba_web(),
                'style': 'filled',
                'shape': 'rect',
            },
            'edge': {
                'fontname': self.font_name,
                'fontsize': self.font_size,
                'fontcolor': Color(0, 0, 0).rgba_web(),
            }
        }

    def done(self):
        source = self.generate()

        self.debug(source)

#simple version of output dot
        source_simple = self.generate1()
        self.debug(source_simple)
        #print(source_simple)
        import time
        filename = '/home/ppw/Documents/pycode/requests_dot/'+str(time.strftime('%d-%H-%M-%S',time.localtime(time.time()))+str('.dot'))
        with open(filename, 'w') as reqfile:
            reqfile.write(source_simple)

        fd, temp_name = tempfile.mkstemp()
        #print(str(fd)+"  "+str(temp_name))
        with os.fdopen(fd, 'w') as f:
            f.write(source)

        cmd = '{} -T{} -o{} {}'.format(
            self.tool, self.output_type, self.output_file, temp_name
        )

        self.verbose('Executing: {}'.format(cmd))
        try:
            ret = os.system(cmd)
            if ret:
                raise PyCallGraphException(
                    'The command "%(cmd)s" failed with error '
                    'code %(ret)i.' % locals())
        finally:
            os.unlink(temp_name)

        self.verbose('Generated {} with {} nodes.'.format(
            self.output_file, len(self.processor.func_count),
        ))

    def generate(self):
        '''Returns a string with the contents of a DOT file for Graphviz to
        parse.
        '''
        indent_join = '\n' + ' ' * 12

        return textwrap.dedent('''\
        digraph G {{

            // Attributes
            {}

            // Groups
            {}

            // Nodes
            {}

            // Edges
            {}

        }}
        '''.format(
            indent_join.join(self.generate_attributes()),
            indent_join.join(self.generate_groups()),
            indent_join.join(self.generate_nodes()),
            indent_join.join(self.generate_edges()),
        ))



    def attrs_from_dict(self, d):
        output = []
        for attr, val in d.items():
            output.append('%s = "%s"' % (attr, val))
        return ', '.join(output)

    def node(self, key, attr):
        return '"{}" [{}];'.format(
            key, self.attrs_from_dict(attr),
        )

    def edge(self, edge, attr):
        return '"{0.src_func}" -> "{0.dst_func}" [{1}];'.format(
            edge, self.attrs_from_dict(attr),
        )

    def generate_attributes(self):
        output = []
        for section, attrs in self.graph_attributes.items():
            output.append('{} [ {} ];'.format(
                section, self.attrs_from_dict(attrs),
            ))
        return output

    def generate_groups(self):
        if not self.processor.config.groups:
            return ''

        output = []
        for group, nodes in self.processor.groups():
            funcs = [node.name for node in nodes]
            funcs = '" "'.join(funcs)
            group_color = self.group_border_color.rgba_web()
            group_font_size = self.group_font_size
            output.append(
                'subgraph "cluster_{group}" {{ '
                '"{funcs}"; '
                'label = "{group}"; '
                'fontsize = "{group_font_size}"; '
                'fontcolor = "black"; '
                'style = "bold"; '
                'color="{group_color}"; }}'.format(**locals()))
        return output

    def generate_nodes(self):
        output = []
        for node in self.processor.nodes():
            attr = {
                'color': self.node_color_func(node).rgba_web(),
                'label': self.node_label_func(node),
            }
            output.append(self.node(node.name, attr))

        return output

    def generate_edges(self):
        output = []

        for edge in self.processor.edges():
            attr = {
                'color': self.edge_color_func(edge).rgba_web(),
                'label': self.edge_label_func(edge),
            }
            output.append(self.edge(edge, attr))

        return output


#======================code edit=============================

    def generate1(self):
        indent_join = '\n' + ' ' * 12
        return textwrap.dedent('''\
        digraph G {{
        
            // Nodes
            {}

            // Edges
            {}

        }}
        '''.format(
            #indent_join.join(self.generate_attributes()),
            #indent_join.join(self.generate_groups()),
            indent_join.join(self.generate_nodes1()),
            indent_join.join(self.generate_edges1()),
        ))

    def edge1(self, edge):
        return '"{0.src_func}" -> "{0.dst_func}";'.format(
            edge
        )

    def node1(self, key):
        return '"{}";'.format(
            key
        )

    def generate_nodes1(self):
        output = []
        for node in self.processor.nodes():

            output.append(self.node1(node.name))

        return output

    def generate_edges1(self):
        output = []

        for edge in self.processor.edges():
            attr = {
                'color': self.edge_color_func(edge).rgba_web(),
                'label': self.edge_label_func(edge),
            }
            output.append(self.edge1(edge))

        return output