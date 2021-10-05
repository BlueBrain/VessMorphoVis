# Introduction 

_VessMorphoVis_ is an integrated suite of toolboxes for interactive visualization and analysis of 
vast brain vascular networks represented by morphological graphs segmented originally from imaging 
or microscopy stacks. Our workflow leverages the outstanding potentials of Blender, aiming to 
establish an integrated, extensible and domain-specific framework capable of interactive 
visualization, analysis, repair, high-fidelity meshing and high-quality rendering of vascular 
morphologies. _VessMorphoVis_ is developed as an extension to its sister 
[_NeuroMorphoVis_](https://github.com/BlueBrain/NeuroMorphoVis). 

<p align="center">
	<img src="https://raw.githubusercontent.com/wiki/BlueBrain/VessMorphoVis/images/logos/vmv-logo.jpeg" width="600">
</p>

## Features

+ Interactive visualization, analysis and automated repair of large-scale vasculature morphology 
skeletons (up to millions of samples).

+ Sketching and building three-dimensional representations of the vascular morphology skeletons 
using various methods for visual analytics.

+ Analysis of neuronal morphology skeletons that are digitally reconstructed from imaging or 
microscopy stacks. 

+ An easy context to load broken morphology skeletons and repair them manually. 

+ Automated reconstruction of polygonal mesh models that represent the surface of the vasvular 
morphologies based on the piecewise meshing method presented by 
[Abdellah et al., 2017](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1788-4).

+ Accurate mesh reconstruction with MetaBalls to create watertight meshes for 
[reaction-diffusion simulations](https://en.wikipedia.org/wiki/Reaction%E2%80%93diffusion_system).

+ Large scale and efficient rendering of the vascular morphologies and meshes using the 
Workbench renderer.
 
+ Automated high quality rendering of the vascular morphologies and their corresponding meshes 
using different shading nodes with Cycles.

+ Exporting the reconstructed meshes in several file formats including 
[PLY](https://en.wikipedia.org/wiki/PLY_(file_format)), 
[OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file), 
[STL](https://en.wikipedia.org/wiki/STL_(file_format)) 
and also as a Blender file ([.blend](https://en.wikipedia.org/wiki/Blender_(software)#File_format)).

# Package Details

_VessMorphoVis_ is mainly based on [Blender](https://www.blender.org/). 
Blender is a free software and can be downloaded from [Blender.org](http://download.blender.org/release/). 
Blender is released under the GNU General Public License ([GPL](https://www.blender.org/about/license/), or 
“free software”).
The current version of _VessMorphoVis_ is compatible with the following Blender versions:

+ [Blender 2.80](http://download.blender.org/release/Blender2.80/)
+ [Blender 2.81](http://download.blender.org/release/Blender2.81/)
+ [Blender 2.82](http://download.blender.org/release/Blender2.82/)
+ [Blender 2.83](http://download.blender.org/release/Blender2.83/)

_VessMorphoVis_ can be downloaded as a __binary archive bundled within Blender__ that can be easily 
extracted and used [out-of-the-box](https://en.wikipedia.org/wiki/Out_of_the_box_(feature)). 
The optional dependencies are already shiped within this archive using [pip](https://pypi.org/project/pip/) 
on each respective platform. This package (released every minor version update of the software) is 
recommended for __Windows users__ or those who cannot use 
the [__Terminal__](https://en.wikipedia.org/wiki/Unix_shell). 
Otherwise, users can just download an installation script that will automatically install the entire 
package to a user-specified directory. This script __does not__ require __sudo__ permissions.

# Documentation 
The documentation is available [here](https://github.com/BlueBrain/VessMorphoVis/wiki). 

# Known Bugs or Feature Requests

Please refer to the [github issue tracker](https://github.com/BlueBrain/VessMorphoVis/issues) for 
fixed and open bugs. User can also report any bugs and request new features needed for their research. 
We are happy to provide direct [support](#contact) . 

# Gallery 

<p align="center">
	<img src="https://github.com/BlueBrain/VessMorphoVis/wiki/images/rendering/BH0031.CNG_artistic.jpg" width=600>
</p>

<p align="center">
	<img src="https://raw.githubusercontent.com/wiki/BlueBrain/VessMorphoVis/images/rendering/vascular_mesh_column.jpeg" width="600">
</p>

<p align="center">
	<img src="https://raw.githubusercontent.com/wiki/BlueBrain/VessMorphoVis/images/rendering/per_segment_coloring_1.jpeg" height="400">
	<img src="https://raw.githubusercontent.com/wiki/BlueBrain/VessMorphoVis/images/rendering/per_segment_coloring_2.jpeg" height="400">
</p>


# Publications & Citation 

If you use _VessMorphoVis_ for your research, media design or other purposes, please cite our 
paper _Interactive visualization and analysis of morphological skeletons of brain vasculature 
networks with VessMorphoVis_ using the following entry:

```
@article{abdellah2020interactive,
  title={Interactive visualization and analysis of morphological skeletons of brain vasculature 
         networks with VessMorphoVis},
  author={Abdellah, Marwan and Guerrero, Nadir Román abd Lapere, Samule and Coggan, Jay S. and 
          Coste, Benoit and Dagar, Snigdha and Keller, Daniel and Courcol, Jean-Denis and 
          Markram, Henry and Sch{\"u}rmann, Felix},
  journal={Bioinformatics},
  volume={In press},
  year={2020},
  publisher={Oxford University Press}
}
```

# Acknowledgement & Funding
_VessMorphoVis_ is developed by the Visualization team at the 
[Blue Brain Project](https://bluebrain.epfl.ch/page-52063.html), 
[Ecole Polytechnique Federale de Lausanne (EPFL)](https://www.epfl.ch/). 
This study was supported by funding to the Blue Brain Project, a research center of the 
École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the 
Swiss Federal Institutes of Technology.


# License 
_VessMorphoVis_ is available to download and use under the GNU General Public License 
([GPL](https://www.gnu.org/licenses/gpl.html), or “free software”). 
The code is open sourced with approval from the open sourcing committee and principal coordinators 
of the Blue Brain Project in June 2020. 

Copyright (c) 2019 - 2021 Blue Brain Project/EPFL

# Attributions 

* [Blender](https://www.blender.org/) (C) is copyright to Blender Foundation. 
The Blender Foundation is a non-profit organization responsible for the development of Blender. 
Blender is released under the GNU Public License, as Free Software, and therefore can be distributed 
by anyone freely. 

* The SWC morphology samples are available from the [Brain Vasculature (BraVa) database](http://cng.gmu.edu/brava). 
The Brain Vasculature (BraVa) database contains digital reconstructions of the human brain arterial 
arborizations from 61 healthy adult subjects along with extracted morphological measurements.
The arterial arborizations include the six major trees stemming from the circle of Willis, 
namely: the left and right Anterior Cerebral Arteries (ACAs), Middle Cerebral Arteries (MCAs), 
and Posterior Cerebral Arteries (PCAs). 
Citation: [Susan N. Wright, Peter Kochunov, Fernando Mut Maurizio Bergamino, Kerry M. Brown, John C. Mazziotta, 
Arthur W. Toga, Juan R. Cebral, Giorgio A. Ascoli. 
Digital reconstruction and morphometric analysis of human brain arterial vasculature from magnetic 
resonance angiography. NeuroImage, 82, 170-181, (2013)](http://dx.doi.org/10.1016/j.neuroimage.2013.05.089). 

* The VMV morphology samples are available with permissions from 
[Pablo Blinder](http://pblab.tau.ac.il/en/), Department of Neurobiology at the Tel Aviv University,
Israel. 

* The H5 morphology samples are available with permissions from the 
[Blue Brain Project](https://bluebrain.epfl.ch/page-52063.html), 
[Ecole Polytechnique Federale de Lausanne (EPFL)](https://www.epfl.ch/). The original dataset 
courtesy of [Bruno Weber](https://www.neuroscience.uzh.ch/en/about/people/steering/Weber.html), 
University of Zurich, Switzerland.

* _VessMorphoVis_ depends on the [MorphIO library](https://github.com/BlueBrain/MorphIO) to load 
H5 morphologies. MorphIO is licensed under the terms of the GNU Lesser General Public License 
version 3.

* The table of contents for all the user documentation pages are generated 
with [markdown-toc](http://ecotrust-canada.github.io/markdown-toc/).
 
# Contact

For more information on _VessMorphoVis_, comments or suggestions, please contact:

__Marwan Abdellah__  
Scientific Visualiation Engineer  
Blue Brain Project  
[marwan.abdellah@epfl.ch](marwan.abdellah@epfl.ch) 
 
__Felix Schürmann__  
Co-director of the Blue Brain Project    
[felix.schuermann@epfl.ch](felix.schuermann@epfl.ch) 

Should you have any questions concerning press enquiries, please contact:

__Kate Mullins__  
Communications  
Blue Brain Project  
[kate.mullins@epfl.ch](kate.mullins@epfl.ch)

<p align="center">
	<img src="https://github.com/BlueBrain/VessMorphoVis/wiki/images/logos/epfl-logo.jpg" width=200>
</p>



