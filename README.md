# 🏠 Furniture Layout Optimizer

An AI-powered system that automatically generates optimized furniture arrangements for interior spaces using genetic algorithms and machine learning.

## 📖 Overview

The **Furniture Layout Optimizer** tackles the challenging problem of efficiently arranging furniture in rooms while maintaining **practicality and aesthetics**. It uses a combination of **genetic algorithms** and **machine learning** to generate optimal furniture layouts based on:

- ✅ Room dimensions  
- ✅ Fixed elements (doors/windows)  
- ✅ Furniture requirements  


---

## ✨ Key Features

- ✅ **Automatic Layout Generation**: Optimize furniture placement based on various constraints.  
- ✅ **Fixed Element Handling**: Respect doors, windows, and other immovable objects.  
- ✅ **Furniture Customization**: Add various furniture types with appropriate dimensions.  
- ✅ **Interactive UI**: Easy-to-use **Streamlit** web interface.  
- ✅ **Visual Results**: Color-coded visualizations of optimized layouts.  
- ✅ **Optimization Tracking**: Monitor improvement over generations.  

---

## 💻 Technical Approach

The system uses a **hybrid approach** combining Genetic Algorithms and Machine Learning.

### 1. 🎨 Object-Oriented Representation
- **Room class**: Stores dimensions, furniture, and fixed elements.  
- **Furniture class**: Represents items with dimensions, position, and orientation.  

### 2. 🧬 Genetic Algorithm Optimization
- Population of furniture arrangements evolved over generations.  
- **Fitness Function** evaluates layouts based on:  
   - ✅ **Overlap avoidance** (heavily penalized).  
   - ✅ **Wall alignment** (rewarded).  
   - ✅ **Walkability space** (rewarded).  
   - ✅ **Space utilization efficiency**.  

### 3. 🤖 Machine Learning Classification
- **Random Forest Classifier** to evaluate layout validity.  
- Feature extraction from room properties.  
- Trained on synthetic datasets of valid/invalid layouts.

### 4. 🎨 Visualization Utilities
- **OpenCV-based rendering** of room layouts.  
- Color-coded furniture placement.  
- Progress tracking visualization.

---

## 📥 Installation

Follow these steps to set up the project:

```bash
# Clone the repository
git clone https://github.com/yourusername/furniture-layout-optimizer.git
cd furniture-layout-optimizer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

## 📋 Requirements
The project requires the following dependencies:  

✅ **Python 3.8+**  
✅ **Streamlit**  
✅ **NumPy**  
✅ **Pandas**  
✅ **Scikit-learn**  
✅ **OpenCV**  
✅ **Matplotlib**  

You can check the full list in **`requirements.txt`**.

---

## 🚀 Usage
To launch the **Streamlit web application**, run:  

```bash
streamlit run app.py
```

## 🚀 Usage Steps
Follow these steps to easily optimize your room layout using this application:  

### 🏠 Configure Room Dimensions
- Set the **length** and **width** of your room from the sidebar.  

### 🚪 Add Fixed Elements (Doors/Windows)
- Specify the position of **fixed elements** like **doors, windows, and walls**.  
- This will help the algorithm avoid placing furniture in front of doors or windows.  

### 🛋️ Select Furniture Items
- Choose the furniture you want to include in the room such as:  
  - 🛏️ **Bed**  
  - 🪑 **Chair**  
  - 📺 **TV Unit**  
  - 🪟 **Table**, etc.  

### 🎛️ Adjust Optimization Parameters
- Configure the **optimization parameters** such as:  
  - 🔄 **Generations** → Number of times the algorithm will optimize the layout.  
  - 👥 **Population Size** → Number of layout combinations per generation.  

### ✅ Click "Optimize Layout"
- Click the **"Optimize Layout"** button to start the layout optimization process.  
- The algorithm will start arranging your furniture based on the given dimensions and fixed elements.  

### 📊 View Results
- Once the optimization is complete, the best layout will be displayed.  
- The layout will maximize space usage and avoid furniture overlap. 

## 📂 Project Structure
The project structure is organized as follows:  


- **app.py**: This is the main Streamlit web application where users can configure and optimize room layouts.  
- **optimizer.py**: Contains the implementation of the genetic algorithm to optimize furniture layouts.  
- **room.py**: Defines the Room and Furniture classes to handle room dimensions, furniture positions, and fixed elements.  
- **visualization.py**: Provides utilities to generate and render visual layouts of the room.  
- **utils.py**: Contains helper functions for data processing and algorithm execution.  
- **data/**: Contains synthetic datasets to train the machine learning model.  
- **models/**: Holds trained ML models to validate and improve layout optimization.  
- **examples/**: Includes example layout configurations for testing.  
- **tests/**: Unit tests to ensure functionality and accuracy of the optimizer.  

## 📊 Example Results
The optimizer significantly improves layout quality over generations.  
It typically reaches high-quality arrangements within **50-100 generations**.  

### ✅ Key Improvements Achieved:
- ✅ **Avoids furniture overlap.**
- ✅ **Maximizes walkable space.**
- ✅ **Optimizes wall alignment.**
- ✅ **Ensures space utilization efficiency.**

## 📊 Example Results

The optimizer significantly improves layout quality over generations.
It typically reaches high-quality arrangements within 50-100 generations.

✅ Avoids furniture overlap.  
✅ Maximizes walkable space.  
✅ Optimizes wall alignment.  
✅ Ensures space utilization efficiency.  

---

## 📊 Optimization Progress Graph
Below is a sample progress graph showing the improvement of layout quality over generations:  

![Optimization Progress](https://github.com/RahulMahanthi/Furniture-Layout-Optimizer/blob/main/pic5_graph.jpg?raw=true)  

---

## 🏠 Room Layouts
Here are some optimized room layouts generated by the model:

**Initial Room Layout:**  
![Initial Layout](https://github.com/RahulMahanthi/Furniture-Layout-Optimizer/blob/main/pic1.jpg?raw=true)  

**Optimized Room Layout:**  
![Optimized Layout](https://github.com/RahulMahanthi/Furniture-Layout-Optimizer/blob/main/pic4_optimized.jpg?raw=true)  

**Table Comparison:**  
![Table Comparison](https://github.com/RahulMahanthi/Furniture-Layout-Optimizer/blob/main/pic6_yable.jpg?raw=true)  

## 🎉 Conclusion
Our **Furniture Layout Optimizer** uses advanced **Genetic Algorithms (GA)** to optimize room layouts, ensuring:  
- ✅ Maximum space utilization  
- ✅ Avoidance of furniture overlap  
- ✅ Efficient room alignment  

We believe this project has the potential to revolutionize interior design, enabling homeowners, architects, and designers to quickly generate optimized room layouts in minutes.  

**💡 Future Scope:**  
- 📈 Implementing Deep Learning models for layout prediction.  
- 🏠 Supporting multi-room optimization.  
- 🎨 Adding a drag-and-drop UI for custom layouts.  

---

## 💻 Try it Yourself!
👉 Clone this repository, run the application, and start optimizing your room layouts!  
👉 Contributions, suggestions, and feedback are welcome.  

✅ **If you like this project, don't forget to ⭐ star the repository.**  

