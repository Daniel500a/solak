# solak

Region Finder - Find regions in images by comparing a view with a minimap.

## Description

This tool allows you to find a region's location by comparing a view image with a minimap image. It uses computer vision techniques to match the view within the minimap and returns the position and confidence of the match.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Daniel500a/solak.git
cd solak
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python region_finder.py <view_image> <minimap_image> [output_image]
```

**Example:**
```bash
python region_finder.py view.jpg minimap.jpg result.jpg
```

### Python API

```python
from region_finder import RegionFinder

# Create a finder instance
finder = RegionFinder(threshold=0.7)

# Find region using file paths
result = finder.find_region('view.jpg', 'minimap.jpg')

if result and result['found']:
    print(f"Region found at position: {result['position']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    # Visualize the match
    finder.visualize_match('minimap.jpg', result, 'output.jpg')
else:
    print("Region not found")

# Or use numpy arrays directly
import cv2
view = cv2.imread('view.jpg')
minimap = cv2.imread('minimap.jpg')
result = finder.find_region_from_images(view, minimap)
```

## Features

- **Template Matching**: Uses OpenCV's template matching to find regions
- **Configurable Threshold**: Adjust matching sensitivity
- **Visualization**: Generate images showing the matched region
- **Multiple Input Methods**: Accept file paths or numpy arrays

## Result Format

When a region is found, the result dictionary contains:

```python
{
    'found': True,
    'confidence': 0.95,  # Match confidence (0-1)
    'position': {
        'x': 100,        # X coordinate of top-left corner
        'y': 150,        # Y coordinate of top-left corner
        'width': 200,    # Width of matched region
        'height': 150    # Height of matched region
    },
    'top_left': (100, 150),
    'bottom_right': (300, 300)
}
```

## Testing

Run the test suite:

```bash
python -m unittest test_region_finder.py
```

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy
- Pillow

## License

MIT