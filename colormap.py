# Copyright (c) 2019, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.
#
# All information contained herein is, and remains the property of Vienna
# University of Technology (TU Wien), Department of Geodesy and Geoinformation
# (GEO). The intellectual and technical concepts contained herein are
# proprietary to Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO). Dissemination of this information or
# reproduction of this material is forbidden unless prior written permission
# is obtained from Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO).

'''
Created On 2019-10-16, last modified
@author: Felix Reuß felix.reuss@geo.tuwien.ac.at
- includes functions from pytesmo package https://github.com/TUW-GEO/pytesmo

Colorella Package: Color organizing and easy to learn laboratory
The packages allows to load color maps from several sources including:
- matplotlib default color maps (e.g viridis, plasma)
- cpt files
- ct files
- json
- or to create new colormaps from dictionaries or lists of colors
classmethods allow the following functions:
- save a newly or modified colormap as .cpt file
- turn a colormap to greyscale (e.g. for printing in greyscale
- reverse a colormap
- view a colormap as plot
- create a list or dictionary object contaning all the colors from a colormap
- adapt a colormao using a function?
- adapt the indices of a colormap
'''''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
import colorsys
import matplotlib.tri as tri
import os
import json
import glob
import warnings

from colorella.utils import cptfile2dict, gdal2dict, json2list

