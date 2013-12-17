import matplotlib.pyplot as plt
from itertools import groupby
from operator import itemgetter
from copy import deepcopy
import sys
from .geom import geom
from numpy import asarray

class geom_linerange(geom):
    VALID_AES = ['x', 'ymin', 'ymax', 'color', 'alpha', 'group', 'linestyle', 'linewidth' 'label', 'size']
    def plot_layer(self, layer):
        # select out valid arguments for this geom
        layer = {k: v for k, v in layer.items() if k in self.VALID_AES}
        layer.update(self.manual_aes)
        if 'x' in layer:
            x = layer.pop('x')
        ymin = asarray(layer.pop('ymin'))
        ymax = asarray(layer.pop('ymax'))
        y = (ymax+ymin) / 2
        ymin = y-ymin
        ymax = ymax-y
        if 'size' in layer:
            # ggplot also supports aes(size=...) but the current mathplotlib is not. See 
            # https://github.com/matplotlib/matplotlib/issues/2658
            if isinstance(layer['size'], list):
                layer['size'] = 4
                msg = "'geom_line()' currenty does not support the mapping of " +\
                      "size ('aes(size=<var>'), using size=4 as a replacement.\n" +\
                      "Use 'geom_line(size=x)' to set the size for the whole line.\n"
                sys.stderr.write(msg)
            layer['linewidth'] = layer['size']
            del layer['size']
        if 'linestyle' in layer and 'color' not in layer:
            layer['color'] = 'k'
        if 'group' not in layer:
            plt.errorbar(x, y, yerr=[ymin, ymax], fmt=' ', capsize=0, **layer)
        else:
            g = layer.pop('group')
            for k, v in groupby(sorted(zip(x, y, ymin, ymax, g), key=itemgetter(4)), key=itemgetter(4)):
                x_g, y_g, ymin_g, ymax_g, _ = zip(*v)
                plt.errorbar(x_g, y_g, yerr=[ymin_g, ymax_g], fmt=' ', capsize=0, **layer)
