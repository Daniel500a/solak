"""
Example script demonstrating the RegionFinder usage.
Creates sample images and demonstrates finding regions.
"""
import cv2
import numpy as np
import os
import sys

# Add parent directory to path to import region_finder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from region_finder import RegionFinder


def create_sample_images():
    """Create sample minimap and view images for demonstration"""
    
    # Get the examples directory path
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a minimap (like a game map)
    minimap = np.ones((400, 400, 3), dtype=np.uint8) * 200
    
    # Add some map features (roads, buildings, etc.)
    # Roads
    cv2.line(minimap, (50, 0), (50, 400), (150, 150, 150), 10)
    cv2.line(minimap, (0, 100), (400, 100), (150, 150, 150), 10)
    cv2.line(minimap, (200, 0), (200, 400), (150, 150, 150), 8)
    
    # Buildings/landmarks
    cv2.rectangle(minimap, (80, 120), (120, 160), (100, 100, 200), -1)
    cv2.rectangle(minimap, (220, 240), (280, 300), (200, 100, 100), -1)
    cv2.circle(minimap, (300, 100), 20, (100, 200, 100), -1)
    cv2.circle(minimap, (150, 300), 15, (100, 150, 200), -1)
    
    # Add some texture
    for i in range(0, 400, 20):
        for j in range(0, 400, 20):
            if (i + j) % 40 == 0:
                cv2.circle(minimap, (i, j), 2, (180, 180, 180), -1)
    
    # Create a view that shows a portion of the minimap
    # This simulates what the player/user sees
    view_x, view_y = 180, 220
    view_width, view_height = 100, 80
    view = minimap[view_y:view_y+view_height, view_x:view_x+view_width].copy()
    
    # Save the images
    minimap_path = os.path.join(examples_dir, 'minimap.jpg')
    view_path = os.path.join(examples_dir, 'view.jpg')
    cv2.imwrite(minimap_path, minimap)
    cv2.imwrite(view_path, view)
    
    print("Sample images created:")
    print(f"  - {minimap_path} (400x400)")
    print(f"  - {view_path} (100x80)")
    print(f"  - View extracted from position: ({view_x}, {view_y})")
    
    return view_x, view_y, minimap_path, view_path, examples_dir


def main():
    """Main demonstration"""
    print("=" * 60)
    print("Region Finder - Example Demonstration")
    print("=" * 60)
    print()
    
    # Create sample images
    print("Step 1: Creating sample images...")
    expected_x, expected_y, minimap_path, view_path, examples_dir = create_sample_images()
    print()
    
    # Create RegionFinder instance
    print("Step 2: Initializing RegionFinder...")
    finder = RegionFinder(threshold=0.7)
    print(f"  - Threshold: {finder.threshold}")
    print()
    
    # Find the region
    print("Step 3: Finding region in minimap...")
    result = finder.find_region(view_path, minimap_path)
    print()
    
    # Display results
    print("Step 4: Results")
    print("-" * 60)
    if result and result['found']:
        print("✓ Region successfully found!")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Position: ({result['position']['x']}, {result['position']['y']})")
        print(f"  Size: {result['position']['width']}x{result['position']['height']}")
        print(f"  Expected position: ({expected_x}, {expected_y})")
        
        # Check accuracy
        x_diff = abs(result['position']['x'] - expected_x)
        y_diff = abs(result['position']['y'] - expected_y)
        print(f"  Position accuracy: ±{x_diff}px horizontal, ±{y_diff}px vertical")
        
        # Visualize the match
        print()
        print("Step 5: Creating visualization...")
        result_path = os.path.join(examples_dir, 'result.jpg')
        finder.visualize_match(minimap_path, result, result_path)
        print(f"  Visualization saved to {result_path}")
        print()
        print("✓ Example completed successfully!")
    else:
        print("✗ Region not found")
        if result:
            print(f"  Best confidence: {result['confidence']:.2%}")
            print(f"  {result.get('message', '')}")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
