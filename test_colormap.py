# Copyright (c) 2020,Vienna University of Technology,
# Department of Geodesy and Geoinformation
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY, DEPARTMENT OF
# GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""
Tests for the Colormap().
"""
import unittest
import random
import matplotlib.pyplot as plt
import gdal
from colormap import colormap
import matplotlib.colors as col

class TestColomap(unittest.TestCase):

    def setUp(self):
        """ Retrieves test data filepaths and auxiliary data. """
        cm_list = plt.colormaps()
        self.default_cm = random.choice(cm_list)
        red = [(0., 1, 1), (1, 0, 0)]
        green = [(0., 1, 1), (1, 0, 0)]
        blue = [(0., 1, 1), (1, 0, 0)]
        alpha = [(0., 1, 1), (1, 0, 0)]
        for i in range(4):
            red.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            green.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            blue.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
            alpha.append((random.uniform(0, 1), random.randint(0, 1), random.randint(0, 1)))
        red.sort(key=lambda x: x[0])
        green.sort(key=lambda x: x[0])
        blue.sort(key=lambda x: x[0])
        alpha.sort(key=lambda x: x[0])
        self.cdict = {'red':tuple(red), 'green': tuple(green), 'blue': tuple(blue), 'alpha': tuple(alpha)}
        self.clist = []
        for i in range(random.randint(1, 20)):
            self.clist.append((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))

    def test_cmap_from_name(self):
        """
        Tests creation of a colormap from name
        """
        cmap = colormap(self.default_cm)
        self.assertIsInstance(cmap, colormap)

    def test_cmap_from_dict(self):
        cmap = colormap(self.cdict)
        self.assertIsInstance(cmap, colormap)

    def test_cmap_from_list(self):
        cmap = colormap(self.clist)
        self.assertIsInstance(cmap, colormap)

    def test_cmap_from_gdal(self):
        path_ct_file = r'\test_data\sgrt_ct_cont_ssm.ct.cpt'
        cmap = colormap(path_ct_file)
        self.assertIsInstance(cmap, colormap)

    def test_cmap_from_cpt(self):
        path_cpt_file = r'\test_data\ETOPO1.cpt'
        cmap = colormap(path_cpt_file)
        self.assertIsInstance(cmap, colormap)

    def test_cmap_from_json(self):
        path_json_file = r'\test_data\Rainbow.json'
        cmap = colormap(path_json_file)
        self.assertIsInstance(cmap, colormap)

    def test_listed2segmented(self):
        cmap = colormap(self.clist)
        cmap = cmap.listed2segmented()
        self.assertIsInstance(cmap, col.LinearSegmentedColormap)

    def test_save(self):
        cmap_write = colormap(self.clist)
        outpath = r'\test_data\test_save.cpt'
        cmap_write.save(outpath)
        cmap_read = colormap(outpath)
        self.assertEqual(cmap_read, cmap_write)

    def test_convert2greyscale(self):
        cmap = colormap(self.default_cm)
        cmap_grey = cmap.convert2greyscale()
        cmap_grey.view()
        self.assertIsInstance(cmap_grey, col.LinearSegmentedColormap)

    def test_to_matplotlib(self):
        cmap = colormap(self.default_cm)
        self.assertIsInstance(cmap, col.LinearSegmentedColormap)

    def test_to_dict(self):
        cmap = colormap(self.cdict)
        cdict_out = cmap.to_dict()
        self.assertEqual(self.cdict, cdict_out)

    def test_to_list(self):
        cmap = colormap(self.clist)
        clist_out = cmap.to_list()
        self.assertListEqual(self.clist, clist_out)

    def test_reverse(self):
        if isinstance(self._mpl_cm, col.ListedColormap):
            colors_reverse = self._mpl_cm.colors[::-1]
        elif isinstance(self._mpl_cm, col.LinearSegmentedColormap):
            colors_reverse = []
            keys = []

            for key in self._mpl_cm._segmentdata:
                keys.append(key)
                channel = self._mpl_cm._segmentdata[key]
                data = []

                for c in channel:
                    data.append((1 - c[0], c[2], c[1]))
                colors_reverse.append(sorted(data))

        self.assertEqual(self.cdict, colors_reverse)

    def test_view(self):
        cmap = colormap(self.default_cm)
        cmap.view()

    def test_to_gdal(self):
        cmap = colormap(self.default_cm)
        g_ct = cmap.to_gdal()
        self.assertIsInstance(g_ct, gdal.ColorTable)

if __name__ == '__main__':
    unittest.main()