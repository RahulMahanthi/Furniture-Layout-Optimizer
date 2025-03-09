import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import cv2

def get_color_for_furniture(furniture_name):
    """Return a color for different furniture types"""
    color_map = {
        'Bed': [0, 0, 255],      # Red
        'Sofa': [0, 255, 0],     # Green
        'Table': [255, 0, 0],    # Blue
        'Chair': [255, 255, 0],  # Cyan
        'Dresser': [255, 0, 255],# Magenta
        'Desk': [0, 255, 255],   # Yellow
        'Bookshelf': [128, 128, 0], # Dark cyan
        'TV Stand': [0, 128, 128]   # Dark red
    }
    
    return color_map.get(furniture_name, [200, 200, 200])  # Default gray

def create_room_image(room, resolution=50):
    """Create a colored image of the room layout using OpenCV"""
    # Create an empty image (white background)
    width_px = int(room.width * resolution)
    length_px = int(room.length * resolution)
    img = np.ones((width_px, length_px, 3), dtype=np.uint8) * 255
    
    # Draw fixed elements (doors, windows) in gray
    for element in room.fixed_elements:
        x1 = int(element['x'] * resolution)
        y1 = int(element['y'] * resolution)
        x2 = int((element['x'] + element['width']) * resolution)
        y2 = int((element['y'] + element['length']) * resolution)
        
        if element['name'] == 'Door':
            color = (150, 150, 150)  # Dark gray
        else:  # Window or other
            color = (200, 200, 200)  # Light gray
            
        cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        
        # Add text label
        cv2.putText(img, element['name'], (x1, y1-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Draw furniture with different colors
    for furniture in room.furniture:
        x1 = int(furniture.x * resolution)
        y1 = int(furniture.y * resolution)
        x2 = int((furniture.x + furniture.length) * resolution)
        y2 = int((furniture.y + furniture.width) * resolution)
        
        # Get color from name
        color = get_color_for_furniture(furniture.name)
        rgb_color = (int(color[2]), int(color[1]), int(color[0]))  # BGR to RGB
        
        cv2.rectangle(img, (x1, y1), (x2, y2), rgb_color, -1)
        
        # Add text label
        cv2.putText(img, furniture.name, (x1, y1-5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    # Draw room outline
    cv2.rectangle(img, (0, 0), (length_px-1, width_px-1), (0, 0, 0), 2)
    
    return img

def plot_to_image(fig):
    """Convert a matplotlib figure to an image"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str

def create_furniture_legend():
    """Create a legend image that shows the color coding for furniture types"""
    width, height = 300, 250
    legend = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    furniture_types = [
        'Bed', 'Sofa', 'Table', 'Chair', 'Dresser', 'Desk', 'Bookshelf', 'TV Stand'
    ]
    
    y_pos = 30
    for furniture in furniture_types:
        color = get_color_for_furniture(furniture)
        rgb_color = (int(color[2]), int(color[1]), int(color[0]))  # BGR to RGB
        
        # Draw rectangle for color sample
        cv2.rectangle(legend, (20, y_pos), (50, y_pos+20), rgb_color, -1)
        
        # Add text label
        cv2.putText(legend, furniture, (60, y_pos+15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        y_pos += 30
    
    cv2.putText(legend, "Legend", (20, 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    return legend