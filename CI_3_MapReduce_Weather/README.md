# CI-3: MapReduce — Hottest / Coolest Year

**Aim:** Use the MapReduce paradigm to find the hottest and coolest year in a weather dataset.

Two equivalent implementations are provided:

| Folder / file | Tech | Use when |
|---------------|------|----------|
| `mapreduce_weather.py` (this folder) | Python `concurrent.futures.ProcessPoolExecutor` | Quick demo. No setup. Same paradigm in pure Python. |
| [`hadoop/`](hadoop/) | Real Apache Hadoop MapReduce in Java | You want to demonstrate the full HDFS + YARN + MapReduce pipeline. |

## Run the Python version
```bash
python mapreduce_weather.py
```
Auto-creates `weather_data.csv` on first run, runs the parallel MapReduce, prints results.

## Run the Hadoop version
```bash
cd hadoop
./run.sh
```
The script verifies that all five Hadoop daemons (NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager) are running (starts any missing ones), compiles the Java code, packages the JAR, uploads input to HDFS, submits the YARN job, and prints the results. See [hadoop/README.md](hadoop/README.md) for full details and prerequisites.

## How both versions implement the same algorithm

- **Map** — for each row in the CSV, emit `(year, temperature)`.
- **Shuffle** — group all temperatures by year (Hadoop framework or Python dict merging).
- **Reduce** — for each year compute `max` and `min`.
- **Final** — pick the year with the largest max (hottest) and smallest min (coolest).

The *paradigm* is identical; the *infrastructure* is the only difference.
