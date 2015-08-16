from docutils.parsers.rst import directives, Directive
from docutils import nodes
from pelican import signals
import os

def register():
    directives.register_directive("plot", Plot)


class Plot(Directive):
    """
    Class to handle plot directive.
    
    Each directive takes in 2 required arguments:
        - key:   the name of the .js/html file
        - title: title for the graph
        - 
    """
    required_arguments = 2
    optional_arguments = 2
    option_spec = {
        'dir': directives.unchanged,
        'jsSubDir': directives.unchanged,

    }

    final_argument_whitespace = True
    has_content = False


    def run(self):
        key = self.arguments[0].strip()
        title = (' ').join(self.arguments[1:])
        directory = self.options.get('dir', '')
        jsSubDir = self.options.get("jsSubDir", 'javascripts')

        #make sure we only use /.
        #user may have entered path using \ or \\, but these will make FireFox freak
        js_file = os.path.join(directory, jsSubDir,key).replace("\\","/")+".js"
        html_file = os.path.join(directory, key).replace("\\","/")+".html"

        div_container = "<div class = 'plotContainer'>"
        title = "<h4 class='text-center'><a href = '{0}'>{1}</a></h4>".format(html_file, title)
        plot_div = "<div class ='plot' id='{0}''>".format(key)
        svg= "<svg></svg>"
        script_tag = "<script src='{0}''></script>".format(js_file)

        return [
            nodes.raw('', div_container, format='html'),
            nodes.raw('',title,format='html'),
            nodes.raw('', plot_div, format='html'),
            nodes.raw('', svg, format='html'),
            nodes.raw('',script_tag, format='html'),
            nodes.raw('', '</div>', format='html'),
            nodes.raw('','</div>',format='html')
            ]