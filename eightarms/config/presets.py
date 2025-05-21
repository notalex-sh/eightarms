# store presets

SPEED_PRESETS = {
    'slow': {
        'min_delay': 3.0,
        'max_delay': 6.0,
        'batch_delay': 2.0,
        'max_pages': 5,
        'commits': 'all',
        'multithreaded': False,
        'max_workers': 1,
        'description': 'Thorough scan with polite delays'
    },
    
    'medium': {
        'min_delay': 0.5,
        'max_delay': 1.5,
        'batch_delay': 0.3,
        'max_pages': 3,
        'commits': [10, 10],
        'multithreaded': True,
        'max_workers': 4,
        'description': 'Balanced speed and thoroughness'
    },
    
    'fast': {
        'min_delay': 0.2,
        'max_delay': 0.8,
        'batch_delay': 0.1,
        'max_pages': 2,
        'commits': [5, 5],
        'multithreaded': True,
        'max_workers': 6,
        'description': 'Quick scan with minimal delays'
    }
}


def get_speed_preset(speed_name: str) -> dict:
    if speed_name not in SPEED_PRESETS:
        raise ValueError(f"Unknown speed preset: {speed_name}. Available: {list(SPEED_PRESETS.keys())}")
    
    return SPEED_PRESETS[speed_name].copy()


def list_speed_presets() -> dict:
    return SPEED_PRESETS.copy()