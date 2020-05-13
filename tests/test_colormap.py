# Copyright (c) 2020, TU Wien, Department of Geodesy and Geoinformation
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
Tests for the colormap.
"""

import unittest

from colorella.colormap import ColorMap


class TestColomap(unittest.TestCase):

    def __init__(self, filepath):
        self.filepath
        super().__init()

    def setUp(self):
        """ Retrieves test data filepaths and auxiliary data. """
        pass

    def test_cmap_from_name(self):
        """
        Tests creation of a colormap from name
        """
        cmap = ColorMap('Viridis')
        self.assertIsInstance(cmap, ColorMap)

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
        cmap = ColorMap(cdict)
        self.assertIsInstance(cmap, ColorMap)

    def cmap_from_list(self):
        clist = [(0., 1, 1), (0.05, 1, 1), (0.11, 0, 0),
                 (0.66, 1, 1), (0.89, 1, 1), (1, 0.5, 0.5)]
        cmap = ColorMap(clist)
        self.assertIsInstance(cmap, ColorMap)

    def cmap_from_gdal(self):
        clist = [(0., 1, 1), (0.05, 1, 1), (0.11, 0, 0),
                 (0.66, 1, 1), (0.89, 1, 1), (1, 0.5, 0.5)]
        cmap = ColorMap(clist)
        self.assertIsInstance(cmap, ColorMap)


if __name__ == '__main__':
    unittest.main()
