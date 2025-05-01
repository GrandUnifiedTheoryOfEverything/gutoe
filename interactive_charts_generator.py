#!/usr/bin/env python3
"""
Interactive Charts Generator

This module provides functions for generating interactive charts and diagrams
for PDF documents using JavaScript and PDF annotations.
"""

import os
import json
import tempfile
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib.units import inch
from reportlab.platypus import Flowable
from reportlab.pdfgen.canvas import Canvas

class InteractiveChart(Flowable):
    """
    Interactive Chart Flowable

    This class creates a flowable object that can be added to a PDF document
    and contains JavaScript for interactive behavior.
    """

    def __init__(self, width, height, chart_data, chart_type="line"):
        """
        Initialize the interactive chart

        Parameters:
        -----------
        width : float
            Width of the chart in points
        height : float
            Height of the chart in points
        chart_data : dict
            Data for the chart
        chart_type : str
            Type of chart (line, bar, pie)
        """
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.chart_data = chart_data
        self.chart_type = chart_type

        # Generate a unique ID for this chart
        self.chart_id = f"chart_{id(self)}"

    def draw(self):
        """Draw the chart on the canvas"""
        # Create a static preview of the chart
        self._draw_static_preview()

        # Add JavaScript for interactivity
        self._add_javascript()

    def _draw_static_preview(self):
        """Draw a static preview of the chart"""
        # Draw a border
        self.canv.rect(0, 0, self.width, self.height)

        # Draw chart title
        title = self.chart_data.get("title", "Interactive Chart")
        self.canv.setFont("Helvetica-Bold", 12)
        self.canv.drawCentredString(self.width/2, self.height - 20, title)

        # Draw a placeholder message
        self.canv.setFont("Helvetica", 10)
        self.canv.drawCentredString(self.width/2, self.height/2,
                                   "Interactive chart - click to activate")

        # Add an annotation for interactivity
        # Note: JavaScript links are not fully supported in ReportLab
        # self.canv.linkRect("",
        #                   f"javascript:activateChart('{self.chart_id}');",
        #                   (0, 0, self.width, self.height),
        #                   thickness=0)
        pass

    def _add_javascript(self):
        """Add JavaScript for chart interactivity"""
        # Convert chart data to JSON
        chart_json = json.dumps(self.chart_data)

        # Create JavaScript to initialize the chart
        js = f"""
        var {self.chart_id}_data = {chart_json};

        function activateChart(chartId) {{
            if (chartId === '{self.chart_id}') {{
                // This would be replaced with actual chart rendering code
                // in a real implementation using a JavaScript charting library
                app.alert('Chart activated: {self.chart_type.capitalize()} Chart\\n' +
                         'Title: {self.chart_data.get("title", "Interactive Chart")}\\n' +
                         'This is a placeholder for interactive functionality.');
            }}
        }}
        """

        # Add the JavaScript to the document
        # Note: JavaScript support is limited in ReportLab
        # self.canv.addJavaScript(js)
        pass

