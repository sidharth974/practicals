# Experiment 3: MapReduce Word Count

**Aim:** Implement MapReduce under Hadoop to count occurrences of each word in a text file.

**Tech:** Java + Apache Hadoop (`org.apache.hadoop.mapreduce`).

## Requirements
- JDK 8 or higher
- Apache Hadoop 3.x installed and configured (`HADOOP_HOME` set, `hadoop` on PATH)
- HDFS running (`start-dfs.sh`) — required only if running on a real cluster; local mode also works

## Files
- `WordMapper.java` — Mapper: emits `(word, 1)` for each token
- `WordReducer.java` — Reducer: sums counts per word
- `WordCount.java` — Driver: configures and submits the MapReduce job
- `input.txt` — sample input text

## How to run
```bash
# 1. Compile against Hadoop libraries
javac -classpath "$(hadoop classpath)" -d . WordMapper.java WordReducer.java WordCount.java

# 2. Package into a runnable jar
jar -cvf wc.jar *.class

# 3. Upload input to HDFS (skip /input creation if it exists)
hadoop fs -mkdir -p /input
hadoop fs -put -f input.txt /input

# 4. Make sure /output does not exist (Hadoop refuses to overwrite)
hadoop fs -rm -r -f /output

# 5. Submit the job
hadoop jar wc.jar WordCount /input /output

# 6. View the result
hadoop fs -cat /output/part-r-00000
```

## Expected Output
```
fun       1
hadoop    2
hello     3
is        2
mapreduce 2
powerful  1
world     2
```

## Common Errors & Fixes
| Error | Fix |
|-------|-----|
| `hadoop: command not found` | Install Hadoop and add `$HADOOP_HOME/bin` to `PATH` |
| `Output directory already exists` | `hadoop fs -rm -r /output` before re-running |
| `ClassNotFoundException` during `javac` | `$(hadoop classpath)` returned empty — verify Hadoop install |
