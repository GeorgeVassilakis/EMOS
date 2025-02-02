"""
Geometric calculations for transit simulations.
"""

import numpy as np

def transit_area_vectorized(x, y, radius, star_radius):
    """
    Vectorized calculation of the overlap area between the star and a transiting body.
    """
    distance = np.sqrt(x**2 + y**2)
    area = np.zeros_like(distance)
    
    # Case 1: No overlap
    no_overlap = distance >= (star_radius + radius)
    area[no_overlap] = 0
    
    # Case 2: Complete overlap (transiting body entirely within the star)
    complete_overlap = distance <= (star_radius - radius)
    area[complete_overlap] = np.pi * radius**2
    
    # Case 3: Partial overlap
    partial_overlap = ~(no_overlap | complete_overlap)
    d = distance[partial_overlap]
    r, R = radius, star_radius
    argument = (d**2 + r**2 - R**2) / (2*d*r)
    argument_clipped = np.clip(argument, -1, 1)
    phi = 2 * np.arccos(argument_clipped)

    theta = 2 * np.arccos((d**2 + R**2 - r**2) / (2 * d * R))
    area1 = 0.5 * r**2 * (phi - np.sin(phi))
    area2 = 0.5 * R**2 * (theta - np.sin(theta))
    area[partial_overlap] = area1 + area2
    
    return area

def circle_overlap_vectorized(x1, y1, r1, x2, y2, r2):
    """
    Vectorized calculation of the overlap area between two circles.
    """
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    area = np.zeros_like(distance)
    
    # Case 1: No overlap
    no_overlap = distance >= (r1 + r2)
    area[no_overlap] = 0
    
    # Case 2: Complete overlap (one circle entirely within the other)
    complete_overlap = distance <= np.abs(r1 - r2)
    area[complete_overlap] = np.pi * np.minimum(r1, r2)**2
    
    # Case 3: Partial overlap
    partial_overlap = ~(no_overlap | complete_overlap)
    d = distance[partial_overlap]
    alpha = np.arccos((d**2 + r1**2 - r2**2) / (2 * d * r1))
    beta = np.arccos((d**2 + r2**2 - r1**2) / (2 * d * r2))
    area1 = r1**2 * alpha
    area2 = r2**2 * beta
    area3 = 0.5 * np.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
    area[partial_overlap] = area1 + area2 - area3
    
    return area 