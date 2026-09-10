import numpy as np
from scipy.signal import butter, filtfilt, correlate

def apply_highpass_filter(data, sample_rate, cutoff_freq):
    """
    Applies a DSP Butterworth high-pass filter to strip out low-frequency 
    terrestrial noise (like AC power line hum and local geological rumbling).
    """
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist
    # 4th order Butterworth filter
    b, a = butter(4, normal_cutoff, btype='high', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def compute_cross_correlation(signal_a, signal_b, sample_rate):
    """
    Performs standard time-domain cross-correlation to find the raw sample 
    delay between two global tracking nodes.
    """
    # Compute cross-correlation
    correlation = correlate(signal_a, signal_b, mode='full')
    
    # Create lag array
    lags = np.arange(-len(signal_a) + 1, len(signal_a))
    
    # Find the peak correlation index
    peak_index = np.argmax(correlation)
    sample_lag = lags[peak_index]
    
    # Convert sample lag to milliseconds
    time_lag_ms = (sample_lag / sample_rate) * 1000.0
    
    return time_lag_ms, correlation

def run_pipeline_diagnostic():
    print("=================================================================")
    print("    GOAA SIGNAL PROCESSOR: CORE PIPELINE DIAGNOSTIC              ")
    print("=================================================================")
    
    sample_rate = 4096  # Hz
    duration = 1.0      # Seconds
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    print("[DSP] Generating simulated noisy telemetry streams...")
    # Generate a clean synthetic transient (a simple Gaussian pulse for testing)
    clean_signal = np.exp(-0.5 * ((t - 0.5) / 0.01)**2)
    
    # Inject heavy low-frequency noise (simulating environmental drift)
    noise_a = 0.5 * np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.2, len(t))
    noise_b = 0.5 * np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.2, len(t))
    
    # Simulate a time delay for Station B (approx 20.5 ms lag)
    shift_samples = int(0.0205 * sample_rate)
    clean_signal_b = np.roll(clean_signal, shift_samples)
    
    raw_station_a = clean_signal + noise_a
    raw_station_b = clean_signal_b + noise_b
    
    print("[DSP] Applying high-pass filters (Cutoff: 20 Hz)...")
    filtered_a = apply_highpass_filter(raw_station_a, sample_rate, cutoff_freq=20.0)
    filtered_b = apply_highpass_filter(raw_station_b, sample_rate, cutoff_freq=20.0)
    
    print("[MATH] Computing baseline cross-correlation...")
    lag_ms, _ = compute_cross_correlation(filtered_a, filtered_b, sample_rate)
    
    print("\n------------------- CORE PIPELINE RESULTS -----------------------")
    print(f" Target Synthetic Lag:      20.500 ms")
    print(f" Extracted Correlated Lag:  {abs(lag_ms):.3f} ms")
    print("-----------------------------------------------------------------")
    
    if abs(abs(lag_ms) - 20.5) < 0.5:
        print(" STATUS: FILTERING AND CROSS-CORRELATION NOMINAL")
    else:
        print(" STATUS: DSP FAILURE - LAG OUT OF BOUNDS")
    print("=================================================================")

if __name__ == "__main__":
    run_pipeline_diagnostic()
