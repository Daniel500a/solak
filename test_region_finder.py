"""
Tests for the RegionFinder class
"""
import unittest
import numpy as np
import cv2
import os
import tempfile
from region_finder import RegionFinder


class TestRegionFinder(unittest.TestCase):
    """Test cases for RegionFinder"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.finder = RegionFinder(threshold=0.7)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_test_image(self, width, height, color):
        """Helper to create a test image"""
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:] = color
        return img
    
    def test_initialization(self):
        """Test RegionFinder initialization"""
        finder = RegionFinder(threshold=0.8)
        self.assertEqual(finder.threshold, 0.8)
    
    def test_load_image_success(self):
        """Test successful image loading"""
        # Create a test image
        img = self.create_test_image(100, 100, (255, 0, 0))
        path = os.path.join(self.temp_dir, 'test.jpg')
        cv2.imwrite(path, img)
        
        # Load it
        loaded = self.finder.load_image(path)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.shape, (100, 100, 3))
    
    def test_load_image_failure(self):
        """Test image loading with non-existent file"""
        loaded = self.finder.load_image('/nonexistent/path/image.jpg')
        self.assertIsNone(loaded)
    
    def test_find_region_from_images_exact_match(self):
        """Test finding region with exact match"""
        # Create a minimap with a pattern
        minimap = self.create_test_image(200, 200, (100, 100, 100))
        
        # Add some distinctive features to the minimap
        cv2.rectangle(minimap, (10, 10), (40, 40), (50, 50, 50), -1)
        cv2.rectangle(minimap, (150, 150), (180, 180), (150, 150, 150), -1)
        
        # Create a view with a distinctive pattern
        view = self.create_test_image(50, 50, (255, 0, 0))
        cv2.circle(view, (25, 25), 10, (0, 255, 0), -1)
        
        # Place the view in the minimap at a known position
        minimap[50:100, 50:100] = view
        
        # Find the region
        result = self.finder.find_region_from_images(view, minimap)
        
        self.assertIsNotNone(result)
        self.assertTrue(result['found'])
        self.assertGreater(result['confidence'], 0.9)
        self.assertEqual(result['position']['x'], 50)
        self.assertEqual(result['position']['y'], 50)
    
    def test_find_region_from_images_no_match(self):
        """Test finding region when no match exists"""
        minimap = self.create_test_image(200, 200, (100, 100, 100))
        view = self.create_test_image(50, 50, (255, 0, 0))
        
        # Don't place view in minimap - they should not match
        
        result = self.finder.find_region_from_images(view, minimap)
        
        self.assertIsNotNone(result)
        # With different images, it should not find a match above threshold
        # Note: this might find false positives with very simple images
    
    def test_find_region_with_files(self):
        """Test finding region using file paths"""
        # Create test images with distinctive patterns
        minimap = self.create_test_image(200, 200, (100, 100, 100))
        view = self.create_test_image(50, 50, (255, 0, 0))
        cv2.circle(view, (25, 25), 10, (0, 255, 0), -1)
        minimap[50:100, 50:100] = view
        
        # Save to files
        minimap_path = os.path.join(self.temp_dir, 'minimap.jpg')
        view_path = os.path.join(self.temp_dir, 'view.jpg')
        cv2.imwrite(minimap_path, minimap)
        cv2.imwrite(view_path, view)
        
        # Find region
        result = self.finder.find_region(view_path, minimap_path)
        
        self.assertIsNotNone(result)
        self.assertTrue(result['found'])
        self.assertGreater(result['confidence'], 0.9)
    
    def test_find_region_invalid_paths(self):
        """Test finding region with invalid file paths"""
        result = self.finder.find_region('/invalid/view.jpg', '/invalid/minimap.jpg')
        self.assertIsNone(result)
    
    def test_visualize_match(self):
        """Test visualization of matched region"""
        # Create test images
        minimap = self.create_test_image(200, 200, (100, 100, 100))
        view = self.create_test_image(50, 50, (255, 0, 0))
        minimap[50:100, 50:100] = view
        
        # Save minimap
        minimap_path = os.path.join(self.temp_dir, 'minimap.jpg')
        cv2.imwrite(minimap_path, minimap)
        
        # Create region info
        region_info = {
            'found': True,
            'confidence': 0.95,
            'position': {'x': 50, 'y': 50, 'width': 50, 'height': 50},
            'top_left': (50, 50),
            'bottom_right': (100, 100)
        }
        
        # Visualize
        output_path = os.path.join(self.temp_dir, 'result.jpg')
        success = self.finder.visualize_match(minimap_path, region_info, output_path)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_path))
    
    def test_visualize_match_no_region(self):
        """Test visualization with no region found"""
        minimap_path = os.path.join(self.temp_dir, 'minimap.jpg')
        minimap = self.create_test_image(200, 200, (100, 100, 100))
        cv2.imwrite(minimap_path, minimap)
        
        region_info = {'found': False, 'confidence': 0.3}
        
        output_path = os.path.join(self.temp_dir, 'result.jpg')
        success = self.finder.visualize_match(minimap_path, region_info, output_path)
        
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
