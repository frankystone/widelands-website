#!/usr/bin/env python
# encoding: utf-8

import pydot as d

from widelandslib.tribe import *
#from pudb import set_trace; set_trace()

from os import makedirs, path
import subprocess
from tempfile import mkdtemp

tdir = ""

##############################
# To Do Make_Flow_Diagram.py #
##############################
# i'd like to add things like: forester resores trunk or: gamekeeper restores meat
#
# also, a building called construction site where alle the building material can point at would be nice
#
# how to tell the viewer, how many and wich ressources turn to others via buildings,
# e.g. 6 trunks to 1 coal with the atlanteans, maybe on the edges?

#############################
# Work around bugs in pydot #
#############################
## Pydot can't handle names with - in it. We replace them.

def _cleanup_str(s):
    return s.replace('-', '')

class Subgraph(d.Subgraph):
    def __init__(self, name, *args, **kwargs):
        name = _cleanup_str(name)
        d.Subgraph.__init__(self, name, *args, **kwargs)

class Node(d.Node):
    def __init__(self, name, *args, **kwargs):
        name = _cleanup_str(name)
        d.Node.__init__(self, name, *args, **kwargs)

class Edge(d.Edge):
    def __init__(self, first, second, *args, **kwargs):
        first = _cleanup_str(first)
        second = _cleanup_str(second)
        d.Edge.__init__(self, first, second, *args, **kwargs)

class CleanedDot(d.Dot):
    def get_node(self, name, *args, **kwargs):
        name = _cleanup_str(name)
        return d.Dot.get_node(self, name, *args, **kwargs)

####################
# Begin of drawing #
####################

def add_building(g, b, limit_inputs=None, limit_outputs=None, limit_buildings=None, link_workers=True, limit_recruits=None):
    # Add the nice node
    workers = ""
    if isinstance(b, (ProductionSite,)):
        workers = r"""<table border="0px" cellspacing="0">"""
        for worker in b.workers:
            wo = b.tribe.workers[worker]
            workers += ('<tr><td border="0px"><img src="{w.image}"/></td><td border="0px">{w.descname}</td></tr>'.
                format(w=wo)
            )
            if link_workers:
                add_worker(g, wo)
                g.add_edge(Edge(b.name, wo.name, color="orange", arrowhead="none"))
        for worker in b.recruits:
            if limit_recruits is None or worker in limit_recruits:
                wo = b.tribe.workers[worker]
                add_worker(g, wo, as_recruit=True)
                g.add_edge(Edge(b.name, wo.name, color="darkgreen"))
        workers += r"""</table>"""

    if isinstance(b, (MilitarySite,)):
        workers = r"""<table border="0px" cellspacing="0">"""
        workers += (r"""<tr><td border="0px">Keeps {b.max_soldiers} Soldiers</td></tr>"""
                    r"""<tr><td border="0px">Conquers {b.conquers} fields</td></tr>"""
                    r"""<tr><td border="0px">Heals {b.heal_per_second} HP per second</td></tr>""").format(b=b)
        workers += r"""</table>"""

    costs = r"""<tr><td colspan="2"><table border="0px" cellspacing="0">"""
    for ware, count in b.buildcost.items():
        w = b.tribe.wares[ware]
        costs += ('<tr><td border="0px">{count} x </td><td border="0px"><img src="{w.image}"/></td><td border="0px">{w.descname}</td></tr>'.
                format(w=w, count=count))
    costs += r"""</table></td></tr>"""
    if not b.buildcost:
        costs = ""

    n = Node(b.name,
        shape = "none",
        label = r"""<<TABLE border="1px" cellborder="0px" cellspacing="0px" cellpadding="0px">
<TR><TD><IMG SRC="{b.image}"/></TD>
<TD valign="bottom">{workers}</TD>
</TR>
<TR><TD align="left" colspan="2">{b.descname}</TD></TR>
{costs}
</TABLE>>""".format(b=b, workers=workers, costs=costs).replace('\n',''),
        URL = "../../buildings/{b.name}/".format(b=b),
        fillcolor = "orange",
        style = "filled",
    )

    sg = Subgraph("%s_enhancements" % b.name,
        ordering = "out", rankdir="TB", rank="same")
    if b.enhancement and not b.enhanced_building:
        cb = b
        while cb.enhancement:
            if limit_buildings == None or (cb.name in limit_buildings):
                sg.add_node(Node(_cleanup_str(cb.name)))
                if limit_buildings == None or (cb.enhancement in limit_buildings):
                    g.add_edge(Edge(cb.name, cb.enhancement, color="blue"))
            cb = b.tribe.buildings[cb.enhancement]
        if limit_buildings == None or (cb.name in limit_buildings):
            sg.add_node(Node(_cleanup_str(cb.name)))
        sg.add_node(n)
        g.add_subgraph(sg)
    else:
        g.add_node(n)


    if isinstance(b, (ProductionSite,)):
        # for worker,c in b.workers: 
        #     g.add_edge(Edge(worker, name, color="orange"))

        for output in b.outputs:
            if limit_outputs is None or output in limit_outputs:
                g.add_edge(Edge(b.name, output, color="darkgreen"))

        for input_ in b.inputs:
            if limit_inputs is None or input_ in limit_inputs:
                g.add_edge(Edge(input_, b.name, color="#cd0000"))
    return n


