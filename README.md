# Summary
## The main script is from rivuletpy. I just modify some lines to improve the function that user can input their position of soma to trace from 3D confocal images. If you want to know more detail, please read https://github.com/RivuletStudio/rivuletpy.

# Installation
## 0. Download from github
## 1. Install the python package using conda
```
$ conda install numpy scipy matplotlib cython tqdm 
$ conda install -c conda-forge pylibtiff 
$ conda install -c simpleitk simpleitk 
```
# Usage
## 0. How to use
```
$ rtrace --help
usage: rtrace [-h] -f FILE [-o OUT] [-t THRESHOLD] [-z ZOOM_FACTOR] [-p SOMA_POSITION] [--save-soma] [--no-save-soma] [--speed] [--quality] [--no-quality] [--clean] [--no-clean] [--non-stop] [--npush NPUSH] [--silent]
              [--no-silent] [--skeletonize] [-v] [--no-view] [--tracing_resolution TRACING_RESOLUTION] [--vtk] [--slicer]

Arguments to perform the Rivulet2 tracing algorithm.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The input file. A image file (*.tif, *.nii, *.mat).
  -o OUT, --out OUT     The name of the output file
  -t THRESHOLD, --threshold THRESHOLD
                        threshold to distinguish the foreground and background. Default 0. If threshold<0, otsu will be used.
  -z ZOOM_FACTOR, --zoom_factor ZOOM_FACTOR
                        The factor to zoom the image to speed up the whole thing. Default 1.
  -p SOMA_POSITION, --soma_position SOMA_POSITION
                        x: x-axis, y: y-axis, z: stack of the images.
  --save-soma           Save the automatically reconstructed soma volume along with the SWC.
  --no-save-soma        Don't save the automatically reconstructed soma volume along with the SWC (default)
  --speed               Use the input directly as speed image
  --quality             Reconstruct the neuron with higher quality and slightly more computing time
  --no-quality          Reconstruct the neuron with lower quality and slightly more computing time
  --clean               Remove the unconnected segments (default). It is relatively safe to do with the Rivulet2 algorithm
  --no-clean            Keep the unconnected segments
  --non-stop            Whether to ignore the stopping criteria & just keep going no matter what. This is only used when you are sure all the positive voxels should belong to the structures of interests.
  --npush NPUSH         Number of iterations for pushing the centerline nodes to the center with the binary map boundaries. This is a post-processing step not nessensary for all the applications. When the number of steps
                        increases, each node will be closer to the center locally and the curves will be less smoother.
  --silent              Omit the terminal outputs
  --no-silent           Show the terminal outputs & the nice logo (default)
  --skeletonize         Preprocessing with skelontonization on the segmentation first before tracing. Recommended for structures with large diameter variance.
  -v, --view            View the reconstructed neuron when rtrace finishes
  --no-view
  --tracing_resolution TRACING_RESOLUTION
                        Only valid for input files compatible with ITK. Will resample the image array into isotropic resolution before tracing. Default 1mm
  --vtk                 Store the world coordinate vtk format along with the swc
  --slicer              Whether to save vtk coordinates in RAS space that can be rendered in 3D Slicer
```
## 1. A example in the TIFF file
```
automatically detect soma position using Rivuletpy method
$ rtrace -f ./test.tif -t 10 -o new.swc
set custom of soma position
$ rtrace -f ./test.tif -t 10 -o new.swc -p '168,102,10'
```

## Visulize the SWC file
Following here:
https://www.neutracing.com/

