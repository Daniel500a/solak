"""
Region Finder - Find region location from view and minimap images
"""
import cv2
import numpy as np
from typing import Tuple, Optional, Dict


class RegionFinder:
    """
    Class to find and match regions between a view image and a minimap.
    """
    
    def __init__(self, threshold: float = 0.7):
        """
        Initialize RegionFinder.
        
        Args:
            threshold: Matching threshold (0-1), higher means stricter matching
        """
        self.threshold = threshold
    
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load an image from file path.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Image as numpy array or None if loading fails
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not load image from {image_path}")
                return None
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def find_region(self, view_image_path: str, minimap_image_path: str) -> Optional[Dict]:
        """
        Find the region in the minimap that corresponds to the view image.
        
        Args:
            view_image_path: Path to the main view image
            minimap_image_path: Path to the minimap image
            
        Returns:
            Dictionary with region information or None if not found
        """
        # Load images
        view = self.load_image(view_image_path)
        minimap = self.load_image(minimap_image_path)
        
        if view is None or minimap is None:
            return None
        
        # Convert to grayscale for template matching
        view_gray = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY)
        minimap_gray = cv2.cvtColor(minimap, cv2.COLOR_BGR2GRAY)
        
        # Try to find the view in the minimap using template matching
        result = cv2.matchTemplate(minimap_gray, view_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Check if match is good enough
        if max_val >= self.threshold:
            # Get dimensions
            h, w = view_gray.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            
            return {
                'found': True,
                'confidence': float(max_val),
                'position': {
                    'x': int(top_left[0]),
                    'y': int(top_left[1]),
                    'width': int(w),
                    'height': int(h)
                },
                'top_left': top_left,
                'bottom_right': bottom_right
            }
        else:
            return {
                'found': False,
                'confidence': float(max_val),
                'message': f'No match found with confidence >= {self.threshold}'
            }
    
    def find_region_from_images(self, view: np.ndarray, minimap: np.ndarray) -> Optional[Dict]:
        """
        Find the region in the minimap that corresponds to the view image.
        This method accepts numpy arrays directly.
        
        Args:
            view: Main view image as numpy array
            minimap: Minimap image as numpy array
            
        Returns:
            Dictionary with region information or None if not found
        """
        if view is None or minimap is None:
            return None
        
        # Convert to grayscale for template matching
        view_gray = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY) if len(view.shape) == 3 else view
        minimap_gray = cv2.cvtColor(minimap, cv2.COLOR_BGR2GRAY) if len(minimap.shape) == 3 else minimap
        
        # Try to find the view in the minimap using template matching
        result = cv2.matchTemplate(minimap_gray, view_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Check if match is good enough
        if max_val >= self.threshold:
            # Get dimensions
            h, w = view_gray.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            
            return {
                'found': True,
                'confidence': float(max_val),
                'position': {
                    'x': int(top_left[0]),
                    'y': int(top_left[1]),
                    'width': int(w),
                    'height': int(h)
                },
                'top_left': top_left,
                'bottom_right': bottom_right
            }
        else:
            return {
                'found': False,
                'confidence': float(max_val),
                'message': f'No match found with confidence >= {self.threshold}'
            }
    
    def visualize_match(self, minimap_image_path: str, region_info: Dict, output_path: str = 'result.jpg') -> bool:
        """
        Visualize the matched region on the minimap and save to file.
        
        Args:
            minimap_image_path: Path to the minimap image
            region_info: Region information from find_region
            output_path: Path to save the visualization
            
        Returns:
            True if successful, False otherwise
        """
        if not region_info or not region_info.get('found'):
            print("No valid region to visualize")
            return False
        
        minimap = self.load_image(minimap_image_path)
        if minimap is None:
            return False
        
        # Draw rectangle on the minimap
        top_left = region_info['top_left']
        bottom_right = region_info['bottom_right']
        cv2.rectangle(minimap, top_left, bottom_right, (0, 255, 0), 2)
        
        # Add confidence text
        confidence = region_info['confidence']
        text = f"Match: {confidence:.2%}"
        cv2.putText(minimap, text, (top_left[0], top_left[1] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save result
        try:
            cv2.imwrite(output_path, minimap)
            print(f"Visualization saved to {output_path}")
            return True
        except Exception as e:
            print(f"Error saving visualization: {e}")
            return False


def main():
    """
    Main function demonstrating usage.
    """
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python region_finder.py <view_image> <minimap_image> [output_image]")
        print("\nExample:")
        print("  python region_finder.py view.jpg minimap.jpg result.jpg")
        sys.exit(1)
    
    view_path = sys.argv[1]
    minimap_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else 'result.jpg'
    
    # Create finder instance
    finder = RegionFinder(threshold=0.6)
    
    # Find region
    print(f"Searching for region in minimap...")
    print(f"View image: {view_path}")
    print(f"Minimap image: {minimap_path}")
    
    result = finder.find_region(view_path, minimap_path)
    
    if result and result.get('found'):
        print(f"\n✓ Region found!")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Position: x={result['position']['x']}, y={result['position']['y']}")
        print(f"  Size: {result['position']['width']}x{result['position']['height']}")
        
        # Visualize the match
        finder.visualize_match(minimap_path, result, output_path)
    else:
        print(f"\n✗ Region not found")
        if result:
            print(f"  Best confidence: {result['confidence']:.2%}")
            print(f"  {result.get('message', '')}")


if __name__ == "__main__":
    main()