def add_ware(g, w):
    # Add the nice node
    n = Node(w.name,
             shape = "ellipse",
             label = (r"""<<TABLE border="0px">
<TR><TD><IMG SRC="{w.image}"/></TD></TR>
<TR><TD>{w.descname}</TD></TR>
</TABLE>>""").format(w=w),
             URL = "../../wares/{warename}/".format(warename=w.name),
             fillcolor = "#dddddd",
             style="filled",
)

    g.add_node(n)

def add_worker(g, w, as_recruit=False):
    # Add the nice node
    n = Node(w.name,
            shape = "octagon" if not as_recruit else "ellipse",
            label = (r"""<<TABLE border="0px">
<TR><TD><IMG SRC="{w.image}"/></TD>
<TD>{w.descname}</TD></TR>
</TABLE>>""").format(w=w),
            URL="../../workers/{w.name}/".format(w=w),
            style="filled",
        )

    g.add_node(n)


def make_graph(tribe_name):
    global tdir
    tdir = mkdtemp(prefix="widelands-help")
    t = Tribe(tribe_name)

    g = CleanedDot(concentrate="false", style="filled", bgcolor="white",
                overlap="false", splines="true", rankdir="LR")

    for name,w in t.wares.items():
        add_ware(g, w)
    #
    # for name,w in t.workers.items():
    #     add_worker(g, w)

    for name,b in t.buildings.items():
        add_building(g, b, link_workers=False)


    g.write_pdf(path.join(tdir, "%s.pdf" % tribe_name))

    g.set_size("6")
    g.write_gif(path.join(tdir, "%s.gif" % tribe_name))

    rtdir, tdir = tdir, ""
    return rtdir

def make_building_graph(t, building_name):
    if isinstance(t, basestring):
        t = Tribe(t)

    b = t.buildings[building_name]

    g = CleanedDot(concentrate="false", bgcolor="transparent",
                overlap="false", splines="true", rankdir="LR")

    if not isinstance(b, (ProductionSite,)):
        inputs, outputs = [], []
    else:
        # TODO: prepare for tribes having buildings with a ware as both input and output.
        inputs, outputs = [[t.wares[name] for name in lst] for lst in [b.inputs, b.outputs]]

    # find the uppermost building in the enhancement hierarchy
    bb = b
    while bb.base_building:
        bb = bb.base_building
        add_building(g, bb, limit_inputs=[], limit_outputs=[], link_workers=False)

    add_building(g, b)

    bb = b
    while bb.enhancement:
        bb = t.buildings[bb.enhancement]
        add_building(g, bb, limit_inputs=[], limit_outputs=[], link_workers=False)

    [add_ware(g, w) for w in inputs + outputs]

    try: makedirs(path.join(tdir, "help/{tribename}/buildings/{building_name}/".format(tribename=t.name, building_name=building_name)))
    except: pass
    g.write(path.join(tdir, "help/{tribename}/buildings/{building_name}/source.dot".format(tribename=t.name, building_name=building_name)))

