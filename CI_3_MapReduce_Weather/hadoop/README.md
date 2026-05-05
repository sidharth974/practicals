# CI-3 — Hadoop MapReduce version

Same problem as the parent folder (find hottest & coolest year), but implemented as a real Hadoop MapReduce job in Java.

## Files
- `WeatherMapper.java`  — emits `(year, temperature)` for each row.
- `WeatherReducer.java` — for each year emits `max=<x>, min=<y>`.
- `WeatherDriver.java`  — wires Mapper+Reducer and submits the job.
- `weather_data.csv`    — sample input.
- `run.sh`              — one-shot: starts daemons if needed, compiles, packages, uploads to HDFS, runs the job, prints results.

## Prerequisites
- Hadoop 3.x installed at `/opt/hadoop` and on `PATH`.
- JDK 8 or 11 (Java 21 will fail — set `JAVA_HOME` in `hadoop-env.sh` to a Java 11 install).
- The Hadoop pseudo-distributed config you set up earlier (NameNode/DataNode/RM/NM running). The script auto-starts any missing daemon.

## Run
```bash
cd ~/SITRC/CI_3_MapReduce_Weather/hadoop
./run.sh
```

## Expected output (key parts)
```
Daemons:
  ... NameNode DataNode SecondaryNameNode ResourceManager NodeManager Jps

>>> Compiling Java sources
    Built weather.jar
>>> Uploading input to HDFS at /weather/input/
>>> Submitting MapReduce job to YARN
... map 100% reduce 100% ...

==========================================
 Per-year max & min temperature
==========================================
2000	max=12.0, min=9.8
2001	max=8.1, min=5.2
2002	max=15.3, min=14.1
2003	max=11.5, min=7.0

==========================================
 Hottest / Coolest year
==========================================
Hottest year: 2002 with max temperature 15.3°C
Coolest year: 2001 with min temperature 5.2°C
```

## Web UIs while the job runs
- HDFS browser : http://localhost:9870
- YARN tracker : http://localhost:8088