class ColorMap:  # TODO: class names start always with an upper case, e.g. ColorMap
    """create a colormap object compatible with matplotlib
    TODO: implement alpha channel support in load and save method. Should colormap.objects be in place or a new object
        """
    def __init__(self, arg, name='default', cm_dirpath='./colormaps'):
        # TODO: blank between parameter and :
        # TODO: str or list or dict, optional
        """
        Constructor of colormap class.

        Parameters
        ----------
        arg : str, dict, list
            defining the input for the colormap, can be one of the following: Name of a matplotlib colormap, list of RGB values, dict of rgb values, cpt filename, ct filename, json filename
            # TODO: add clear examples how the input should or can look like
        """
        self.arg = arg
        self.dirpath = cm_dirpath
        self._mpl_cm.name = name

        # TODO: the first check must be a matplotlib colormap
        if isinstance(self.arg, matplotlib.colors.LinearSegmentedColormap) or isinstance(self.arg, matplotlib.colors.ListedColormap):
            self._mpl_cm = self.arg

        elif isinstance(self.arg, str):
            for files in os.walk(self.dirpath):
                for file in files:
                    if self.arg in files:
                        self.c_map_name = os.path.splitext(file)[0]
                        self.extension = os.path.splitext(file)[1]

                        if '.cpt' == self.extension:
                            ColorMap.from_cptfile(os.path.join(self.dirpath, file))

                        elif '.ct' == self.extension:
                            ColorMap.from_gdal(os.path.join(self.dirpath, file))

                        elif '.json' == self.extension:
                            ColorMap.from_json(os.path.join(self.dirpath, file))
                    else:
                        continue

        elif self.arg in plt.colormaps():
            self._mpl_cm = cm.get_cmap(self.arg)  # TODO: better variable naming than object? _mpl_cm

        elif isinstance(self.arg, list):
            self._mpl_cm = col.ListedColormap(name=self._mpl_cm.name, colors=self.arg)  # TODO: the name should be self.cm_name

        elif isinstance(self.arg, dict):
            self._mpl_cm = col.LinearSegmentedColormap(name=self._mpl_cm.name, segmentdata=self.arg) # TODO: the name should be self.cm_name

        else:
            # TODO: update error message
            # valid = c.colormaps + c.diverging_black
            txt = "name provided {0} is not recognised or file extension is not supported. ".format(self.arg)
            txt += "\n valid name can be found in colormap.colormap_names"
            txt += "\n supported file extensions are .cpt and .ct"
            raise ValueError(txt)

    @property
    def name(self):
        """
        Returns attribute name
        """
        return self._mpl_cm.name

    def __len__(self):
        """
        Returns number of colors in the colormap
        - for Segmented Colormap: Number of Segments
        - for Listed Colormap: total number of colors
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return len(cmap._object._segmentdata.get('red'))
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return self._mpl_cm.N

    def __getitem__(self, item):
        """
        Returns the xth color of the colormap
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return {'red':cmap_object._segmentdata.get('red')[item], 'green':cmap_object._segmentdata.get('green')[item], 'blue': cmap_object._segmentdata.get('blue')[item], 'alpha': cmap_object._segmentdata.get('alpha')[item]}
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return cmap_object.colors[item]

    def __str__(self):
        """
        Returns a string containing the RGB values of the colormap
        - for Segmented Colormap: Start and end color
        - for a Listed Colormap: all colors
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return str(cmap_object._segmentdata.values())
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return str(cmap_object.colors[0]+cmap_object.colors[-1])

    #TODO name automatically set, or by user?
    def to_gradient(self, name = None, inplace=True):
        """
        Converts a listed Colormap to a Linear Segmented Colormap

        Parameters
        ----------
        outname: str, optional
            filename if the colormap is saved
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            warnings.warn("Colormap is already a Segmented Colormap. Listed Colormap required")
            return self._mpl_cm
        else:
            mpl_cm = col.LinearSegmentedColormap.from_list(name, self._mpl_cm.colors)

        if inplace:
            self._mpl_cm = mpl_cm
            return self
        else:
            return ColorMap(mpl_cm, name=self._mpl_cm.name+'_gradient')


    # TODO: out_filepath mandatory; or out_path and check for file or directory path whats with save_as_json etc?
    def save_as_cpt(self, outname=None, **kwargs):
        """
        Saves a acolormap.object as a .cpt file

        Parameters
        ----------
        outname: str, optional
            outname for the file
        keyword arguments: int
            Vmin, Vmax, N (Number of colorsteps)

        """
        if outname is None:
            outname = self.dirpath+self.name+'.cpt'
        elif '.cpt' not in outname:
            outname = outname+'.cpt'
        vmin=0
        vmax=1
        N=255
        #create string for upper, lower colors
        b = np.array(kwargs.get("B", self._mpl_cm(0.)))
        f = np.array(kwargs.get("F", self._mpl_cm(1.)))
        na = np.array(kwargs.get("N", (0, 0, 0))).astype(float)
        ext = (np.c_[b[:3], f[:3], na[:3]].T * 255).astype(int)
        #Creating footer
        extstr = "B {:3d} {:3d} {:3d}\nF {:3d} {:3d} {:3d}\nN {:3d} {:3d} {:3d}"
        ex = extstr.format(*list(ext.flatten()))
        # create colormap
        colors = (self._mpl_cm(np.linspace(0., 1., N))[:, :3] * 255).astype(int)
        vals = np.linspace(vmin, vmax, N)
        arr = np.c_[vals[:-1], colors[:-1], vals[1:], colors[1:]]

        fmt = "%e %3d %3d %3d %e %3d %3d %3d"

        if not os.path.exists(outname):
            os.makedirs(outname)
        np.savetxt(outname, arr, fmt=fmt,
                   header="# COLOR_MODEL = RGB",
                   footer=ex, comments="")

    # TODO: more detailed documentation
    def convert2greyscale(self, weights = 1, inplace=True):
        """
        Return a grayscale version of the given colormap. Luminanance values are calculated using a dot  product of a weight array and the color array of the object

        Parameters
        ----------
        weights: int
            weights used to convert RGB values to luminance, default =1

        """
        colors = self._mpl_cm(np.arange(self._mpl_cm.N))

        # convert RGB to perceived grayscale luminance
        if weights == 1:
            RGB_weights = [0.2126, 0.7152, 0.0722]
            luminance = np.dot(colors[:, :3], RGB_weights)
        elif weights == 2:
            RGB_weights = [0.299, 0.587, 0.114]
            luminance = np.dot(colors[:, :3], RGB_weights)
        elif weights == 3:
            RGB_weights = [0.299, 0.587, 0.114]
            luminance = np.sqrt(np.dot(colors[:, :3] ** 2, RGB_weights))
        else:
            warnings.warn('Argument weight only supports values between 1 and 3')

        colors[:, :3] = luminance[:, np.newaxis]
        mpl_cm = col.LinearSegmentedColormap.from_list(self.c_map_name + "_grey", colors, self._mpl_cm.N)

        if inplace:
            self._mpl_cm = mpl_cm
            return self
        else:
            return ColorMap(mpl_cm, name=self._mpl_cm.name+'_grey')

    def to_matplotlib(self):
        """
        Returns the matplotlib colormap object"
        """
        return self._mpl_cm

    def to_dict(self):
        """
        Creates a dictionary of colors from a colormap object

        Returns
        -------
        dict object

        """
        if isinstance(self._mpl_cm, col.ListedColormap):
            col_list = self._mpl_cm._lut
            red = []
            green = []
            blue = []
            alpha = []

            for i in range(len(col_list)):
                red.append(col_list[i][0])
                green.append(col_list[i][1])
                blue.append(col_list[i][2])
                alpha.append(col_list[i][3])
            col_dct = {'R': red, 'G': green, 'B': blue, 'A': alpha}
            return col_dct

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return self._mpl_cm._segmentdata

    def to_list(self):
        """
        Creates a list of colors from a colormap object

        Returns
        -------
        List object
        """
        if isinstance(self._mpl_cm, col.ListedColormap):
            col_list = self._mpl_cm._lut
            col_list_tuples = [tuple(l) for l in col_list]
            return col_list_tuples

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            dic_list = []
            for key, value in self._mpl_cm._segmentdata.items():
                temp = [key, value]
                dic_list.append(temp)
            return  dic_list

    def plot(self):
        """
        Shows the colormap as a colorbar in a plot
        """
        colors = self._mpl_cm(np.arange(self._mpl_cm.N))
        plt.imshow([colors], extent=[0, 10, 0, 1])
        plt.axis('off')
        plt.show()

    def reverse(self, inplace=True):
        """
        Reverses a colormap, a.k.a returns the containing colors in reverse direction. Class type remains the same
        """

        if isinstance(self._mpl_cm, col.ListedColormap):
            mpl_cm = col.ListedColormap(self._mpl_cm.colors[::-1])

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            reverse = []
            keys = []

            for key in self._mpl_cm._segmentdata:
                keys.append(key)
                channel = self._mpl_cm._segmentdata[key]
                data = []

                for c in channel:
                    data.append((1 - c[0], c[2], c[1]))
                reverse.append(sorted(data))

            revdict = dict(zip(keys, reverse))
            mpl_cm = mpl.colors.LinearSegmentedColormap(self._mpl_cm, revdict)

        if inplace:
            self._mpl_cm = mpl_cm
            return self._mpl_cm
        else:
            return ColorMap(mpl_cm, name=self._mpl_cm.name + '_reversed')


    def to_gdal(self):
        """
        Converts a Colormap object to a gdal color table
        """
        gdal_ct = gdal.ColorTable()
        if isinstance(self._mpl_cm, col.ListedColormap):
            for i in range(len(self._mpl_cm.colors)):
                gdal_ct.SetColorEntry(i, tuple(int(self._mpl_cm.colors[i][0]*255), int(self._mpl_cm.colors[i][1]*255), int(self._mpl_cm.colors[i][2]*255), 255))
        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            for i in range(0, 256):
                gdal_ct.SetColorEntry(i, tuple(int(self._mpl_cm._segmentdata.get('red')[i]), int(self._mpl_cm._segmentdata.get('green')[i]), int(self._mpl_cm._segmentdata.get('blue')[i], int(self._mpl_cm._segmentdata.get('alpha')[i])))
        return gdal_ct


    @classmethod
    def from_cptfile(cls, filepath):
        name, cptdict = cptfile2dict(filepath)
        return col.LinearSegmentedColormap(name=name, segmentdata=cptdict)

    def from_gdal(cls, filepath):
        name, gdaldict = gdal2dict(filepath)
        return col.LinearSegmentedColormap(name=name, segmentdata=gdaldict)

    def from_json(cls, filepath):
        name, jsonlist = json2list(filepath)
        return col.ListedColormap(name=name, colors=jsonlist)
