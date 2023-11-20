

import matplotlib.pyplot as plt
from pulse2percept.stimuli import GratingStimulus
xdim, ydim = 1024, 768


for direction in range(0, 180, 10):
   stim = GratingStimulus((xdim, ydim), direction, spatial_freq=0.005, temporal_freq=0.0001)
   image = stim.data[:, 0].reshape(xdim, ydim)
   plt.imsave(f'grating_{direction}.bmp', image, cmap='gray')