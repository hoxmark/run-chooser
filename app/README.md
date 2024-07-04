# Running Routes Analysis Web App

## Overview

The Running Routes Analysis Web App is a comprehensive tool for runners to track, analyze, and visualize their workouts. This web application provides various features, including interactive heatmaps, detailed workout statistics, a calendar view, and individual route visualizations. Built with Flask, Folium, and Leaflet.js, this app offers a modern and user-friendly interface to help you improve your running performance.

## Features

### Welcome Page
- **Attractive Design**: A welcoming and visually appealing landing page with clear navigation to all main features.
- **Easy Navigation**: Buttons to quickly access heatmaps, metadata, workout overview, and calendar.

### Heatmap
- **Interactive Heatmap**: Visualize all your running routes on an interactive heatmap.
- **Customizable**: Based on your GPX data, it shows the density of your runs.

### Metadata
- **Detailed Statistics**: View comprehensive statistics for all your workouts, including total distance, average pace, and total elevation gain.
- **Seasonal Analysis**: Break down your workout data by season to see how your performance varies throughout the year.

### Workout Overview
- **Workout List**: A detailed list of all your workouts with essential metrics like distance, elevation gain, and date.
- **Quick Access**: Links to view each workout in detail.

### Workout Calendar
- **Calendar View**: Visualize your workout history in a calendar format to easily track your running activities over time.

### Single Workout View
- **Route Visualization**: See the detailed route of each individual workout on an interactive map.
- **Run Stats**: View specific statistics for each workout, including distance, elevation gain, and average pace.

### All Runs Mapped
- **Route Mapping**: Visualize every single run on a map to see your running paths over time.
- **Interactive Map**: Use Leaflet.js to explore each route in detail.

## Getting Started

### Prerequisites
- Python 3.7+
- Flask
- Folium
- GPXpy

### Installation
1. **Clone the repository**:
    \`\`\`sh
    git clone https://github.com/yourusername/running-routes-analysis.git
    cd running-routes-analysis
    \`\`\`

2. **Create a virtual environment and activate it**:
    \`\`\`sh
    python -m venv venv
    source venv/bin/activate  # On Windows use \`venv\Scripts\activate\`
    \`\`\`

3. **Install dependencies**:
    \`\`\`sh
    pip install -r requirements.txt
    \`\`\`

4. **Run the application**:
    \`\`\`sh
    python app.py
    \`\`\`

5. **Access the application**:
    Open your web browser and navigate to \`http://127.0.0.1:5001\`.

## Project Structure
```
/your_project
|-- app.py
|-- templates
|   |-- base.html
|   |-- home.html
|   |-- heatmap.html
|   |-- metadata.html
|   |-- workout_overview.html
|   |-- workout_calendar.html
|   |-- single_workout.html
|   |-- all_runs.html
|-- static
|   |-- style.css
|   |-- leaflet.css
|   |-- leaflet.js
|   |-- images
|       |-- heatmap.png
|       |-- metadata.png
|       |-- overview.png
|       |-- calendar.png
|-- utils
|   |-- __init__.py
|   |-- gpx_utils.py
```

## Usage
- **Upload GPX files**: Place your GPX files in the \`workouts\` directory.
- **View Heatmap**: Navigate to the heatmap page to see a visual representation of your running routes.
- **Analyze Metadata**: Go to the metadata page to see detailed statistics of your runs.
- **Workout Overview**: Check out the workout overview page for a list of all your workouts.
- **Workout Calendar**: Use the calendar view to track your workout history.
- **Individual Workout**: Click on any workout in the overview to see its detailed route and stats.
- **All Runs Mapped**: View all your running routes on a single map.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or suggestions, feel free to reach out to [your email address].
