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

import numpy as np
import unittest
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.cm as cm
from colormap import colormap
import matplotlib.colors as col

# TODO: use random numbers
class TestColomap(unittest.TestCase):

    def __init__(self, filepath):
        self.filepath
        super().__init()

    @classmethod
    def setUpClass(cls):
        """ Creates Colormap test data. """
        cls(testpath)

    def setUp(self):
        """ Retrieves test data filepaths and auxiliary data. """

    def test_cmap_from_name(self):  #TODO: add test in front of
        """
        Tests creation of a colormap from name
        """
        cmap = colormap('Viridis')
        self.assertIsInstance(cmap, colormap)


    def cmap_from_dict(self):
        cdict = {'red': ((0., 1, 1),
                         (0.05, 1, 1),
                         (0.11, 0, 0),
                         (0.66, 1, 1),
                         (0.89, 1, 1),
                         (1, 0.5, 0.5)),
                 'green': ((0., 1, 1),
                           (0.05, 1, 1),
                           (0.11, 0, 0),
                           (0.375, 1, 1),
                           (0.64, 1, 1),
                           (0.91, 0, 0),
                           (1, 0, 0)),
                 'blue': ((0., 1, 1),
                          (0.05, 1, 1),
                          (0.11, 1, 1),
                          (0.34, 1, 1),
                          (0.65, 0, 0),
                          (1, 0, 0)),
                 'alpha': ((0., 1, 1),
                           (0.05, 1, 1),
                           (0.11, 1, 1),
                           (0.34, 1, 1),
                           (0.65, 0, 0),
                           (1, 0, 0))}
        cmap = colormap(cdict)
        self.assertIsInstance(cmap, colormap)

    def cmap_from_list(self):
        clist = [(0., 1, 1), (0.05, 1, 1), (0.11, 0, 0), (0.66, 1, 1), (0.89, 1, 1), (1, 0.5, 0.5)]
        cmap = colormap(clist)
        self.assertIsInstance(cmap, colormap)

    def cmap_from_gdal(self):
        clist = [(0., 1, 1), (0.05, 1, 1), (0.11, 0, 0), (0.66, 1, 1), (0.89, 1, 1), (1, 0.5, 0.5)]
        cmap = colormap(clist)
        self.assertIsInstance(cmap, colormap)

    def cmap_from_cpt(self):


        self.assertIsInstance(cmap, colormap)


if __name__ == '__main__':
    unittest.main()