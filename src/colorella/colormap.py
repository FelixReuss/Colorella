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
import os
import glob
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
from osgeo import gdal
import warnings

from src.colorella.utils import cptfile2dict, gdal2dict, json2list


class ColorMap:
    """create a colormap object compatible with matplotlib
        """

    def __init__(self, arg, cm_dirpath='./colormaps', name=None):
        """
        Constructor of colormap class.

        Parameters
        ----------
        arg : str, dict, list
            defining the input for the colormap, can be one of the following: Name of a matplotlib colormap, list of RGB values, dict of rgb values, cpt filename, ct filename, json filename
        """
        self.arg = arg
        self.dirpath = cm_dirpath

        if isinstance(self.arg, col.LinearSegmentedColormap) or isinstance(self.arg, col.ListedColormap):
            self._mpl_cm = self.arg
            if name:
                self._mpl_cm.name = name
        elif isinstance(self.arg, str) and self.arg in plt.colormaps():
            self._mpl_cm = cm.get_cmap(self.arg)
            if name:
                self._mpl_cm.name = name
        elif isinstance(self.arg, str):
            self._mpl_cm = ColorMap.from_cm_directory(self.arg, self.dirpath)
            if name:
                self._mpl_cm.name = name
        else:
            txt = "Input provided {0} is not recognised".format(
                self.arg)
            txt += "\n Input String has to be either a Matplotlib Colormap Name or a file name in the default colormap directory"
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
            return len(self._mpl_cm._segmentdata.get('red'))
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return self._mpl_cm.N

    def __getitem__(self, item):
        """
        Returns the xth color of the colormap
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return {'red':self._mpl_cm._segmentdata.get('red')[item], 'green':self._mpl_cm._segmentdata.get('green')[item], 'blue': self._mpl_cm._segmentdata.get('blue')[item], 'alpha': self._mpl_cm._segmentdata.get('alpha')[item]}
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return self._mpl_cm.colors[item]

    def __str__(self):
        """
        Returns a string containing the RGB values of the colormap
        - for Segmented Colormap: Start and end color
        - for a Listed Colormap: all colors
        """
        if isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            return str(self._mpl_cm._segmentdata.values())
        elif isinstance(self._mpl_cm, col.ListedColormap):
            return str(self._mpl_cm.colors[0]+self._mpl_cm.colors[-1])

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
        # Creating footer
        extstr = "B {:3d} {:3d} {:3d}\nF {:3d} {:3d} {:3d}\nN {:3d} {:3d} {:3d}"
        footer = extstr.format(*list(ext.flatten()))
        # create colormap
        colors = (self._mpl_cm(np.linspace(0., 1., N))[:, :3] * 255).astype(int)
        vals = np.linspace(vmin, vmax, N)
        col_arr = np.c_[vals[:-1], colors[:-1], vals[1:], colors[1:]]

        fmt = "%e %3d %3d %3d %e %3d %3d %3d"

        if not os.path.exists(outname):
            os.makedirs(outname)
        np.savetxt(outname, col_arr, fmt=fmt,
                   header="# COLOR_MODEL = RGB",
                   footer=footer, comments="")

    def save_as_ct(self, outname=None):
        """
        Saves a acolormap.object as a gdal .ct file

        Parameters
        ----------
        outname: str, optional
            outname for the file
        """
        if outname is None:
            outname = self.dirpath+self.name+'.ct'
        elif '.ct' not in outname:
            outname = outname+'.ct'

        arr = np.zeros((255, 3))

        if isinstance(self._mpl_cm, col.ListedColormap):
            for i in range(len(self._mpl_cm.colors)):
                arr[i, :] = [int(self._mpl_cm.colors[i][0] * 255), int(self._mpl_cm.colors[i][1] * 255),
                                          int(self._mpl_cm.colors[i][2] * 255)]
        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            colors = (self._mpl_cm(np.linspace(0., 1., 255))[:, :3] * 255).astype(int)
            for i in range(len(colors)):
                arr[i, :] = [colors[i][0], colors[i][1], colors[i][2]]

        if not os.path.exists(outname):
            os.makedirs(outname)
        np.savetxt(outname, arr)

    def convert2greyscale(self, weights=1, inplace=True):
        """
        Return a grayscale version of the given colormap. Luminanance values are calculated using a dot  product of a weight array and the color array of the object

        Parameters
        ----------
        weights: int
            weights used to convert RGB values to luminance, default =1

        """
        colors = self._mpl_cm(np.arange(self._mpl_cm.N))

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
        mpl_cm = col.LinearSegmentedColormap.from_list(self._mpl_cm.name +'_grey', colors, self._mpl_cm.N)

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
            return self._mpl_cm.colors

        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            dic_list = []
            for key, value in self._mpl_cm._segmentdata.items():
                temp = [key, value]
                dic_list.append(temp)
            return  dic_list

    def view(self):
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
                gdal_ct.SetColorEntry(i, (int(self._mpl_cm.colors[i][0]*255), int(self._mpl_cm.colors[i][1]*255), int(self._mpl_cm.colors[i][2]*255), 255))
        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            colors = (self._mpl_cm(np.linspace(0., 1., 255))[:, :3] * 255).astype(int)
            for i in range(len(colors)):
                gdal_ct.SetColorEntry(i,
                                      (int(colors[i][0]), int(colors[i][1]),
                                            int(colors[i][2]), 255))
        return gdal_ct

    def from_gdal(self):
        """
        Converts a gdal Colortable to a matplotlib colormap
        """
        mpl_arr = [[self.GetColorEntry[x][0] / 255.0, self.GetColorEntry[x][1] / 255.0, self.GetColorEntry[x][0] / 255.0] for x in self.GetCount()]
        mpl_cmap = ColorMap.from_list(mpl_arr)
        return mpl_cmap


    @classmethod
    def from_cm_directory(cls, cm_name, dirpath):
        """
        Checks if given Input string matches with any file in the given directory. In case classmthod from_file is called

        Parameters:
        ----------
        cm_name: str
            name of the colormap file to be opened

        Returns
        ---------
        colormap object
        """
        for filepath in glob.glob(dirpath):
            if cm_name in filepath:
                return cls.from_file(filepath)

    @classmethod
    def from_file(cls, filepath, name=None):
        """
        Function to open colormap objects from .cpt, .ct, .json files

        Parameters:
        ----------
        filepath: str
            path and filename of the colormap to be opened

        Returns
        ---------
        colormap object
        """

        mpl_cm = None
        extension = os.path.splitext(filepath)[1]
        if '.cpt' == extension:
            _, cptdict = cptfile2dict(filepath)
            mpl_cm = col.LinearSegmentedColormap(name=name, segmentdata=cptdict)
        elif '.ct' == extension:
            _, gdaldict = gdal2dict(filepath)
            mpl_cm = col.LinearSegmentedColormap(name=name, segmentdata=gdaldict)
        elif '.json' == extension:
            _, jsonlist = json2list(filepath)
            mpl_cm = col.ListedColormap(jsonlist, name=name)
        else:
            raise Exception('')

        return cls(mpl_cm)

    @classmethod
    def from_dict(cls, cdict, name='default'):
        """
           from matplotlib:
               Create color map from linear mapping segments

               segmentdata argument is a dictionary with a red, green and blue
               entries. Each entry should be a list of *x*, *y0*, *y1* tuples,
               forming rows in a table. Entries for alpha are optional.

               Example: suppose you want red to increase from 0 to 1 over
               the bottom half, green to do the same over the middle half,
               and blue over the top half.  Then you would use::

                   cdict = {'red':   [(0.0,  0.0, 0.0),
                                      (0.5,  1.0, 1.0),
                                      (1.0,  1.0, 1.0)],

                            'green': [(0.0,  0.0, 0.0),
                                      (0.25, 0.0, 0.0),
                                      (0.75, 1.0, 1.0),
                                      (1.0,  1.0, 1.0)],

                            'blue':  [(0.0,  0.0, 0.0),
                                      (0.5,  0.0, 0.0),
                                      (1.0,  1.0, 1.0)]}

               Each row in the table for a given color is a sequence of
               *x*, *y0*, *y1* tuples.  In each sequence, *x* must increase
               monotonically from 0 to 1.  For any input value *z* falling
               between *x[i]* and *x[i+1]*, the output value of a given color
               will be linearly interpolated between *y1[i]* and *y0[i+1]*::

                   row i:   x  y0  y1
                                  /
                                 /
                   row i+1: x  y0  y1

               Hence y0 in the first row and y1 in the last row are never used.
           """
        mpl_cm = col.LinearSegmentedColormap(name=name, segmentdata=cdict)
        return cls(mpl_cm, name=name)

    @classmethod
    def from_list(cls, clist, name='default', gradient=False):
        """
        Make a linear segmented colormap with *name* from a sequence
        of *colors* which evenly transitions from colors[0] at val=0
        to colors[-1] at val=1.  *N* is the number of rgb quantization
        levels.
        Alternatively, a list of (value, color) tuples can be given
        to divide
        """
        if gradient==False:
            mpl_cm = col.ListedColormap(name=name, colors=clist)
        if gradient==True:
            mpl_cm = col.LinearSegmentedColormap.from_list(name='default', colors=clist)
        return cls(mpl_cm, name=name)

    @classmethod
    def from_cptfile(cls, filepath):
        name, cptdict = cptfile2dict(filepath)
        return cls.from_dict(cptdict, name=name)

    @classmethod
    def from_gdal(cls, filepath):
        name, gdaldict = gdal2dict(filepath)
        return cls.from_dict(gdaldict, name=name)

    @classmethod
    def from_json(cls, filepath):
        name, jsonlist = json2list(filepath)
        return cls.from_list(jsonlist, name=name)
