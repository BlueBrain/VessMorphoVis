# Introduction 

VessMorphoVis is an integrated suite of toolboxes for interactive visualization and analysis of vast brain vascular networks represented by morphological graphs segmented originally from imaging or microscopy stacks. Our workflow leverages the outstanding potentials of Blender, aiming to establish an integrated, extensible and domain-specific framework capable of interactive visualization, analysis, repair, high-fidelity meshing and high-quality rendering of vascular morphologies.

## Features

+ Interactive visualization, analysis and automated repair of large-scale vasculature morphology skeletons.
+ Sketching and building three-dimensional representations of the vascular morphology skeletons using various methods for visual analytics.
+ Automated analysis of neuronal morphology skeletons that are digitally reconstructed from optical microscopy stacks. 
+ An easy context to load broken morphology skeletons and repair them manually. 
+ Automated reconstruction of polygonal mesh models that represent the surface of the vasvular morphologies based on the piecewise meshing method presented by [Abdellah et al., 2017](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1788-4).
+ Accurate mesh reconstruction with meta balls to create watertight meshes for reaction-diffusion simulations.
+ Exporting the reconstructed meshes in several file formats including [PLY](https://en.wikipedia.org/wiki/PLY_(file_format)), [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file), [STL](https://en.wikipedia.org/wiki/STL_(file_format)) and also as a Blender file ([.blend](https://en.wikipedia.org/wiki/Blender_(software)#File_format)).


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

# Known Bugs or Feature Requests

Please refer to the [github issue tracker](https://github.com/BlueBrain/VessMorphoVis/issues) for fixed and open bugs. User can also report any bugs and request new features needed for their research. We are happy to provide direct [support](#contact) . 


# Publications & Citation 

If you use _VessMorphoVis_ for your research, media design or other purposes, please cite our paper _Interactive visualization and analysis of morphological skeletons of brain vasculature networks with VessMorphoVis_ using the following entry:

```
@article{abdellah2020interactive,
  title={Interactive visualization and analysis of morphological skeletons of brain vasculature 
         networks with VessMorphoVis},
  author={Abdellah, Marwan and Guerrero, Nadir Román abd Lapere, Samule and Coggan, Jay S. and 
          Coste, Benoit and Dagaer, Snigdha and Keller, Daniel and Courcol, Jean-Denis and 
          Markram, Henry and Sch{\"u}rmann, Felix},
  journal={Bioinformatics},
  volume={In press},
  year={2020},
  publisher={Oxford University Press}
}
```

# Contact

For more information on _VessMorphoVis_, comments or suggestions, please contact:

__Marwan Abdellah__  
Scientific Visualiation Engineer  
Blue Brain Project  
[marwan.abdellah@epfl.ch](marwan.abdellah@epfl.ch) 
 
__Felix Schürmann__  
Co-director of the Blue Brain Project    
[felix.schuermann@epfl.ch](samuel.lapere@epfl.ch) 

Should you have any questions concerning press enquiries, please contact:

__Kate Mullins__  
Communications  
Blue Brain Project  
[kate.mullins@epfl.ch](kate.mullins@epfl.ch)




