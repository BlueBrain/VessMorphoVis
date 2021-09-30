#!/usr/bin/env bash
####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of VessMorphoVis <https://github.com/BlueBrain/VessMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

# If no configuration file is provided, then report it and exit
if [ $# -eq 0 ]
	then echo "No configuration file is provided, EXITING!"; exit
fi

# Source the input configuration file to use the parameters 
echo "Using the configuration file [$1]"
source $1

#####################################################################################################
BOOL_ARGS=''
if [ "$RECONSTRUCT_MORPHOLOGY_SKELETON" == "yes" ];
    then BOOL_ARGS+=' --reconstruct-morphology-skeleton '; fi
if [ "$RECONSTRUCT_VASCULAR_MESH" == "yes" ];
    then BOOL_ARGS+=' --reconstruct-vascular-mesh '; fi
if [ "$CONNECT_SOMA_MESH_TO_ARBORS" == "yes" ];
    then BOOL_ARGS+=' --connect-soma-arbors'; fi
if [ "$CONNECT_VASCULAR_OBJECTS_INTO_SINGLE_MESH" == "yes" ];
    then BOOL_ARGS+=' --joint-vascular-meshes'; fi
####################################################################################################
# Rendering parameters
if [ "$RENDER_VASCULAR_MORPHOLOGY" == "yes" ];
    then BOOL_ARGS+=' --render-vascular-morphology '; fi
if [ "$RENDER_VASCULAR_MORPHOLOGY_360" == "yes" ];
    then BOOL_ARGS+=' --render-vascular-morphology-360 '; fi
if [ "$RENDER_VASCULAR_MORPHOLOGY_PROGRESSIVE" == "yes" ];
    then BOOL_ARGS+=' --render-vascular-morphology-progressive '; fi
if [ "$RENDER_VASCULAR_MESH" == "yes" ];
    then BOOL_ARGS+=' --render-vascular-mesh '; fi
if [ "$RENDER_VASCULAR_MESH_360" == "yes" ];
    then BOOL_ARGS+=' --render-vascular-mesh-360 '; fi
if [ "$RENDER_TO_SCALE" == "yes" ];
    then BOOL_ARGS+=' --render-to-scale '; fi
####################################################################################################
# Export morphology
if [ "$EXPORT_VASCULAR_MORPHOLOGY_H5" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-h5'; fi
if [ "$EXPORT_VASCULAR_MORPHOLOGY_VMV" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-vmv'; fi
if [ "$EXPORT_VASCULAR_MORPHOLOGY_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-morphology-blend '; fi
####################################################################################################
# Export vascular mesh
if [ "$EXPORT_VASCULAR_MESH_PLY" == "yes" ];
    then BOOL_ARGS+=' --export-vascular-mesh-ply '; fi
if [ "$EXPORT_VASCULAR_MESH_OBJ" == "yes" ];
    then BOOL_ARGS+=' --export-vascular-mesh-obj '; fi
if [ "$EXPORT_VASCULAR_MESH_STL" == "yes" ];
    then BOOL_ARGS+=' --export-vascular-mesh-stl '; fi
if [ "$EXPORT_VASCULAR_MESH_BLEND" == "yes" ];
    then BOOL_ARGS+=' --export-vascular-mesh-blend '; fi
if [ "$EXPORT_INDIVIDUALS" == "yes" ];
    then BOOL_ARGS+=' --export-individuals '; fi
####################################################################################################
# Morphology analysis
if [ "$ANALYZE_MORPHOLOGY_SKELETON" == "yes" ];
    then BOOL_ARGS+=' --analyze-morphology '; fi

####################################################################################################
# echo 'FLAGS:' $BOOL_ARGS
echo -e "\nRUNNING ... VessMorphoVis \n"
    python vessmorphovis.py                                                                         \
    --blender=$BLENDER_EXECUTABLE                                                                   \
    --input=$INPUT                                                                                  \
    --morphology-file=$MORPHOLOGY_FILE                                                              \
    --morphology-directory=$MORPHOLOGY_DIRECTORY                                                    \
    --output-directory=$OUTPUT_DIRECTORY                                                            \
    --morphology-reconstruction-algorithm=$MORPHOLOGY_RECONSTRUCTION_ALGORITHM                      \
    --morphology-skeleton=$SKELETON                                                                 \
    --meshing-algorithm=$MESHING_TECHNIQUE                                                          \
    --meta-balls-resolution-setting=$META_BALLS_RESOLUTION_SETTING                                  \
    --meta-balls-resolution=$META_BALLS_RESOLUTION_VALUE                                            \
    --edges=$EDGES                                                                                  \
    --surface=$SURFACE                                                                              \
    --morphology-color=$MESH_COLOR                                                                  \
    --mesh-color=$MESH_COLOR                                                                        \
    --sections-radii=$SET_SECTION_RADII                                                             \
    --radii-scale-factor=$RADII_SCALE_FACTOR                                                        \
    --fixed-section-radius=$FIXED_SECTION_RADIUS                                                    \
    --minimum-section-radius=$MINIMUM_SECTION_RADIUS                                                \
    --bevel-sides=$SECTION_BEVEL_SIDES                                                              \
    --camera-view=$CAMERA_VIEW                                                                      \
    --camera-projection=$CAMERA_PROJECTION                                                          \
    --rendering-view=$RENDERING_VIEW                                                                \
    --full-view-resolution=$FULL_VIEW_FRAME_RESOLUTION                                              \
    --resolution-scale-factor=$FULL_VIEW_SCALE_FACTOR                                               \
    --shader=$SHADER                                                                                \
    --execution-node=$EXECUTION_NODE                                                                \
    --tessellation-ratio=$TESSELLATION_RATIO                                                        \
    $BOOL_ARGS

echo -e "\nVessMorphoVis DONE !\n"
####################################################################################################
