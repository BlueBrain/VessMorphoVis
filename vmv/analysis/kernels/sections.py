

from functools import reduce 

def compute_section_average_radius(section):


    
    pass 


def compite_segement_length(sample_1, sample_2):
    pass 


####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_length(section):
    
    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return 0.0

    # Compute the length from the segments 
    for i in range(len(section.samples) - 1):
        section_length += (section.samples[i + 1].point - section.samples[i].point).length
    
    # Return the section length 
    return section_length



def compute_section_surface_area(section):
    pass 

def compute_section_volume(section):
    pass



