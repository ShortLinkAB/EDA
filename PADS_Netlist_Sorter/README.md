This tool is intended to be used when comparing PADS netlists.

It parses a PADS netlist, orders all the nets by connected nodes and creates an output file with the sorted netlist.
Everything not in the \*NET\* part of the netlist file is ignored.

By running this tool on two netlists, the two output files can be compared even if the order of the nets or the names of the nets are different: the intention is to compare the connected nodes.

By using the diff tool Eskil, it is also possible to use some clever regexp preprocessing to further reduce false errors (e.g. ignoring the order of pin 1 and 2 of a resistor).

Usage: 

``python PADS_Netlist_Sorter.py InputNetlist.net`` will process the file InputNetlist.net and create ``sorted_InputNetlist.net`` in the same folder.
