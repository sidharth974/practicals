#!/usr/bin/env bash
# Build, deploy and run the Hadoop weather MapReduce job.
# Assumes Hadoop is installed at /opt/hadoop and the daemons are running.

set -e
cd "$(dirname "$0")"

# 1. Make sure Hadoop env is loaded.
source ~/.bashrc

# 2. Make sure all 5 daemons are alive; start any that are missing.
for d in NameNode DataNode SecondaryNameNode ResourceManager NodeManager; do
    if ! jps | grep -q "^[0-9]* $d$"; then
        echo "Starting missing daemon: $d"
        case $d in
            NameNode|DataNode|SecondaryNameNode) hdfs --daemon start "${d,,}" ;;
            ResourceManager|NodeManager)         yarn --daemon start "${d,,}" ;;
        esac
    fi
done
sleep 3
echo "Daemons:" ; jps

# 3. Compile.
echo ">>> Compiling Java sources"
javac -classpath "$(hadoop classpath)" -d . WeatherMapper.java WeatherReducer.java WeatherDriver.java
jar -cvf weather.jar *.class >/dev/null
echo "    Built weather.jar"

# 4. Upload input to HDFS.
echo ">>> Uploading input to HDFS at /weather/input/"
hadoop fs -mkdir -p /weather/input
hadoop fs -put -f weather_data.csv /weather/input/

# 5. Make sure output dir doesn't exist (Hadoop refuses to overwrite).
hadoop fs -rm -r -f /weather/output 2>/dev/null || true

# 6. Run the job.
echo ">>> Submitting MapReduce job to YARN"
hadoop jar weather.jar WeatherDriver /weather/input /weather/output

# 7. Show results, then derive hottest / coolest.
echo
echo "=========================================="
echo " Per-year max & min temperature"
echo "=========================================="
hadoop fs -cat /weather/output/part-r-00000

echo
echo "=========================================="
echo " Hottest / Coolest year"
echo "=========================================="
hadoop fs -cat /weather/output/part-r-00000 | python3 -c "
import sys, re
records = []
for line in sys.stdin:
    m = re.match(r'(\d+)\s+max=([\-\d\.]+),\s*min=([\-\d\.]+)', line)
    if m:
        records.append((int(m.group(1)), float(m.group(2)), float(m.group(3))))
hottest = max(records, key=lambda r: r[1])
coolest = min(records, key=lambda r: r[2])
print(f'Hottest year: {hottest[0]} with max temperature {hottest[1]}°C')
print(f'Coolest year: {coolest[0]} with min temperature {coolest[2]}°C')
"
