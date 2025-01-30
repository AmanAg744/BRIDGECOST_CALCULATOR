from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QFileDialog, 
    QDockWidget, QDialog, QFormLayout, QMessageBox,QInputDialog,QHeaderView, QSizePolicy

)
from PyQt5.QtCore import Qt
from plot import Plotter
from database import DatabaseManager
from calculations import CostCalculator

class UpdateDatabaseDialog(QDialog):
    def __init__(self, db_manager, material, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.material = material
        self.setWindowTitle(f"Update {material} Costs")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # Fetch current data for the material
        self.current_data = self.db_manager.fetch_material_data(self.material)
        if not self.current_data:
            QMessageBox.warning(self, "Error", f"No data found for {self.material}.")
            self.close()
            return

        # Create input fields with current data
        self.base_rate_input = QLineEdit(str(self.current_data[1]))
        self.maintenance_rate_input = QLineEdit(str(self.current_data[2]))
        self.repair_rate_input = QLineEdit(str(self.current_data[3]))
        self.demolition_rate_input = QLineEdit(str(self.current_data[4]))
        self.env_factor_input = QLineEdit(str(self.current_data[5]))
        self.social_factor_input = QLineEdit(str(self.current_data[6]))
        self.delay_factor_input = QLineEdit(str(self.current_data[7]))

        # Add fields to the form
        layout.addRow("Base Rate (₹/m²):", self.base_rate_input)
        layout.addRow("Maintenance Rate (₹/m²/year):", self.maintenance_rate_input)
        layout.addRow("Repair Rate (₹/m²):", self.repair_rate_input)
        layout.addRow("Demolition Rate (₹/m²):", self.demolition_rate_input)
        layout.addRow("Environmental Factor (₹/m²):", self.env_factor_input)
        layout.addRow("Social Factor (₹/vehicle/year):", self.social_factor_input)
        layout.addRow("Delay Factor (₹/vehicle/year):", self.delay_factor_input)

        # Add update button
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_data)
        layout.addRow(self.update_button)

    def update_data(self):
        try:
            # Get updated values
            base_rate = float(self.base_rate_input.text())
            maintenance_rate = float(self.maintenance_rate_input.text())
            repair_rate = float(self.repair_rate_input.text())
            demolition_rate = float(self.demolition_rate_input.text())
            env_factor = float(self.env_factor_input.text())
            social_factor = float(self.social_factor_input.text())
            delay_factor = float(self.delay_factor_input.text())

            # Update database
            self.db_manager.update_cost_data(
                self.material,
                BaseRate=base_rate,
                MaintenanceRate=maintenance_rate,
                RepairRate=repair_rate,
                DemolitionRate=demolition_rate,
                EnvironmentalFactor=env_factor,
                SocialFactor=social_factor,
                DelayFactor=delay_factor
            )

            QMessageBox.information(self, "Success", "Database updated successfully!")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers.")

class BridgeCostApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel vs. Concrete Bridge Cost Comparison")
        self.setGeometry(100, 100, 1200, 600)
        
        # Initialize components
        self.db_manager = DatabaseManager("bridge_costs.db")
        self.calculator = CostCalculator(self.db_manager)
        self.plotter = Plotter()
        
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left Dock (Input Dock)
        self.left_dock = QDockWidget("Input Parameters", self)
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.create_input_fields()
        self.left_dock.setWidget(self.left_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)

        # Center Panel (Bar Plot)
        self.plot_canvas = self.plotter.get_canvas()
        main_layout.addWidget(self.plot_canvas)

        # Right Dock (Output Dock)
        self.right_dock = QDockWidget("Output Table", self)
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)

        # **Define `self.output_layout` before using it**
        self.output_layout = QVBoxLayout()  # <-- Fix here
        self.right_layout.addLayout(self.output_layout)  # <-- Attach to right layout

        self.create_output_table()

        self.right_widget.setLayout(self.right_layout)
        self.right_dock.setWidget(self.right_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)

        # Set central widget
        self.setCentralWidget(main_widget)

    def create_input_fields(self):
        input_grid = QGridLayout()
        
        # Create input fields
        self.span_length_input = QLineEdit()
        self.width_input = QLineEdit()
        self.traffic_volume = QLineEdit()
        self.design_life = QLineEdit()
        
        # Add labels and inputs to grid
        input_grid.addWidget(QLabel('Span Length (m):'), 0, 0)
        input_grid.addWidget(self.span_length_input, 0, 1)
        
        input_grid.addWidget(QLabel('Width (m):'), 1, 0)
        input_grid.addWidget(self.width_input, 1, 1)
        
        input_grid.addWidget(QLabel('Traffic Volume (vehicles/day):'), 2, 0)
        input_grid.addWidget(self.traffic_volume, 2, 1)
        
        input_grid.addWidget(QLabel('Design Life (years):'), 3, 0)
        input_grid.addWidget(self.design_life, 3, 1)
        
        # Add calculate button
        self.calculate_button = QPushButton('Calculate Costs')
        self.calculate_button.clicked.connect(self.calculate_costs)
        input_grid.addWidget(self.calculate_button, 4, 0, 1, 2)
        
        # Add update database button
        self.update_db_button = QPushButton('Update Database')
        self.update_db_button.clicked.connect(self.show_update_database_dialog)
        input_grid.addWidget(self.update_db_button, 5, 0, 1, 2)
        
        # Add result label for errors
        self.result_label = QLabel('')
        input_grid.addWidget(self.result_label, 6, 0, 1, 2)
        
        self.left_layout.addLayout(input_grid)
        self.left_layout.addStretch()

    def show_update_database_dialog(self):
        # Show a dialog to select material to update
        material, ok = QInputDialog.getItem(
            self, "Select Material", "Choose material to update:", ["Steel", "Concrete"], 0, False
        )
        if ok and material:
            dialog = UpdateDatabaseDialog(self.db_manager, material, self)
            dialog.exec_()

    def create_output_table(self):
        self.output_layout.addWidget(QLabel("Cost Comparison Table", alignment=Qt.AlignCenter))

        # Create and configure table
        self.output_table = QTableWidget()
        self.output_table.setColumnCount(3)
        self.output_table.setHorizontalHeaderLabels([
            "Cost Component",
            "Steel Bridge (₹)",
            "Concrete Bridge (₹)"
        ])
        
        # **Improve Display Spacing**
        self.output_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.output_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.output_table.verticalHeader().setDefaultSectionSize(40)  # Increase row height

        # Add export button
        self.export_button = QPushButton("Export Plot")
        self.export_button.clicked.connect(self.export_plot)

        self.output_layout.addWidget(self.output_table)
        self.output_layout.addWidget(self.export_button)

    def calculate_costs(self):
        try:
            # Get input values
            span_length = float(self.span_length_input.text())
            width = float(self.width_input.text())
            traffic_volume = float(self.traffic_volume.text())
            design_life = int(self.design_life.text())
            
            # Validate inputs
            if any(val <= 0 for val in [span_length, width, traffic_volume, design_life]):
                raise ValueError("All inputs must be positive numbers")
            
            # Calculate costs
            results = self.calculator.calculate_costs(
                span_length, width, traffic_volume, design_life
            )
            
            # Update display
            self.populate_output_table(results)
            self.update_plot(results)
            self.result_label.setText("")  # Clear any error messages
            
        except ValueError as e:
            self.result_label.setText(f"Error: {str(e)}")

    def populate_output_table(self, results):
        components = self.calculator.get_cost_components()
        self.output_table.setRowCount(len(components))
        
        for i, component in enumerate(components):
            self.output_table.setItem(i, 0, QTableWidgetItem(component))
            self.output_table.setItem(i, 1, QTableWidgetItem(f"{results[0][i + 1]:,.2f}"))
            self.output_table.setItem(i, 2, QTableWidgetItem(f"{results[1][i + 1]:,.2f}"))
        
        self.output_table.resizeColumnsToContents()

    def update_plot(self, results):
        labels = self.calculator.get_cost_components()[:-1]  # Exclude Total Cost
        steel_costs = [results[0][i + 1] for i in range(len(labels))]
        concrete_costs = [results[1][i + 1] for i in range(len(labels))]
        self.plotter.plot_comparison(steel_costs, concrete_costs, labels)

    def export_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export Plot", "", "PNG Files (*.png)"
        )
        if file_name:
            self.plotter.save_plot(file_name)

    def update_database(self):
        # Add functionality to update database (optional)
        pass

    def closeEvent(self, event):
        self.db_manager.close()
        super().closeEvent(event)
    