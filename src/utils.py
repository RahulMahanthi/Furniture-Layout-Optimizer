import json
import pickle
import numpy as np
from src.room import Room, Furniture

def load_model(model_path):
    """Load the trained machine learning model"""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def save_room_layout(room, filename):
    """Save room layout to JSON file"""
    room_data = {
        'name': room.name,
        'length': room.length,
        'width': room.width,
        'fixed_elements': room.fixed_elements,
        'furniture': [f.to_dict() for f in room.furniture]
    }
    
    with open(filename, 'w') as f:
        json.dump(room_data, f, indent=4)
        
def load_room_layout(filename):
    """Load room layout from JSON file"""
    with open(filename, 'r') as f:
        room_data = json.load(f)
    
    # Create room
    room = Room(length=room_data['length'], width=room_data['width'], name=room_data['name'])
    
    # Add fixed elements
    for element in room_data['fixed_elements']:
        room.add_fixed_element(element)
    
    # Add furniture
    for furn_data in room_data['furniture']:
        furn = Furniture(
            name=furn_data['name'], 
            width=furn_data['width'], 
            length=furn_data['length'],
            movable=furn_data['movable'],
            x=furn_data['x'],
            y=furn_data['y'],
            orientation=furn_data['orientation']
        )
        room.add_furniture(furn)
    
    return room

def create_feature_vector(room):
    """Create feature vector for a room to use with the trained model"""
    # Extract features similar to those used during training
    features = [
        room.length,
        room.width,
        room.length * room.width,  # area
        len(room.furniture),
        len(room.fixed_elements),
    ]
    
    # Calculate furniture density
    furniture_area = sum(f.width * f.length for f in room.furniture)
    room_area = room.length * room.width
    furniture_density = furniture_area / room_area
    free_space = 1 - furniture_density
    
    # Calculate wall distances
    wall_distances = []
    for furn in room.furniture:
        dist_left = furn.x
        dist_right = room.length - (furn.x + furn.length)
        dist_top = furn.y
        dist_bottom = room.width - (furn.y + furn.width)
        min_wall_dist = min(dist_left, dist_right, dist_top, dist_bottom)
        wall_distances.append(min_wall_dist)
    
    avg_wall_distance = sum(wall_distances) / len(wall_distances) if wall_distances else 0
    
    # Calculate walkability
    grid = room.get_grid_representation(grid_size=10)
    empty_cells = np.sum(grid == 0)
    total_cells = grid.size
    walkability = empty_cells / total_cells
    
    # Add to features
    features.extend([
        furniture_density,
        free_space,
        avg_wall_distance,
        walkability
    ])
    
    # Add furniture type counts
    furniture_types = set(f.name for f in room.furniture)
    features.append(len(furniture_types))
    
    # Calculate furniture-to-furniture distances (average)
    furniture_coords = [(f.x + f.length/2, f.y + f.width/2) for f in room.furniture]
    avg_distance = 0
    if len(furniture_coords) > 1:
        distances = []
        for i in range(len(furniture_coords)):
            for j in range(i+1, len(furniture_coords)):
                x1, y1 = furniture_coords[i]
                x2, y2 = furniture_coords[j]
                dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                distances.append(dist)
        avg_distance = sum(distances) / len(distances)
    features.append(avg_distance)
    
    return np.array(features).reshape(1, -1)  # Reshape for single prediction

def evaluate_layout(model, room):
    """Evaluate a room layout using the trained model"""
    features = create_feature_vector(room)
    prediction = model.predict(features)[0]
    
    # Get probability if the model supports predict_proba
    try:
        probability = model.predict_proba(features)[0][1]  # Probability of class 1 (valid)
        return prediction, probability
    except:
        return prediction, None
        
def get_furniture_templates():
    """Return common furniture templates with typical dimensions"""
    return [
        {'name': 'Bed', 'width': 1.5, 'length': 2.0, 'movable': True},
        {'name': 'Sofa', 'width': 0.9, 'length': 2.2, 'movable': True},
        {'name': 'Table', 'width': 0.8, 'length': 1.2, 'movable': True},
        {'name': 'Chair', 'width': 0.5, 'length': 0.5, 'movable': True},
        {'name': 'Dresser', 'width': 0.5, 'length': 1.2, 'movable': True},
        {'name': 'Desk', 'width': 0.7, 'length': 1.4, 'movable': True},
        {'name': 'TV Stand', 'width': 0.4, 'length': 1.5, 'movable': True},
        {'name': 'Bookshelf', 'width': 0.4, 'length': 0.8, 'movable': True},
    ]

def get_fixed_element_templates():
    """Return common fixed element templates"""
    return [
        {'name': 'Door', 'width': 0.2, 'length': 0.9},
        {'name': 'Window', 'width': 0.1, 'length': 1.2},
    ]