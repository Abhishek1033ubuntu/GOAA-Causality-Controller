import numpy as np

def run_global_6_station_triangulation():
    print("=================================================================")
    print("    ACTIVATING 6-NODE GLOBAL TRIANGULATION MAPPING MATRIX        ")
    print("=================================================================")
    
    c = 299792.458 # Speed of light in km/s
    
    # 1. Define the True 3D Physical Geography of the Array
    stations = {
        'Station_A_Europe':    np.array([4200.0, 0.0, 4800.0]),
        'Station_B_Americas':  np.array([-4800.0, -2800.0, 3000.0]),
        'Station_C_Australia': np.array([-3900.0, 3000.0, -4200.0]),
        'Station_D_Africa':     np.array([4500.0, 1500.0, 500.0]),
        'Station_E_EastAsia':  np.array([1200.0, 5500.0, 3100.0]),
        'Station_F_Antarctica':np.array([0.0, 0.0, -6300.0])
    }
    
    # 2. Define an arbitrary Target Origin Source in Deep Space
    # This is the true direction vector of our cosmic phenomenon
    true_source_vector = np.array([0.267, -0.535, 0.802])
    true_source_vector /= np.linalg.norm(true_source_vector) # Normalize to a unit vector
    
    print(f"[CELESTIAL] Target Vector Source Orientation: {true_source_vector}")
    
    # 3. Calculate True Physical Arrival Times at each station relative to Earth center
    arrival_times = {}
    for name, coords in stations.items():
        # Projection of station coordinates onto the incoming wave vector divided by c
        arrival_times[name] = np.dot(coords, true_source_vector) / c
        
    # 4. Generate Relative Time Delays (Using Station A Europe as the central master clock)
    master_station = 'Station_A_Europe'
    relative_delays = []
    station_matrix = []
    
    for name, coords in stations.items():
        if name == master_station:
            continue
        # dt = t_target - t_master
        dt = arrival_times[name] - arrival_times[master_station]
        relative_delays.append(dt)
        
        # Geometry matrix baseline: Row = (Station_i - Station_Master)
        baseline_diff = coords - stations[master_station]
        station_matrix.append(baseline_diff)
        
    relative_delays = np.array(relative_delays)
    station_matrix = np.array(station_matrix)
    
    # 5. THE 3D LEAST-SQUARES INVERSION SOLVER
    # We invert the geometry matrix to map relative time delays back into spatial vector components:
    # Matrix * Vector = c * Delays  -->  Vector = Inverse(Matrix) * c * Delays
    b_vector = c * relative_delays
    
    # Perform Singular Value Decomposition (SVD) Pseudo-Inverse for maximum numerical stability
    calculated_source_vector, residuals, rank, s = np.linalg.lstsq(station_matrix, b_vector, rcond=None)
    
    # Ensure the calculated tracking vector is perfectly normalized
    calculated_source_vector /= np.linalg.norm(calculated_source_vector)
    
    # 6. Calculate Spatial Tracking Error
    spatial_reconstruction_error = np.linalg.norm(true_source_vector - calculated_source_vector)
    
    print("\n------------------- TRIANGULATION MATRIX AUDIT ------------------")
    print(f" Target Direction Vector:     {true_source_vector}")
    print(f" Reconstructed Server Vector: {calculated_source_vector}")
    print(f" Absolute Vector Variance:    {spatial_reconstruction_error:.9f}")
    print("-----------------------------------------------------------------")
    
    if spatial_reconstruction_error < 1e-5:
        print(" STATUS: GLOBAL OMNIDIRECTIONAL COORDINATE LOCK SECURED!")
        print(" Central server successfully pinpointed source coordinates via 6-node SVD inversion.")
    else:
        print(" STATUS: GEOMETRIC DRIFT DETECTED")
    print("=================================================================")

# Run the global triangulation pipeline
run_global_6_station_triangulation()
