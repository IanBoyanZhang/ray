# ray

Personal challenge

TODO: read original Jensen 98 paper

[Berkeley CS184](http://cs184.eecs.berkeley.edu/cs184_sp16/article/21)

## Photon Tracing

Also known as "light ray tracing", "backward ray tracing", "Forward ray tracing", "Backward path tracing"

Photon tracing works in exactly the same way as ray tracing except for the fact that photon propagate flux whereas rays gather radiance

Interaction of a photon with a material can be different that the interaction of a ray

When photon hits an object, it can either be reflected, transmitted, or absorbed, which is decided probabilistically based on the material parameters of the surface

### Russian Roulette
is used to decide which type of interaction

#### Reflection, transmission, or absorption

diffuse reflection coefficient d
and
specular reflection coefficient s (with d+s le 1)

Based the decision on maximum energy, compute the probability for refection as 
Pr = max(dr + sr, dg + sg, db + sb)
d - diffuse reflection
s - specular relection
RGB
#### Why Russian Roulette
TODO: Understand the benefits
1. We prefer photons with similar power in the photon map. This makes the radiance estimate much better using only a few photons
2. If we generate, say, two, photons per surface interaction then we will have power(2, 8) photons after 8 interactions. 

Caveat:

It increases variance on the solution. Instead of using exact values for reflection and transmission to scale the photon energy we now rely on 
a sampling of these values that will converage to the correct result as enough photons are used

TODO: read more literature on this topics described in [A Practical Guide to Global Illumination using Photon Maps](https://graphics.stanford.edu/courses/cs348b-01/course8.pdf)

## Photon Storing
Photon surface interactions are stored in photon map

### Which Photon surface interaction are stored?
Photons are only stored where they hit *diffuse* surface (non-specular surface)

*The probability of having a matching incoming photon from the specular direction is zero?*

*Standard ray tracing works better in this case?*

Global data structure **Photon Map**

Each emitted photon can be stored several times along its path.

Stores:

+ the position
+ incoming photon power
+ incident direction are stored
+ (Practical reason, a flag with each set of photon data, which is used during sorting and lookup in the photon map)
### Data structure
```c
float x,y,z     // position
char p[4]       // power packed as 4 chars -- Ward
char phi, theta // compressed incident direction
short flag      // flag used in kdtree
```

if memory is not concern, float can be used to store power in the red, green, and blue color band

Other performance-memory space trade-off consideration like memory address alignment
TODO: 
spectral simulation?

During the photon tracing pass the photon map is arranged as a flat array of photons. For efficiency reason this array is re-organized into a 
balanced *kdtree* before rendering

#### Coordination Transformation
TODO: is there a better way than doing inverse trigonometric functions?
lookup table?
phi = 255 * (atan2(dy, dx)*PI) / (2*PI)
theta = 255 * acos(dx) / PI


## Participant media
_volume photon map_

Probablity of being scattered or absorped in the medium

Depends on
+density of medium
+the distance the photon travels through the medium

the denser the medium, the shorter the average distance before a photon interaction happens

Photons are stored at the positions where a scattering event happens
The exception is photons that come directly from the light source since direct illumination is evaluated using ray tracing.

it allows us to compute the *in-scattered radiance* in a medium simply by a *lookup in the photon map*

TODO:
Read *anisotropic scattering*

### Multiple scattering, anistropic scattering, and non-homogeneous media
General multiple scattering is simulated simply by letting the photons scatter everywhere and continuously after the first interaction. The path can be terminated using Russian roulette

Ray marching to integrate the properties of the medium

Dividing the medium into little steps
Precomputed probability it is determined whether a photon should be absorbed, scattered, or whether another step is necessary

## Three photon map
+Caustic photon map

+Global photon map

+Volum photon map

TODO: understand matrix representation in above three different type of maps

More photon tracing path should be performed for caustic photon map since it should be of high quality and therefore often needs
more photons than the other two

The construction of the photon maps is most easily achieved by using *two separate photon tracing steps?* (mentioned above?)

TODO: The sequence shouldn't matter? 

# Preparing the photon map for rendering
Photons are only generated during the photon tracing pass, in the rendering pass the photon map is static data structure
Incoming flux and reflected radiance at many points in the scene

*To locate nearest photons in the photon map*

Requirement for data-structure

+fast nearest neighbor searching
+handle highly non-uniform distribution --caustics photon map

## Balanced kd-tree
The time it takes to locaate one photon in a balanced kd-tree has a worst time performance:
O(logN) N is the number of photons in the tree

A balanced kd-tree can be represented using a heap like data structure

(Array element 1 is the tree
root, and element i has element 2i as left child and element 2i+ 1 as right child.)

### Balancing

*Splitting dimension*
The choice of a splitting dimension is based on the distribution of points within the set.

One might use either the variance or the maximum distance between the points as criterion

The splitting dimension is thus chosen as the one which has the largest maximum distance between the points

Complexity of balancing algorithm is O(NlogN)

References:

1. [Rejection sampling](https://en.wikipedia.org/wiki/Rejection_sampling)

2. [A Practical Guide to Global Illumination using Photon Maps](https://graphics.stanford.edu/courses/cs348b-01/course8.pdf)

3. [Caustics](https://en.wikipedia.org/wiki/Caustic_(optics)#Computer_graphics)

4. [Diffuse and specular reflection](https://en.wikipedia.org/wiki/Diffuse_reflection#/media/File:Lambert2.gif)

5. [Ward's packed rgb format](https://en.wikipedia.org/wiki/RGBE_image_format)

6. [Bi-directional reflectance distribution function](https://en.wikipedia.org/wiki/Bidirectional_reflectance_distribution_function)

7. [Lambertian Cosine Law](https://en.wikipedia.org/wiki/Lambert%27s_cosine_law)

8. [Basic principles of surface reflectance](https://www.cs.cmu.edu/afs/cs/academic/class/15462-f09/www/lec/lec8.pdf)