def make_worker_graph(t, worker_name):
    if isinstance(t, basestring):
        t = Tribe(t)

    w = t.workers[worker_name]

    g = CleanedDot(concentrate="false", bgcolor="transparent",
                overlap="false", splines="true", rankdir="LR")

    buildings = [bld for bld in t.buildings.values() if 
            isinstance(bld, ProductionSite) and 
              (w.name in bld.workers or w.name in bld.recruits)]

    for bld in buildings:
        add_building(g, bld, limit_inputs=[], limit_outputs=[], limit_buildings=[buildings], link_workers=False, limit_recruits=[w.name])
        if w.name in bld.workers:
            g.add_edge(Edge(bld.name, w.name, color="orange", arrowhead="none"))

    sg = Subgraph("%s_enhancements" % w.name,
        ordering = "out", rankdir="TB", rank="same")
    # find exactly one level of enhancement
    for other in t.workers.values():
        if other.becomes == w.name:
            add_worker(sg, other)
            g.add_edge(Edge(other.name, w.name, color="blue"))
        elif w.becomes == other.name:
            add_worker(sg, other)
            g.add_edge(Edge(w.name, other.name, color="blue"))

    add_worker(sg, w)
    g.add_subgraph(sg)

    try: makedirs(path.join(tdir, "help/{tribename}/workers/{workername}/".format(tribename=t.name, workername=w.name)))
    except OSError: pass
    g.write(path.join(tdir, "help/{tribename}/workers/{workername}/source.dot".format(tribename=t.name, workername=w.name)))

def make_ware_graph(t, ware_name):
    if isinstance(t, basestring):
        t = Tribe(t)
    w = t.wares[ware_name]

    g = CleanedDot(concentrate="false", bgcolor="transparent",
                overlap="false", splines="true", rankdir="LR")

    buildings = [bld for bld in t.buildings.values() if isinstance(bld, (ProductionSite, )) and (w.name in bld.inputs or w.name in bld.outputs)]
    [add_building(g, bld, limit_inputs=[w.name], limit_outputs=[w.name], limit_buildings=[b.name for b in buildings], link_workers=False) for bld in buildings]

    add_ware(g, w)

    try: makedirs(path.join(tdir, "help/{tribename}/wares/{warename}/".format(tribename=t.name, warename=ware_name)))
    except OSError: pass
    g.write(path.join(tdir, "help/{tribename}/wares/{warename}/source.dot".format(tribename=t.name, warename=ware_name)))

def process_dotfile(directory):
    subprocess.Popen("dot -Tpng -o {dir}/image.png -Tcmapx -o {dir}/map.map {dir}/source.dot".format(dir=directory).split(" ")).wait()
    #with open(directory,"w") as html:
    #    html.write(r"""<IMG SRC="image.png" border="0px" usemap="#G"/>""" + open(path.join(directory, "map.map")).read())

def make_all_subgraphs(t):
    global tdir
    tdir = mkdtemp(prefix="widelands-help")
    if isinstance(t, basestring):
        t = Tribe(t)
    print "making all subgraphs for tribe", t.name, "in", tdir

    print "  making workers"

    for w in t.workers:
        print "    " + w
        make_worker_graph(t, w)
        process_dotfile(path.join(tdir, "help/{tribename}/workers/{workername}/".format(tribename=t.name, workername=w)))

    print "  making wares"

    for w in t.wares:
        print "    " + w
        make_ware_graph(t, w)
        process_dotfile(path.join(tdir, "help/{tribename}/wares/{warename}/".format(tribename=t.name, warename=w)))

    print "  making buildings"

    for b in t.buildings:
        print "    " + b
        make_building_graph(t, b)
        process_dotfile(path.join(tdir, "help/{tribename}/buildings/{buildingname}/".format(tribename=t.name, buildingname=b)))

    rtdir, tdir = tdir, ""
    return rtdir

def add_bases(tribe, building, g):
    if b.enhanced_building:
        add_building()

if __name__ == "__main__":
    make_all_subgraphs()
