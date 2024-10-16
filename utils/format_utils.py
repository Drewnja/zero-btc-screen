def format_hash_rate(rate):
    return f"{rate / 1e18:.1f}"  # Convert to EH/s and format to 1 decimal place

def format_difficulty(diff):
    return f"{diff / 1e12:.2f}"  # Convert to trillions and format to 2 decimal places

