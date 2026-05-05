# CI-3: MapReduce — Hottest / Coolest Year

**Aim:** Use the MapReduce paradigm to find the hottest and coolest year in a weather dataset.

**Tech:** Pure Python (`concurrent.futures.ProcessPoolExecutor`) — **no Hadoop required**. The map step runs in parallel across CPU cores.

## Run
```bash
python mapreduce_weather.py
```
The script auto-generates a small `weather_data.csv` on first run.

## How it works
1. **Read** the CSV.
2. **Split** the rows into chunks.
3. **Map (parallel):** each worker groups its chunk's temperatures by year.
4. **Shuffle:** combine partial maps so each year has all its temperatures.
5. **Reduce:** for each year compute max & min temperature.
6. **Final:** pick the year with the highest max and the year with the lowest min.
