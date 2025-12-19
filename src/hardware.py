import platform
import re

def get_rpi_model():
    """
    Detects the Raspberry Pi model based on /proc/cpuinfo revision code.
    Returns a dictionary with model details.
    """
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read()
        
        # Extract revision
        match = re.search(r"Revision\s+:\s+([0-9a-f]+)", cpuinfo)
        if not match:
            return {"model": "Unknown", "type": "Unknown", "revision": "Unknown"}
        
        revision = match.group(1)
        
        # https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#new-style-revision-codes
        # We can implement a simplified lookup or just return the raw revision if unknown
        # For this requirement, we want to distinguish major families (Zero 2 W, 3, 4, 5)
        
        # Partial lookup table for common models
        # This is not exhaustive but covers the requested target hardware
        revisions = {
            # Pi Zero 2 W
            "902120": "Raspberry Pi Zero 2 W",
            
            # Pi 3 Model B
            "a02082": "Raspberry Pi 3 Model B",
            "a22082": "Raspberry Pi 3 Model B",
            "a32082": "Raspberry Pi 3 Model B",
            
            # Pi 3 Model B+
            "a020d3": "Raspberry Pi 3 Model B+",
            
            # Pi 4 Model B
            "a03111": "Raspberry Pi 4 Model B (1GB)",
            "b03111": "Raspberry Pi 4 Model B (2GB)",
            "c03111": "Raspberry Pi 4 Model B (4GB)",
            "d03111": "Raspberry Pi 4 Model B (8GB)",
            
            # Pi 5
            "c04170": "Raspberry Pi 5 (4GB)",
            "d04170": "Raspberry Pi 5 (8GB)",
        }
        
        # Fallback logic for new style codes if not in strict map
        # Bit-wise parsing could be added here for full robustness
        
        model_name = revisions.get(revision, f"Raspberry Pi (Revision: {revision})")
        
        # Determine family
        if "Zero 2 W" in model_name:
            family = "Zero"
        elif "Pi 3" in model_name:
            family = "3"
        elif "Pi 4" in model_name:
            family = "4"
        elif "Pi 5" in model_name:
            family = "5"
        else:
            family = "Unknown"
            
        return {
            "model": model_name,
            "family": family,
            "revision": revision,
            "arch": platform.machine()
        }
        
    except FileNotFoundError:
        # Not running on a Pi (e.g., dev machine)
        return {
            "model": "Non-Raspberry Pi Environment",
            "family": "Generic",
            "revision": "N/A",
            "arch": platform.machine()
        }

def is_raspberry_pi():
    """Checks if the system is a Raspberry Pi."""
    info = get_rpi_model()
    return info["family"] != "Generic"
