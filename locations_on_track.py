'''
Gives back indices for reward zone, outbound journey, and the areas before and after the reward zone.
'''
import numpy as np
import os

def reward_zone_arrays(prm, location):
    filepath = prm.get_filepath()
    rz_indices = []
    pre_rz_indices = []
    post_rz_indices = []
    outbound_indices = []


    for i in range(len(location)):
        if location[i]>=30 and location[i]<90:
            outbound_indices.append(i)
        if location[i]>=70 and location[i]<90:
            pre_rz_indices.append(i)
        elif location[i]>=90 and location[i]<110:
            rz_indices.append(i)
        elif location[i]>=110 and location[i]<130:
            post_rz_indices.append(i)

    np.save(filepath + "Behaviour\\Data\\outbound_journey", outbound_indices)
    np.save(filepath + "Behaviour\\Data\\reward_zone", rz_indices)
    np.save(filepath + "Behaviour\\Data\\pre_rz",  pre_rz_indices)