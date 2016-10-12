# CONSTANT
# TODO: load constant from another file

# TODO: Use numpy vector

# Monte carlo distribution?

# Energy 
from random import uniform
import operator

def emit_photons_from_diffuse_point_light():
  # NUM_OF_PHOTON = 1e6
  # NUM_OF_PHOTON = 1e2
  NUM_OF_PHOTON = 1
  n_e = 0
  # TODO: parameterize light source position
  # (x, y, z, Energy)
  p = (0, 0, 0, 0)
  # What s the best data structure?
  photons = []
  # not enough photon?
  while(n_e < NUM_OF_PHOTON):
    while True:
      x = uniform(-1, 1)
      y = uniform(-1, 1)
      z = uniform(-1, 1)
      if x*x + y*y + z*z <= 1:
        # trace photon from p in direction d
        # Vector add
        # photons.append((x, y, z))
        # Normalized energy
        photons.append(tuple(map(operator.add, p, (x, y, z, 1.0/NUM_OF_PHOTON))))
        break
    n_e += 1
  
  return photons

print emit_photons_from_diffuse_point_light()
