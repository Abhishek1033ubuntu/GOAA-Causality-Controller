import numpy as np
import matplotlib.pyplot as plt

def run_dynamic_chirp_generator():
    print("=================================================================")
    print("     INITIALIZING DYNAMIC COSMIC CHIRP SIGNAL GENERATOR         ")
    print("=================================================================")
    
    duration = 8.0  # 8-second observation window
    sample_rate = 5000
    timestamps = np.linspace(0, duration, int(duration * sample_rate))
    
    # 1. Planetary Array Coordinates (KM)
    stations = {
        'Station_A_Europe':    np.array([4200.0, 0.0, 4800.0]),
        'Station_B_Americas':  np.array([-4800.0, -2800.0, 3000.0]),
        'Station_C_Australia': np.array([-3900.0, 3000.0, -4200.0]),
    }
    
    c = 299792.458  # Speed of light
    wave_vector = np.array([0.6, 0.0, 0.8])
    wave_vector /= np.linalg.norm(wave_vector)
    
    print(f"[GENERATOR] Generating non-linear frequency sweep across global nodes...")
    
    # 2. THE CHIRP EQUATION: Frequency sweeps from 5Hz up to 45Hz dynamically
    f_start = 5.0
    f_end = 45.0
    
    # Calculate relative physical time delays for each node
    delays = {}
    for name, coords in stations.items():
        delays[name] = np.dot(coords, wave_vector) / c
        
    # 3. Generate Dynamic Wave Streams per Station
    chirp_streams = {}
    for name, dt in delays.items():
        # Shift the timeline by the specific station spatial delay
        t_shifted = timestamps - dt
        
        # Non-linear phase accumulation formula for a linear frequency chirp
        phase = 2 * np.pi * (f_start * t_shifted + ((f_end - f_start) / (2 * duration)) * (t_shifted ** 2))
        
        # Exponential amplitude envelope modeling the approach to collision
        amplitude_envelope = 0.05 + 0.2 * np.exp(t_shifted / duration)
        
        # Synthesize pure dynamic wave + baseline background noise
        pure_wave = amplitude_envelope * np.sin(phase)
        random_noise = np.random.normal(0, 0.3, len(timestamps))
        
        chirp_streams[name] = pure_wave + random_noise

    print("[GENERATOR OK] Dynamic event streams successfully broadcasted to hardware nodes.")
    
    # 4. VISUALIZING THE DYNAMIC ENVELOPE (Europe vs Americas)
    plt.figure(figsize=(12, 5))
    plt.plot(timestamps, chirp_streams['Station_A_Europe'], label='Europe Node (Alpha)', alpha=0.6, color='blue')
    plt.plot(timestamps, chirp_streams['Station_B_Americas'], label='Americas Node (Beta)', alpha=0.4, color='orange')
    
    plt.xlim([duration - 1.5, duration]) # Zoom into the final 1.5 seconds to see the dense chirp waves
    plt.title("GOAA Ingest: Accelerated Cosmic Chirp Waveforms (Final Approach View)", fontsize=12, fontweight='bold')
    plt.xlabel("Time Vectors (Seconds)")
    plt.ylabel("Raw Signal Strain + Noise")
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()
    
    print("=================================================================")

# Execute the dynamic broadcaster
run_dynamic_chirp_generator()
