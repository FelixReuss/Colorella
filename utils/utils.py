import numpy as np
import colorsys
import os
import json


def cptfile2dict(filepath):
    """
           Creates a color dict for a colormap object from a .cpt colormap file

           Returns
           -------
           dict with all colors from file

           """
    try:
        f = open(filepath)
        name = os.path.splitext(os.path.basename(filepath))[0]
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
    return name, colordict

def gdal2list(filepath):
    """
            Creates a color list for a colormap object from a gdal .ct file

            Returns
            -------
            list with a colors from file

            """

    try:
        f = open(filepath)
        name = os.path.splitext(os.path.basename(filepath))[0]
    except IOError:
        print("file ", filepath, "not found")

    lines = f.readlines()
    f.close()
    red = []
    green = []
    blue = []
    col_list = []
    for l in lines:
        ls = l.split()
        if l.strip():
            red.append(float(ls[0]))
            green.append(float(ls[1]))
            blue.append(float(ls[2]))

        else:
            continue

    red = np.array(red, dtype=np.float64)
    green = np.array(green, dtype=np.float64)
    blue = np.array(blue, dtype=np.float64)

    red = red / 255.
    green = green / 255.
    blue = blue / 255.

    for i in range(len(red)):
        col_list.append((red[i], green[i], blue[i]))
    colordict = {"red": red, "green": green, "blue": blue}
    return name, colordict

def json2list(filepath):
    """
           Creates a color list for a colormap object from a json file, or None if the file was invalid

           Returns
           -------
           list with all colors from file

           """

    try:
        with open(filepath, "r") as fidin:
            name = os.path.splitext(os.path.basename(filepath))[0]
            cmap_dict = json.load(fidin)
            cmap_dict = cmap_dict[0]
            if cmap_dict.get('RGBPoints', None) is None:
                return None
            colormap_type = cmap_dict.get('type', 'segmented')
            colormap_name = cmap_dict.get('name', os.path.basename(filepath))
            if colormap_type == 'segmented':
                col_list = [cmap_dict['RGBPoints'][x:x + 3] for x in range(0, len(cmap_dict['RGBPoints']), 4)]
            elif colormap_type == 'listed':
                col_list = [cmap_dict['RGBPoints'][x:x + 3] for x in range(0, len(cmap_dict['RGBPoints']), 4)]

    except IOError:
        print("file ", filepath, "not found")

    return name, col_list