class InteractiveChartsGenerator:
    """
    Interactive Charts Generator

    This class provides methods for generating interactive charts and diagrams
    for PDF documents.
    """

    def __init__(self, output_dir="gfx/pdf/interactive"):
        """
        Initialize the interactive charts generator

        Parameters:
        -----------
        output_dir : str
            Directory to save chart images (will be created if it doesn't exist)
        """
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    def create_interactive_line_chart(self, data, title="Interactive Line Chart",
                                     x_label="X Axis", y_label="Y Axis",
                                     width=6*inch, height=4*inch):
        """
        Create an interactive line chart

        Parameters:
        -----------
        data : list
            List of data series, each containing a name and data points
        title : str
            Title of the chart
        x_label : str
            Label for the x-axis
        y_label : str
            Label for the y-axis
        width : float
            Width of the chart
        height : float
            Height of the chart

        Returns:
        --------
        InteractiveChart
            Interactive chart flowable
        """
        # Create chart data
        chart_data = {
            "type": "line",
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "series": data
        }

        # Create a static image for the chart
        self._create_static_image(chart_data, "line")

        # Create and return the interactive chart
        return InteractiveChart(width, height, chart_data, "line")

    def create_interactive_bar_chart(self, data, title="Interactive Bar Chart",
                                    x_label="Categories", y_label="Values",
                                    width=6*inch, height=4*inch):
        """
        Create an interactive bar chart

        Parameters:
        -----------
        data : list
            List of data points, each containing a category and value
        title : str
            Title of the chart
        x_label : str
            Label for the x-axis
        y_label : str
            Label for the y-axis
        width : float
            Width of the chart
        height : float
            Height of the chart

        Returns:
        --------
        InteractiveChart
            Interactive chart flowable
        """
        # Create chart data
        chart_data = {
            "type": "bar",
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "data": data
        }

        # Create a static image for the chart
        self._create_static_image(chart_data, "bar")

        # Create and return the interactive chart
        return InteractiveChart(width, height, chart_data, "bar")

    def create_interactive_pie_chart(self, data, title="Interactive Pie Chart",
                                    width=5*inch, height=5*inch):
        """
        Create an interactive pie chart

        Parameters:
        -----------
        data : list
            List of data points, each containing a category and value
        title : str
            Title of the chart
        width : float
            Width of the chart
        height : float
            Height of the chart

        Returns:
        --------
        InteractiveChart
            Interactive chart flowable
        """
        # Create chart data
        chart_data = {
            "type": "pie",
            "title": title,
            "data": data
        }

        # Create a static image for the chart
        self._create_static_image(chart_data, "pie")

        # Create and return the interactive chart
        return InteractiveChart(width, height, chart_data, "pie")

    def _create_static_image(self, chart_data, chart_type):
        """
        Create a static image for the chart

        Parameters:
        -----------
        chart_data : dict
            Data for the chart
        chart_type : str
            Type of chart (line, bar, pie)

        Returns:
        --------
        str
            Path to the saved image
        """
        # Create a unique filename
        filename = f"{chart_data['title'].lower().replace(' ', '_')}_{id(chart_data)}.png"
        output_file = os.path.join(self.output_dir, filename)

        # Create figure
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        if chart_type == "line":
            # Plot each data series
            for series in chart_data["series"]:
                x_values = [point[0] for point in series["data"]]
                y_values = [point[1] for point in series["data"]]
                ax.plot(x_values, y_values, label=series["name"])

            # Add labels and title
            ax.set_xlabel(chart_data["x_label"])
            ax.set_ylabel(chart_data["y_label"])
            ax.set_title(chart_data["title"])
            ax.legend()

        elif chart_type == "bar":
            # Extract categories and values
            categories = [item["category"] for item in chart_data["data"]]
            values = [item["value"] for item in chart_data["data"]]

            # Create bar chart
            ax.bar(categories, values)

            # Add labels and title
            ax.set_xlabel(chart_data["x_label"])
            ax.set_ylabel(chart_data["y_label"])
            ax.set_title(chart_data["title"])

        elif chart_type == "pie":
            # Extract categories and values
            categories = [item["category"] for item in chart_data["data"]]
            values = [item["value"] for item in chart_data["data"]]

            # Define professional color scheme
            colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(categories)))

            # Create pie chart with enhanced styling
            wedges, texts, autotexts = ax.pie(
                values,
                labels=None,  # We'll add custom labels
                autopct='%1.1f%%',
                startangle=90,
                shadow=True,
                colors=colors,
                wedgeprops={'edgecolor': 'w', 'linewidth': 1, 'antialiased': True},
                textprops={'fontsize': 12, 'weight': 'bold'}
            )

            # Customize autopct text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_weight('bold')

            # Add a legend with categories
            ax.legend(
                wedges,
                categories,
                title=chart_data.get("legend_title", "Categories"),
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1),
                fontsize=10
            )

            # Add title with custom styling
            ax.set_title(
                chart_data["title"],
                fontsize=14,
                fontweight="bold",
                pad=20
            )

            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')

            # Add a subtle grid in the background
            ax.grid(True, linestyle='--', alpha=0.3)

            # Add a thin border around the chart
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color('gray')
                spine.set_linewidth(0.5)

        # Save the figure
        plt.savefig(output_file)
        plt.close()

        return output_file

# Main function for command-line usage
def main():
    """Main function for command-line usage"""
    generator = InteractiveChartsGenerator()

    # Create sample line chart data
    line_data = [
        {
            "name": "Series 1",
            "data": [(0, 1), (1, 2), (2, 4), (3, 8), (4, 16)]
        },
        {
            "name": "Series 2",
            "data": [(0, 1), (1, 3), (2, 9), (3, 27), (4, 81)]
        }
    ]

    # Create sample bar chart data
    bar_data = [
        {"category": "A", "value": 10},
        {"category": "B", "value": 20},
        {"category": "C", "value": 15},
        {"category": "D", "value": 25}
    ]

    # Create sample pie chart data
    pie_data = [
        {"category": "Category 1", "value": 35},
        {"category": "Category 2", "value": 25},
        {"category": "Category 3", "value": 20},
        {"category": "Category 4", "value": 15},
        {"category": "Category 5", "value": 5}
    ]

    # Create interactive charts
    generator.create_interactive_line_chart(line_data)
    generator.create_interactive_bar_chart(bar_data)
    generator.create_interactive_pie_chart(pie_data)

    print("Interactive charts generated successfully!")

if __name__ == "__main__":
    main()
