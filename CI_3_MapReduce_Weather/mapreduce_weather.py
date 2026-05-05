# CI-3: MapReduce-style processing of weather data to find the hottest
# and coolest year. Implemented WITHOUT Hadoop -- we use Python's
# concurrent.futures.ProcessPoolExecutor to run the map step in parallel
# across CPU cores. Demonstrates the MapReduce paradigm in pure Python.

import csv
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor


# ---------------- read the dataset ----------------

def read_weather_data(file_path):
    """Read weather CSV into a list of {year, temperature} dicts."""
    with open(file_path, "r") as f:
        return list(csv.DictReader(f))


# ---------------- map phase ----------------

def map_function(chunk):
    """
    Map step: for each row in the chunk, group temperatures by year.
    Returns {year -> list of temperatures}.
    """
    grouped = defaultdict(list)
    for row in chunk:
        year = int(row["year"])
        temp = float(row["temperature"])
        grouped[year].append(temp)
    return grouped


# ---------------- reduce phase ----------------

def reduce_function(grouped):
    """
    Reduce step: for each year compute its max and min temperature.
    Returns {year -> {'max': ..., 'min': ...}}.
    """
    extremes = {}
    for year, temps in grouped.items():
        extremes[year] = {"max": max(temps), "min": min(temps)}
    return extremes


# ---------------- driver ----------------

def split_data(data, chunk_size):
    """Split the data into chunks of fixed size for parallel mappers."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def map_reduce(file_path, chunk_size=50):
    data = read_weather_data(file_path)
    chunks = list(split_data(data, chunk_size))

    # MAP IN PARALLEL across CPU cores. Each worker processes one chunk.
    with ProcessPoolExecutor() as executor:
        partials = list(executor.map(map_function, chunks))

    # SHUFFLE: combine partial maps so each year has all its temperatures.
    combined = defaultdict(list)
    for partial in partials:
        for year, temps in partial.items():
            combined[year].extend(temps)

    # REDUCE: per-year max/min.
    extremes = reduce_function(combined)

    # Final pass: pick the year with the highest max and the year with the lowest min.
    hottest = max(extremes, key=lambda y: extremes[y]["max"])
    coolest = min(extremes, key=lambda y: extremes[y]["min"])
    return hottest, extremes[hottest], coolest, extremes[coolest], extremes


# ---------------- create demo dataset on first run ----------------

def make_demo_csv(path):
    """Write a tiny example weather_data.csv if it doesn't exist."""
    if os.path.exists(path):
        return
    rows = [
        ("year", "temperature"),
        ("2000", "10.5"), ("2000", "12.0"), ("2000", "9.8"),
        ("2001", "5.2"),  ("2001", "8.1"),  ("2001", "6.5"),
        ("2002", "15.3"), ("2002", "14.1"),
        ("2003", "7.0"),  ("2003", "10.0"), ("2003", "11.5"),
    ]
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"Created demo dataset {path}")


if __name__ == "__main__":
    csv_path = "weather_data.csv"
    make_demo_csv(csv_path)

    hot_year, hot_data, cool_year, cool_data, all_extremes = map_reduce(csv_path, chunk_size=50)

    print("\nPer-year extremes:")
    for year in sorted(all_extremes):
        e = all_extremes[year]
        print(f"  {year}: max={e['max']:>5}°C, min={e['min']:>5}°C")

    print(f"\nHottest year: {hot_year} with maximum temperature {hot_data['max']}°C")
    print(f"Coolest year: {cool_year} with minimum temperature {cool_data['min']}°C")
