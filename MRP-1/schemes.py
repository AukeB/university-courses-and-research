import numpy as np
import matplotlib.pyplot as plt

coordinate_array = [[-57,-59,-13,-90,-62],[-4,20,38,-34,15],['C','E','N','S','W']]

for i in range(5):
    plt.annotate(s='',xy=(i+1,coordinate_array[0][i]),xytext=(i+1,coordinate_array[1][i]),arrowprops=dict(arrowstyle='<|-|>'))
    plt.annotate(s='LS{0}'.format(coordinate_array[2][i]),xy=(i+1-0.148,coordinate_array[1][i]),xytext=(i+1-0.148,coordinate_array[1][i]),arrowprops=dict(width=0,headwidth=0,headlength=0))
plt.xlim(0,6)
plt.ylim(-91,91)
plt.title('Declination range of LaSilla Cameras')
plt.xlabel('Camera'); plt.ylabel('Declination (degrees)')
plt.grid()
plt.show()
