import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Room class to store room dimensions and furniture
class Room:
    def __init__(self, length, width, name="Room"):
        self.length = length
        self.width = width
        self.name = name
        self.furniture = []
        self.fixed_elements = []  # windows, doors, etc.
        
    def add_furniture(self, furniture):
        self.furniture.append(furniture)
        
    def add_fixed_element(self, element):
        self.fixed_elements.append(element)
        
    def get_grid_representation(self, grid_size=20):
        """Convert room to grid representation"""
        grid = np.zeros((int(self.width * grid_size), int(self.length * grid_size)))
        
        # Add fixed elements to grid (value = 1)
        for element in self.fixed_elements:
            x1 = int(element['x'] * grid_size)
            y1 = int(element['y'] * grid_size)
            x2 = int((element['x'] + element['width']) * grid_size)
            y2 = int((element['y'] + element['length']) * grid_size)
            grid[y1:y2, x1:x2] = 1
        
        # Add furniture to grid (value = 2)
        for furn in self.furniture:
            x1 = int(furn.x * grid_size)
            y1 = int(furn.y * grid_size)
            x2 = int((furn.x + furn.width) * grid_size)
            y2 = int((furn.y + furn.length) * grid_size)
            grid[y1:y2, x1:x2] = 2
            
        return grid
        
    def visualize(self, grid_size=20, return_fig=False):
        """Visualize room layout"""
        grid = self.get_grid_representation(grid_size)
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(grid, cmap=['white', 'black', 'blue'], vmin=0, vmax=2, cbar=False, ax=ax)
        ax.set_title(f"{self.name} Layout")
        
        if return_fig:
            return fig
        else:
            plt.show()
            
    def to_dict(self):
        """Convert room to dictionary for API responses"""
        return {
            'name': self.name,
            'length': self.length,
            'width': self.width,
            'furniture': [f.to_dict() for f in self.furniture],
            'fixed_elements': self.fixed_elements
        }

# Furniture class
class Furniture:
    def __init__(self, name, width, length, movable=True, x=0, y=0, orientation=0):
        self.name = name
        self.width = width
        self.length = length
        self.movable = movable
        self.x = x  # x-coordinate in the room
        self.y = y  # y-coordinate in the room
        self.orientation = orientation  # 0: normal, 90: rotated
        
    def set_position(self, x, y, orientation=None):
        self.x = x
        self.y = y
        if orientation is not None:
            self.orientation = orientation
            
    def rotate(self):
        """Rotate furniture by 90 degrees"""
        self.orientation = (self.orientation + 90) % 360
        # Swap width and length if orientation is 90 or 270
        if self.orientation == 90 or self.orientation == 270:
            self.width, self.length = self.length, self.width
            
    def to_dict(self):
        return {
            'name': self.name,
            'width': self.width,
            'length': self.length,
            'movable': self.movable,
            'x': self.x,
            'y': self.y,
            'orientation': self.orientation
        }