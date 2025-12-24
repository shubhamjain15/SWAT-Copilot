"""
Basic usage examples for SWAT-Copilot.

This script demonstrates how to use the SWAT-Copilot library
to load and analyze SWAT model projects.
"""

from pathlib import Path

from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.summary import SummarizeService
from swat_copilot.services.analysis import AnalysisService
from swat_copilot.visualization.plots import SWATPlotter


def main() -> None:
    """Run basic usage examples."""

    # Initialize project manager
    manager = ProjectManager()

    # Example 1: Find SWAT projects
    print("=== Finding SWAT Projects ===")
    search_path = Path(".")  # Current directory
    projects = manager.find_projects(search_path, max_depth=2)
    print(f"Found {len(projects)} SWAT project(s):")
    for project_path in projects:
        print(f"  - {project_path}")

    # Example 2: Load a project
    if projects:
        print("\n=== Loading SWAT Project ===")
        project = manager.load_project(projects[0])
        print(f"Loaded: {project.name}")
        print(f"Path: {project.project_path}")
        print(f"Files: {sum(len(files) for files in project.files.values())}")

        # Example 3: Get project summary
        print("\n=== Project Summary ===")
        summarizer = SummarizeService(project)
        summary = summarizer.get_project_summary()
        print(f"Name: {summary['name']}")
        print(f"Size: {summary['size_mb']} MB")
        print(f"Has outputs: {summary['has_outputs']}")

        # Example 4: Analyze outputs (if available)
        if project.has_outputs():
            print("\n=== Output Analysis ===")
            output_summary = summarizer.get_output_summary()
            print(f"Output files: {len(output_summary['output_files'])}")

            analyzer = AnalysisService(project)

            # Get statistics for a variable
            stats = analyzer.get_variable_statistics("FLOW_OUT", "reach")
            if "error" not in stats:
                print(f"\nFLOW_OUT Statistics:")
                print(f"  Mean: {stats['mean']:.2f}")
                print(f"  Min: {stats['min']:.2f}")
                print(f"  Max: {stats['max']:.2f}")

            # Calculate water balance
            balance = analyzer.calculate_water_balance("subbasin")
            print(f"\nWater Balance:")
            for component, value in balance.items():
                print(f"  {component}: {value}")

            # Example 5: Create visualizations
            print("\n=== Creating Visualizations ===")
            plotter = SWATPlotter(project)

            try:
                # Time series plot
                image_data = plotter.plot_time_series(
                    "FLOW_OUT",
                    output_type="reach",
                    title="Streamflow Time Series",
                )
                print("Created time series plot")

                # Comparison plot
                image_data = plotter.plot_comparison(
                    ["FLOW_OUT", "SED_OUT"],
                    output_type="reach",
                )
                print("Created comparison plot")

            except Exception as e:
                print(f"Visualization error: {e}")

    else:
        print("\nNo SWAT projects found.")
        print("Place a SWAT project directory in the current path or specify a path.")


if __name__ == "__main__":
    main()
