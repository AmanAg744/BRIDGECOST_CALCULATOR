**Bridge Cost Comparison Tool**

A desktop application to compare the life cycle costs of steel and concrete bridges using an SQLite database.

**Features:**

*   Input bridge parameters (span length, width, traffic volume, design life).
    
*   Compute and compare life cycle costs for steel and concrete bridges.
    
*   Interactive bar plot visualization.
    
*   Export cost comparison plots as PNG files.
    
*   SQLite database for cost data storage.
    

**Installation:**

1.  Clone the repository:
    
    *   git clone https://github.com/yourusername/bridge-cost-comparison.git
        
    *   cd bridge-cost-comparison
        
2.  Install dependencies:
    
    *   pip install -r requirements.txt
        

**Usage:**

1.  Run the application using python main.py.
    
2.  Enter the bridge parameters.
    
3.  Click "Calculate Costs" to compare costs.
    
4.  View results in the output table and bar plot.
    
5.  Export plots using the "Export Plot" button.
    

**Project Structure:**

*   main.py - Application entry point
    
*   gui.py - GUI implementation
    
*   database.py - Database management
    
*   calculations.py - Cost calculation logic
    
*   plot.py - Plotting functionality
    
*   requirements.txt - Dependencies
    
*   README.txt - Project information
    

**License:**This project is licensed under the MIT License.
