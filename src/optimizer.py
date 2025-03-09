import numpy as np
import random
import copy
import matplotlib.pyplot as plt
from src.room import Room, Furniture

class GeneticLayoutOptimizer:
    def __init__(self, room_length, room_width, furniture_list, fixed_elements=None, 
                 population_size=50, generations=100, mutation_rate=0.2, elitism_count=5):
        self.room_length = room_length
        self.room_width = room_width
        self.furniture_list = furniture_list
        self.fixed_elements = fixed_elements if fixed_elements else []
        
        # GA parameters
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count
        
        # Progress tracking
        self.best_fitness_history = []
        
    def initialize_population(self):
        """Create initial random population of furniture layouts"""
        population = []
        
        for _ in range(self.population_size):
            # Create a new individual (furniture arrangement)
            individual = []
            
            for furniture in self.furniture_list:
                # Clone furniture item
                furn_copy = copy.deepcopy(furniture)
                
                # Random orientation (0 or 90 degrees)
                if random.random() > 0.5:
                    furn_copy.rotate()
                
                # Random position within room bounds
                x = random.uniform(0, self.room_length - furn_copy.length)
                y = random.uniform(0, self.room_width - furn_copy.width)
                furn_copy.set_position(x, y)
                
                individual.append(furn_copy)
                
            population.append(individual)
            
        return population
    
    def calculate_fitness(self, individual):
        """Calculate fitness score for an individual layout"""
        # Higher score is better
        score = 100
        
        # Check for overlaps with fixed elements
        for furniture in individual:
            for element in self.fixed_elements:
                if (furniture.x < element['x'] + element['width'] and 
                    furniture.x + furniture.length > element['x'] and
                    furniture.y < element['y'] + element['length'] and
                    furniture.y + furniture.width > element['y']):
                    score -= 20  # Heavy penalty for overlapping fixed elements
        
        # Check for furniture-furniture overlaps
        for i in range(len(individual)):
            for j in range(i+1, len(individual)):
                furn1 = individual[i]
                furn2 = individual[j]
                
                if (furn1.x < furn2.x + furn2.length and 
                    furn1.x + furn1.length > furn2.x and
                    furn1.y < furn2.y + furn2.width and
                    furn1.y + furn1.width > furn2.y):
                    score -= 15  # Penalty for furniture overlap
        
        # Reward furniture against walls
        for furniture in individual:
            # Check if any edge is close to a wall
            dist_left = furniture.x
            dist_right = self.room_length - (furniture.x + furniture.length)
            dist_top = furniture.y
            dist_bottom = self.room_width - (furniture.y + furniture.width)
            
            min_wall_dist = min(dist_left, dist_right, dist_top, dist_bottom)
            
            if min_wall_dist < 0.1:  # Close to wall (10cm)
                score += 5
        
        # Reward clear walkways (simplified)
        # We'll use a grid-based approach
        grid_size = 20
        grid = np.zeros((int(self.room_width * grid_size), int(self.room_length * grid_size)))
        
        # Add fixed elements to grid
        for element in self.fixed_elements:
            x1 = int(element['x'] * grid_size)
            y1 = int(element['y'] * grid_size)
            x2 = int((element['x'] + element['width']) * grid_size)
            y2 = int((element['y'] + element['length']) * grid_size)
            grid[y1:y2, x1:x2] = 1
        
        # Add furniture to grid
        for furn in individual:
            x1 = int(furn.x * grid_size)
            y1 = int(furn.y * grid_size)
            x2 = int((furn.x + furn.length) * grid_size)
            y2 = int((furn.y + furn.width) * grid_size)
            grid[y1:y2, x1:x2] = 1
            
        # Calculate walkability
        empty_cells = np.sum(grid == 0)
        total_cells = grid.size
        walkability = empty_cells / total_cells
        
        score += walkability * 30  # Reward for good walkability
        
        # If score is negative, set to 0
        score = max(0, score)
        
        return score
    
    def select_parents(self, population, fitness_scores):
        """Select parents for crossover using tournament selection"""
        tournament_size = 3
        parents = []
        
        for _ in range(2):
            # Select random subset of individuals
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            
            # Select winner (highest fitness)
            winner_idx = tournament_indices[np.argmax(tournament_fitness)]
            parents.append(population[winner_idx])
            
        return parents
    
    def crossover(self, parent1, parent2):
        """Create a child layout by combining elements from both parents"""
        child = []
        
        for i in range(len(parent1)):
            # 50% chance to inherit from each parent
            if random.random() < 0.5:
                child.append(copy.deepcopy(parent1[i]))
            else:
                child.append(copy.deepcopy(parent2[i]))
                
        return child
    
    def mutate(self, individual):
        """Apply random mutations to an individual"""
        for furniture in individual:
            # Mutate position
            if random.random() < self.mutation_rate:
                x = random.uniform(0, self.room_length - furniture.length)
                y = random.uniform(0, self.room_width - furniture.width)
                furniture.set_position(x, y)
                
            # Mutate orientation
            if random.random() < self.mutation_rate:
                furniture.rotate()
                
        return individual
    
    def optimize(self, verbose=True):
        """Run the genetic algorithm optimization"""
        # Initialize population
        population = self.initialize_population()
        
        self.best_fitness_history = []
        best_individual = None
        best_fitness = 0
        
        for generation in range(self.generations):
            # Calculate fitness for each individual
            fitness_scores = [self.calculate_fitness(ind) for ind in population]
            
            # Track best individual
            max_fitness_idx = np.argmax(fitness_scores)
            if fitness_scores[max_fitness_idx] > best_fitness:
                best_fitness = fitness_scores[max_fitness_idx]
                best_individual = copy.deepcopy(population[max_fitness_idx])
                
            self.best_fitness_history.append(best_fitness)
            
            if verbose and generation % 10 == 0:
                print(f"Generation {generation}, Best Fitness: {best_fitness:.2f}")
            
            # Create new population
            new_population = []
            
            # Elitism - keep best individuals
            sorted_indices = np.argsort(fitness_scores)[::-1]
            for i in range(self.elitism_count):
                new_population.append(copy.deepcopy(population[sorted_indices[i]]))
            
            # Create the rest through crossover and mutation
            while len(new_population) < self.population_size:
                # Select parents
                parents = self.select_parents(population, fitness_scores)
                
                # Crossover
                child = self.crossover(parents[0], parents[1])
                
                # Mutation
                child = self.mutate(child)
                
                new_population.append(child)
                
            population = new_population
            
        if verbose:
            print(f"Optimization complete. Best fitness: {best_fitness:.2f}")
        
        return best_individual, best_fitness
    
    def plot_fitness_history(self):
        """Plot the fitness history of the optimization process"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.best_fitness_history)
        plt.title('Best Fitness Score Over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Fitness Score')
        plt.grid(True)
        
        return plt.gcf()  # Return the current figure

def create_room_with_furniture(room_length, room_width, furniture_list, fixed_elements=None, name="Optimized Room"):
    """Helper function to create a room with furniture"""
    room = Room(length=room_length, width=room_width, name=name)
    
    # Add fixed elements
    if fixed_elements:
        for element in fixed_elements:
            room.add_fixed_element(element)
    
    # Add furniture
    for furniture in furniture_list:
        room.add_furniture(furniture)
        
    return room

def optimize_room_layout(room_length, room_width, furniture_config, fixed_elements=None, 
                        generations=100, population_size=50):
    """Main function to optimize room layout based on input configurations"""
    # Convert furniture config to actual Furniture objects
    furniture_list = []
    for item in furniture_config:
        furniture = Furniture(
            name=item['name'],
            width=item['width'],
            length=item['length'],
            movable=item.get('movable', True)
        )
        furniture_list.append(furniture)
    
    # Create and run optimizer
    optimizer = GeneticLayoutOptimizer(
        room_length=room_length,
        room_width=room_width,
        furniture_list=furniture_list,
        fixed_elements=fixed_elements,
        generations=generations,
        population_size=population_size
    )
    
    # Run the optimization
    best_layout, fitness = optimizer.optimize()
    
    # Create and return the optimized room
    optimized_room = create_room_with_furniture(
        room_length=room_length,
        room_width=room_width,
        furniture_list=best_layout,
        fixed_elements=fixed_elements
    )
    
    return optimized_room, best_layout, fitness, optimizer.best_fitness_history