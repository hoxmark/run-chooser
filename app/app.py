from flask import Flask, render_template
from utils.gpx_utils import (
    calculate_distances_and_elevation,
    calculate_pace,
    create_heatmap,
    import_gpx_files,
    seasonal_analysis,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/heatmap")
def heatmap():
    directory = "workouts/"
    routes = import_gpx_files(directory)
    m = create_heatmap(routes)
    map_html = m._repr_html_()
    return render_template("heatmap.html", map_html=map_html)


@app.route("/metadata")
def metadata():
    directory = "workouts/"
    routes = import_gpx_files(directory)
    distances, elevations = calculate_distances_and_elevation(routes)
    total_distance = sum(distances)
    avg_pace = (
        sum(calculate_pace(route) for route in routes) / len(routes) if routes else 0
    )
    total_elevation_gain = sum(elevations)
    season_data = seasonal_analysis(routes, distances)
    return render_template(
        "metadata.html",
        total_distance=total_distance,
        avg_pace=avg_pace,
        total_elevation_gain=total_elevation_gain,
        season_data=season_data,
    )


@app.route("/workout_overview")
def workout_overview():
    directory = "workouts/"
    routes = import_gpx_files(directory)
    distances, elevations = calculate_distances_and_elevation(routes)
    workout_list = [
        {
            "id": idx,
            "date": route[0][3],
            "distance": round(distance / 1000, 2),  # Convert to km
            "elevation_gain": round(elevation, 2),
            "pace": round(calculate_pace(route), 2),
        }
        for idx, (route, distance, elevation) in enumerate(
            zip(routes, distances, elevations)
        )
    ]
    return render_template("workout_overview.html", workout_list=workout_list)


@app.route("/workout/<int:workout_id>")
def single_workout(workout_id):
    directory = "workouts/"
    routes = import_gpx_files(directory)
    route = routes[workout_id]
    distance, elevation_gain = calculate_distances_and_elevation([route])
    pace = calculate_pace(route)
    return render_template(
        "single_workout.html",
        route=route,
        distance=distance[0],
        elevation_gain=elevation_gain[0],
        pace=pace,
    )


@app.route("/all_runs")
def all_runs():
    directory = "workouts/"
    routes = import_gpx_files(directory)
    distances, elevations = calculate_distances_and_elevation(routes)
    all_run_data = [
        {
            "id": idx,
            "date": route[0][3],
            "distance": round(distance / 1000, 2),  # Convert to km
            "elevation_gain": round(elevation, 2),
            "pace": round(calculate_pace(route), 2),
            "route": route,
        }
        for idx, (route, distance, elevation) in enumerate(
            zip(routes, distances, elevations)
        )
    ]
    return render_template("all_runs.html", all_run_data=all_run_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
