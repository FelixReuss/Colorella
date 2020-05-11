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

#CM_DIRPATH = './colormaps'

# TODO: create a second file with general functions, e.g. RGB to 0, 1 conversion.
# TODO: tidy up all comments, create more were necessary

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

        #else:
            #self.c_map_name = userinput

        # TODO: the first check must be a matplotlib colormap

        if self.arg in plt.colormaps():
            self._object = cm.get_cmap(self.arg)  # TODO: better variable naming than object? _mpl_cm
            #self.name = self.arg

        elif isinstance(self.arg, list):
            self._object = col.ListedColormap(name=name, colors=self.arg)  # TODO: the name should be self.cm_name

        elif isinstance(self.arg, dict):
            self._object = col.LinearSegmentedColormap(name=name, segmentdata=self.arg) # TODO: the name should be self.cm_name

        elif '.' in self.arg:  # TODO: use os.path.isfile or sth similar
            name = os.path.splitext(arg)[0]
            extension = os.path.splitext(arg)[1] # TODO: self.extension was never set before

            if '.cpt' == extension:

                #self.c_map_name = self.userinput

            elif '.ct' == extension:
                self._object = col.LinearSegmentedColormap.from_list(name='CMap', segmentdata=self.__colormap_from_gdal())
                #self.c_map_name = self.userinput

            elif '.json' == extension:
                self._object = col.ListedColormap(name='CMAP', colors=self.__colormap_from_json())

        else:
            # TODO: update error message
            # valid = c.colormaps + c.diverging_black
            txt = "name provided {0} is not recognised or file extension is not supported. ".format(self.arg)
            txt += "\n valid name can be found in colormap.colormap_names"
            txt += "\n supported file extensions are .cpt and .ct"
            raise ValueError(txt)

    # TODO: maybe add some properties? How many colours are in the colourmap etc., the name of the colourmap

    @property
    def name(self):
        return self._mpl_cm.name

    # TODO: delete
    # @staticmethod
    # def colormaps_path():
    #     """
    #     Returns
    #     -------
    #     current colormap directory
    #     """
    #     return CM_DIRPATH

    # TODO: delete
    # @staticmethod
    # def get_user_colormaps():
    #     """
    #     Lists all colormaps in the colormap directory
    #
    #     Returns
    #     -------
    #     list of all files in the colormap directory
    #     """
    #     user_colormaps = []
    #     for root, dirs, files in os.walk(CM_DIRPATH):
    #         user_colormaps.append(files)
    #     return print(user_colormaps)

    def __len__(self):
        return 3

    def __getitem__(self, item):
        pass

    def __str__(self):
        pass

    # TODO: In my opinion this should be a to_ ... method
    # TODO: don't overwrite, use inplace or return new object
    def gradient(self, name = None, inplace=True):
        """
        Converts a listed Colormap to a Linear Segmented Colormap

        Parameters
        ----------
        outname: str, optional
            filename if the colormap is saved
        """
        if "LinearSegmentedColormap" == self._mpl_cm:
            warnings.warn("dasdfs")
            return self
        else:

        mpl_cm = col.LinearSegmentedColormap.from_list(name, self._mpl_cm.colors)
        if inplace:
            self._mpl_cm = mpl_cm
            return self
        else:
            return ColorMap(mpl_cm)

    # TODO: why two times?
    # TODO: don't overwrite, use inplace or return new object
    #Same as from_gradient
    # def listed2segmented(self, outname = None):
    #     """
    #     Converts a listed Colormap to a Linear Segmented Colormap
    #
    #     Parameters
    #     ----------
    #     outname: str, optional
    #         filename if the colormap is saved
    #     """
    #     if isinstance(self._object, col.ListedColormap):
    #         self._object = col.LinearSegmentedColormap.from_list(outname, self._object.colors)
    #     else:
    #         return None

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
            outname = self.name+'.cpt'
        elif '.cpt' not in outname:
            outname = outname+'.cpt'
        vmin=0
        vmax=1
        N=255
        #def export_cmap_to_cpt(cmap, vmin=0, vmax=1, N=255, filename="test.cpt", **kwargs):
        #    # create string for upper, lower colors
        b = np.array(kwargs.get("B", self._object(0.)))
        f = np.array(kwargs.get("F", self._object(1.)))
        na = np.array(kwargs.get("N", (0, 0, 0))).astype(float)
        ext = (np.c_[b[:3], f[:3], na[:3]].T * 255).astype(int)
        #Creating footer
        extstr = "B {:3d} {:3d} {:3d}\nF {:3d} {:3d} {:3d}\nN {:3d} {:3d} {:3d}"
        ex = extstr.format(*list(ext.flatten()))
        # create colormap
        colors = (self._object(np.linspace(0., 1., N))[:, :3] * 255).astype(int)
        vals = np.linspace(vmin, vmax, N)
        arr = np.c_[vals[:-1], colors[:-1], vals[1:], colors[1:]]

        fmt = "%e %3d %3d %3d %e %3d %3d %3d"

        if not os.path.exists(CM_DIRPATH):
            os.makedirs(CM_DIRPATH)
        np.savetxt(os.path.join(CM_DIRPATH, outname), arr, fmt=fmt,
                   header="# COLOR_MODEL = RGB",
                   footer=ex, comments="")

    # TODO: don't overwrite, use inplace or return new object
    # TODO: more detailed documentation
    def convert2greyscale(self, weights = 1, inplace=True):
        """
        Return a grayscale version of the given colormap

        Parameters
        ----------
        weights: int
            weights used to convert RGB values to luminance, default =1

        """
        colors = self._object(np.arange(self._object.N))

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
            print('Argument weight only supports values between 1 and 3')

        colors[:, :3] = luminance[:, np.newaxis]
        self._object = col.LinearSegmentedColormap.from_list(self.c_map_name + "_grey", colors, self._object.N)

    def to_matplotlib(self):
        """
        Returns the matplotlib colormap object"
        """
        return self._object

    #TODO: Segmented Colormap returns no dict (if you cannot find a solution for this, add it to the nodes as a warning)
    def to_dict(self):
        """
        Creates a dictionary of colors from a colormap object

        Returns
        -------
        dict object

        """
        if isinstance(self._object, col.ListedColormap):
            col_list = self._object._lut
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

        elif isinstance(self._object, col.LinearSegmentedColormap):
            nested_col_list = []
            col_list = []
            #red = []
            #green = []
            #blue = []
            #alpha = []

            for key, value in self._object._segmentdata.items():
                nested_col_list.append([key, value])

            red = nested_col_list[0]
            red = red[1:]
            green = nested_col_list[1]
            green = green[1:]
            blue = nested_col_list[2]
            blue = blue[1:]
            alpha = nested_col_list[3]
            alpha = alpha[1:]

            for i in range(len(red)):
                col_list.append((red[i], green[i], blue[i], alpha[i]))

    def to_list(self):
        """
        Creates a list of colors from a colormap object

        Returns
        -------
        List object
        """
        if isinstance(self._object, col.ListedColormap):
            col_list = self._object._lut
            col_list_tuples = [tuple(l) for l in col_list]
            return col_list_tuples

        elif isinstance(self._object, col.LinearSegmentedColormap):
            temp = []
            dic_list = []
            for key, value in self._object._segmentdata.items():
                temp = [key, value]
                dic_list.append(temp)

    def plot(self):
        """
        Shows the colormap as a colorbar in a plot
        """
        #cmap = self.to_matplotlib()
        #colors = cmap(np.arange(cmap.N))
        #plt.imshow([colors], extent=[0, 10, 0, 1])
        #plt.axis('off')
        #plt.show()
        #cmap = plt.cm.get_cmap(self._object)
        colors = self._object(np.arange(self._object.N))
        plt.imshow([colors], extent=[0, 10, 0, 1])
        plt.axis('off')
        plt.show()

    # TODO: don't overwrite, use inplace or return new object
    def reverse(self, inplace=True):
        """
        Reverses a colormap, a.k.a returns the containing colors in reverse direction
        """

        if isinstance(self._object, col.ListedColormap):
            self._object = col.ListedColormap(self._object.colors[::-1])

        elif isinstance(self._object, col.LinearSegmentedColormap):
            reverse = []
            keys = []

            for key in self._object._segmentdata:
                keys.append(key)
                channel = self._object._segmentdata[key]
                data = []

                for c in channel:
                    data.append((1 - c[0], c[2], c[1]))
                reverse.append(sorted(data))

            revdict = dict(zip(keys, reverse))
            self._object = mpl.colors.LinearSegmentedColormap(self._object, revdict)
        return self._object

    @classmethod
    def from_cptfile(cls, filepath):
        cptdict = cptfile2dict(filepath)
        return cls.from_dict(cptdict)

    # TODO: this function is general file -> dict; move them somewhere else and implement them as a classmethod. cptfile2dict
    #add if line is empty continue
    def __colormap_from_cptfile(self):
        """
        Creates a color dict for a colormap object from a .cpt colormap file

        Returns
        -------
        dict with all colors from file

        """
        filepath = os.path.join(CM_DIRPATH, self.c_map_name + self.extension)
        try:
            f = open(filepath)
        except IOError:
            print("file ", filepath, "not found")
            return None

        lines = f.readlines()
        f.close()

        x = []
        r = []
        g = []
        b = []
        colorModel = "RGB"
        for l in lines:
            ls = l.split()
            if l.strip():
                if l[0] == "#":
                    if ls[-1] == "HSV":
                        colorModel = "HSV"
                        continue
                    else:
                        continue
                if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
                    pass
                else:
                    x.append(float(ls[0]))
                    r.append(float(ls[1]))
                    g.append(float(ls[2]))
                    b.append(float(ls[3]))
                    xtemp = float(ls[4])
                    rtemp = float(ls[5])
                    gtemp = float(ls[6])
                    btemp = float(ls[7])
            else:
                continue

        x.append(xtemp)
        r.append(rtemp)
        g.append(gtemp)
        b.append(btemp)

        nTable = len(r)
        x = np.array(x, dtype=np.float64)
        r = np.array(r, dtype=np.float64)
        g = np.array(g, dtype=np.float64)
        b = np.array(b, dtype=np.float64)
        if colorModel == "HSV":
            for i in range(r.shape[0]):
                rr, gg, bb = colorsys.hsv_to_rgb(r[i] / 360., g[i], b[i])
                r[i] = rr;
                g[i] = gg;
                b[i] = bb
        if colorModel == "RGB":
            r = r / 255.
            g = g / 255.
            b = b / 255.
        xNorm = (x - x[0]) / (x[-1] - x[0])

        red = []
        blue = []
        green = []
        for i in range(len(x)):
            red.append([xNorm[i], r[i], r[i]])
            green.append([xNorm[i], g[i], g[i]])
            blue.append([xNorm[i], b[i], b[i]])
        colordict = {"red": red, "green": green, "blue": blue}
        return colordict

    # TODO: this function is general file -> dict; move them somewhere else and implement them as a classmethod.
    def __colormap_from_gdal(self):
        """
        Creates a color list for a colormap object from a gdal .ct file

        Returns
        -------
        list with a colors from file

        """
        filepath = os.path.join(CM_DIRPATH, self.c_map_name + self.extension)
        try:
            f = open(filepath)
        except IOError:
            print("file ", filepath, "not found")

        lines = f.readlines()
        f.close()
        r = []
        g = []
        b = []
        col_list = []
        for l in lines:
            ls = l.split()
            if l.strip():
                r.append(float(ls[0]))
                g.append(float(ls[1]))
                b.append(float(ls[2]))

            else:
                continue

        r = np.array(r, dtype=np.float64)
        g = np.array(g, dtype=np.float64)
        b = np.array(b, dtype=np.float64)

        r = r / 255.
        g = g / 255.
        b = b / 255.

        for i in range(len(r)):
            col_list.append((r[i], g[i], b[i]))
        return col_list

    # TODO: this function is general file -> dict; move them somewhere else.
    #TODO check if all json files look the same? Alpha channel? Listed or segmented, keywords and implement them as a classmethod?
    def __colormap_from_json(self):
        """
        Creates a color list for a colormap object from a json file, or None if the file was invalid

        Returns
        -------
        list with all colors from file

        """
        filepath = os.path.join(CM_DIRPATH, self.c_map_name + self.extension)
        try:
            with open(filepath, "r") as fidin:
                cmap_dict = json.load(fidin)
                cmap_dict = cmap_dict[0]
                if cmap_dict.get('RGBPoints', None) is None:
                    return None
                colormap_type = cmap_dict.get('type', 'segmented')
                colormap_name = cmap_dict.get('name', os.path.basename(filepath))
                if colormap_type == 'segmented':
                    col_list = [cmap_dict['RGBPoints'][x:x+3] for x in range(0, len(cmap_dict['RGBPoints']), 4)]
                elif colormap_type == 'listed':
                    col_list = [cmap_dict['RGBPoints'][x:x+3] for x in range(0, len(cmap_dict['RGBPoints']), 4)]

        except IOError:
            print("file ", filepath, "not found")

        return col_list

    # TODO: what do the following functions?
    # TODO: Delete
    def change(self, function):
        """ Applies function (which should operate on vectors of shape 3: [r, g, b]), on colormap cmap.
        This routine will break any discontinuous points in a colormap.
        e.g. dark_jet = cmap_map(lambda x: x*0.75, matplotlib.cm.jet)
            light_jet = cmap_map(lambda x: x/2 + 0.5, matplotlib.cm.jet)
        """
        if isinstance(self._object, col.LinearSegmentedColormap):
            cdict = self._object._segmentdata
            step_dict = {}
            # Firt get the list of points where the segments start or end
            for key in ('red', 'green', 'blue'):
                step_dict[key] = list(map(lambda x: x[0], cdict[key]))
            step_list = sum(step_dict.values(), [])
            step_list = np.array(list(set(step_list)))
            # Then compute the LUT, and apply the function to the LUT
            reduced_cmap = lambda step: np.array(self._object(step)[0:3])
            old_LUT = np.array(list(map(reduced_cmap, step_list)))
            new_LUT = np.array(list(map(function, old_LUT)))
            # Now try to make a minimal segment definition of the new LUT
            cdict = {}
            for i, key in enumerate(['red', 'green', 'blue']):
                this_cdict = {}
                for j, step in enumerate(step_list):
                    if step in step_dict[key]:
                        this_cdict[step] = new_LUT[j, i]
                    elif new_LUT[j, i] != old_LUT[j, i]:
                        this_cdict[step] = new_LUT[j, i]
                colorvector = list(map(lambda x: x + (x[1],), this_cdict.items()))
                colorvector.sort()
                cdict[key] = colorvector

            return col.LinearSegmentedColormap('CMap', cdict, 1024)
        else:
            return None

    # TODO: Delete
    def cmap_xmap(self, function):
        """ Applies function, on the indices of colormap cmap. Beware, function
        should map the [0, 1] segment to itself, or you are in for surprises.

        See also cmap_xmap.
        """
        if isinstance(self._object, col.LinearSegmentedColormap):
            cdict = self._object._segmentdata
            function_to_map = lambda x: (function(x[0]), x[1], x[2])
            for key in ('red', 'green', 'blue'):
                cdict[key] = map(function_to_map, cdict[key])
                cdict[key].sort()
                assert (cdict[key][0] < 0 or cdict[key][-1] > 1), "Resulting indices extend out of the [0, 1] segment."

            return col.LinearSegmentedColormap('CMap', cdict, 1024)

        else:
            return None