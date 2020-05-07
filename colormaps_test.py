import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from colormap import colormap
import matplotlib.colors as col


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

nested_col_list = []
col_list = []
red = []
green = []
blue = []
alpha = []

for key, value in cdict.items():
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
print(col_list[0][0])
cmap1 = [(0.05, 1, 1), (0.11, 1, 1), (0.34, 1, 1)]
cmap_ob3 = col.ListedColormap(cmap1)

cmap_ob1  = colormap('viridis')

#Json oolormaps seem to have incorrect colors, problem with alpha channel?
cmap_ob2 = colormap('Rainbow.json')
colormap.get_user_colormaps()
#cmap_ob1.view()




#cmap2 = ['#eeefff', '#eeefff', '#eeefff']
#cmap_ob2 = colormap(cmap2)
cmap_ob2.view()

cmap3 = [(0., 1, 1), (0.05, 1, 1), (0.11, 0, 0), (0.66, 1, 1), (0.89, 1, 1), (1, 0.5, 0.5)]
cmap_ob3 = colormap(cmap3)
cmap_ob3.view()

#arraqy = cmap.colors.to_rgba_array()



test2 = colormap('magma')
test3 = colormap('plasma')
#print(test3._object.colors.to_rgba())

test4 = colormap('ETOPO1.cpt')
test5 = colormap('sgrt_ct_cont_ssm.ct')

#test1.convert2greyscale(3)
test4.reverse()
#test1.view()
test2.view()
test3.view()
#print(test3.__dict__)
print(test5.to_list())

col_dic = test4._object._segmentdata
print(col_dic)


#test1.to_matplotlib()
#print(test4.__dict__)
#col_list = test1._object._lut
#col_list_sliced = col_list[:, :3]
#col_list_tuples = [tuple(l) for l in col_list_sliced]
#print(col_list_tuples)
#print(col_list)
#print(col_list[250][1])
#print(len(col_list[1]))
#print(np.shape(col_list))
#red = []
#green = []
#blue = []

#for i in range(len(col_list)):
#    red.append(col_list[i][0])
#    green.append(col_list[i][1])
#    blue.append(col_list[i][2])
#res_dct = {'R': red, 'G': green, 'B': blue}
#print(res_dct)
#print(test5.__dict__)
#test5.save('newtest')


#print(isinstance(test2.object, col.ListedColormap))
#test2.reverse()
#test5.to_greyscale()
#test5.save()
#print(str(test1.object))
#print(test1.__dict__)
#print('test4:', test4)
#print(test4.__dict__)

#print(test2.__dict__)
#print(isinstance(test1.object, col.ListedColormap))
#test1.reverse()
#test1.view()
#test2.view()
#test3.view()
#test4.view()
#test5.view()

#test4.save('test.cpt')

np.random.seed(19680801)
npts = 200
ngridx = 100
ngridy = 200
x = np.random.uniform(-2, 2, npts)
y = np.random.uniform(-2, 2, npts)
z = x * np.exp(-x**2 - y**2)

fig, (ax1, ax2) = plt.subplots(nrows=2)

# -----------------------
# Interpolation on a grid
# -----------------------
# A contour plot of irregularly spaced data coordinates
# via interpolation on a grid.

# Create grid values first.
xi = np.linspace(-2.1, 2.1, ngridx)
yi = np.linspace(-2.1, 2.1, ngridy)

# Perform linear interpolation of the data (x,y)
# on a grid defined by (xi,yi)
triang = tri.Triangulation(x, y)
interpolator = tri.LinearTriInterpolator(triang, z)
Xi, Yi = np.meshgrid(xi, yi)
zi = interpolator(Xi, Yi)

# Note that scipy.interpolate provides means to interpolate data on a grid
# as well. The following would be an alternative to the four lines above:
#from scipy.interpolate import griddata
#zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='linear')


ax1.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
cntr1 = ax1.contourf(xi, yi, zi, levels=14, cmap=cmap)

test5.convert2greyscale()
#test5.to_matplotlib()
#test5.to_dict()
#test5.to_list()
#test5.to_gdal_ct()

fig.colorbar(cntr1, ax=ax1)
ax1.plot(x, y, 'ko', ms=3)
ax1.set(xlim=(-2, 2), ylim=(-2, 2))
ax1.set_title('grid and contour (%d points, %d grid points)' %
              (npts, ngridx * ngridy))

plt.show()