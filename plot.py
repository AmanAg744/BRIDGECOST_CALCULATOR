from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Plotter:
    def __init__(self):
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
    
    def get_canvas(self):
        return self.canvas
    
    def plot_comparison(self, steel_costs, concrete_costs, labels):
        self.ax.clear()
        
        # Create bars
        bar_width = 0.35
        x = range(len(labels))
        
        # Plot bars
        self.ax.bar(x, steel_costs, width=bar_width, label="Steel", color="blue")
        self.ax.bar([p + bar_width for p in x], concrete_costs, width=bar_width, 
                   label="Concrete", color="orange")
        
        # Customize plot
        self.ax.set_xticks([p + bar_width/2 for p in x])
        self.ax.set_xticklabels(labels, rotation=45, ha="right")
        self.ax.set_title("Cost Comparison: Steel vs. Concrete")
        self.ax.set_ylabel("Cost (₹)")
        self.ax.legend()
        
        # Adjust layout to prevent label cutoff
        self.figure.tight_layout()
        self.canvas.draw()
    
    def save_plot(self, filename):
        self.figure.savefig(filename, bbox_inches='tight', dpi=300)