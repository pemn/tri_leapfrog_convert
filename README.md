## Description
convert triangulations between leapfrog and vulcan
## Input/Output
file in any of the supported formats:  
 - 00t (Vulcan Triangulation, requires vulcan)
 - msh (Leapfrog Mesh)
 - obj (Wavefront mesh, open source format)
 ## Wildcards
 Instead of selecting multiple files, a file wildcard can be used.  
 ### Example1 
 `*.msh`  
 Leave the output field blank and a `00t` file with the same base name will be created for each input `msh` in the folder.  
 ### Example2
 `*.00t`  
 A .msh will be created for each 00t file.
 
