import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

from src.room import Room, Furniture
from src.optimizer import optimize_room_layout
from src.visualization import create_room_image, create_furniture_legend
from src.utils import (
    get_furniture_templates, 
    get_fixed_element_templates,
    save_room_layout
)

# Set page config
st.set_page_config(
    page_title="Furniture Layout Optimizer",
    page_icon="🪑",
    layout="wide"
)

# Create necessary directories
os.makedirs("outputs", exist_ok=True)

def main():
    st.title("🪑 Furniture Layout Optimizer")
    
    st.sidebar.header("Room Configuration")
    
    # Room dimensions
    st.sidebar.subheader("Room Dimensions")
    room_length = st.sidebar.slider("Room Length (meters)", 2.0, 10.0, 5.0, 0.1)
    room_width = st.sidebar.slider("Room Width (meters)", 2.0, 8.0, 4.0, 0.1)
    
    # Fixed elements
    st.sidebar.subheader("Fixed Elements (Doors/Windows)")
    fixed_elements = []
    
    templates = get_fixed_element_templates()
    num_fixed_elements = st.sidebar.number_input("Number of fixed elements", 0, 5, 1)
    
    for i in range(num_fixed_elements):
        st.sidebar.markdown(f"**Fixed Element {i+1}**")
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            element_type = st.selectbox(
                f"Type {i+1}", 
                ["Door", "Window"],
                key=f"fixed_type_{i}"
            )
        
        # Get default dimensions from template
        default_template = next((t for t in templates if t['name'] == element_type), templates[0])
        
        with col2:
            wall = st.selectbox(
                f"Wall {i+1}", 
                ["Top", "Right", "Bottom", "Left"],
                key=f"wall_{i}"
            )
        
        # Auto position based on wall
        if wall == "Top":
            default_x = room_length / 2 - default_template['length'] / 2
            default_y = 0.0  # Ensure this is a float, not a list
        elif wall == "Right":
            default_x = room_length - default_template['width']
            default_y = room_width / 2 - default_template['length'] / 2
        elif wall == "Bottom":
            default_x = room_length / 2 - default_template['length'] / 2
            default_y = room_width - default_template['width']
        else:  # Left
            default_x = 0.0
            default_y = room_width / 2 - default_template['length'] / 2
            
        # Position sliders
        position_col1, position_col2 = st.sidebar.columns(2)
        with position_col1:
            # Ensure all values are floats
            x_position = st.slider(
                f"X Position {i+1}", 
                min_value=0.0, 
                max_value=float(max(0.1, room_length - default_template['length'])), 
                value=float(default_x),
                step=0.1,
                key=f"x_pos_{i}"
            )
        with position_col2:
            # Ensure all values are floats
            y_position = st.slider(
                f"Y Position {i+1}", 
                min_value=0.0, 
                max_value=float(max(0.1, room_width - default_template['width'])), 
                value=float(default_y),
                step=0.1,
                key=f"y_pos_{i}"
            )
            
        fixed_elements.append({
            'name': element_type,
            'x': x_position,
            'y': y_position,
            'width': default_template['width'],
            'length': default_template['length']
        })
        
    # Furniture selection
    st.sidebar.subheader("Furniture")
    furniture_templates = get_furniture_templates()
    
    # Select furniture items
    selected_furniture = []
    st.sidebar.markdown("**Select Furniture Items**")
    
    for template in furniture_templates:
        count = st.sidebar.number_input(
            f"{template['name']} (count)", 
            0, 5, 
            0 if template['name'] not in ['Bed', 'Sofa'] else 1,
            key=f"count_{template['name']}"
        )
        
        for j in range(count):
            selected_furniture.append(template.copy())
    
    # Optimization parameters
    st.sidebar.subheader("Optimization Settings")
    generations = st.sidebar.slider("Generations", 10, 500, 100)
    population_size = st.sidebar.slider("Population Size", 10, 200, 50)
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Room Preview")
        
        # Create an empty room with fixed elements
        preview_room = Room(
            length=room_length,
            width=room_width,
            name="Room Preview"
        )
        
        for element in fixed_elements:
            preview_room.add_fixed_element(element)
        
        # Display room
        if selected_furniture:
            st.write("Room with fixed elements (doors, windows)")
        else:
            st.write("Add furniture items using the sidebar")
            
        # Create and display the room image
        room_img = create_room_image(preview_room)
        st.image(room_img, channels="BGR", use_column_width=True)
        
    with col2:
        st.subheader("Selected Furniture")
        if not selected_furniture:
            st.write("No furniture selected")
        else:
            for i, item in enumerate(selected_furniture):
                st.write(f"{i+1}. {item['name']} ({item['length']}m × {item['width']}m)")
        
        # Display color legend
        legend_img = create_furniture_legend()
        st.image(legend_img, channels="BGR", width=250)
    
    # Run optimization
    if st.button("Optimize Layout") and selected_furniture:
        with st.spinner("Optimizing furniture layout..."):
            progress_bar = st.progress(0)
            
            # Run the optimization
            optimized_room, best_layout, fitness, fitness_history = optimize_room_layout(
                room_length=room_length,
                room_width=room_width,
                furniture_config=selected_furniture,
                fixed_elements=fixed_elements,
                generations=generations,
                population_size=population_size
            )
            
            # Update progress bar
            for i in range(100):
                progress_bar.progress(i + 1)
                time.sleep(0.01)
            
            # Display results
            st.success(f"Optimization completed! Final fitness score: {fitness:.2f}")
            
            # Show optimized layout
            st.subheader("Optimized Layout")
            optimized_img = create_room_image(optimized_room)
            st.image(optimized_img, channels="BGR", use_column_width=True)
            
            # Plot fitness history
            st.subheader("Optimization Progress")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(fitness_history)
            ax.set_title('Fitness Score Over Generations')
            ax.set_xlabel('Generation')
            ax.set_ylabel('Fitness Score')
            ax.grid(True)
            st.pyplot(fig)
            
            # Display furniture positions in a table
            st.subheader("Furniture Positions")
            furniture_data = []
            for furn in best_layout:
                furniture_data.append({
                    'Name': furn.name,
                    'X Position': f"{furn.x:.2f}m",
                    'Y Position': f"{furn.y:.2f}m",
                    'Dimensions': f"{furn.length:.2f}m × {furn.width:.2f}m",
                    'Orientation': f"{furn.orientation}°"
                })
            
            st.table(pd.DataFrame(furniture_data))
            
            # Save layout
            save_path = f"outputs/optimized_layout_{int(time.time())}.json"
            save_room_layout(optimized_room, save_path)
            st.success(f"Layout saved to {save_path}")
    
    # Footer
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This application uses a genetic algorithm to optimize furniture layouts. It takes into account:
    
    - Room dimensions
    - Fixed elements like doors and windows
    - Furniture placement constraints
    - Walkability and space utilization
    
    The optimization process starts with random layouts and evolves better solutions over generations.
    """)

if __name__ == "__main__":
    main()