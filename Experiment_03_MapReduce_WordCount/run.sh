#!/usr/bin/env bash
# Interactive MapReduce WordCount runner.
# Lets the user pick or paste their own input, runs the Hadoop job,
# then displays the result sorted by frequency.

set -e
cd "$(dirname "$0")"

# ---------------------------------------------------------------- helpers ----
press_enter() { read -rp "Press Enter to continue..." _; }

ensure_daemons() {
    # Confirm all 5 Hadoop daemons are running; print which (if any) are missing.
    local needed="NameNode DataNode SecondaryNameNode ResourceManager NodeManager"
    local running
    running="$(jps | awk '{print $2}')"
    local missing=""
    for d in $needed; do
        echo "$running" | grep -q "^${d}$" || missing="$missing $d"
    done
    if [ -n "$missing" ]; then
        echo "ERROR: these Hadoop daemons are not running:$missing"
        echo "Start them with:"
        echo "  hdfs --daemon start namenode"
        echo "  hdfs --daemon start datanode"
        echo "  hdfs --daemon start secondarynamenode"
        echo "  yarn --daemon start resourcemanager"
        echo "  yarn --daemon start nodemanager"
        exit 1
    fi
}

ensure_jar() {
    # Compile if wc.jar is missing or the source has changed.
    if [ ! -f wc.jar ] || [ WordMapper.java -nt wc.jar ] || \
       [ WordReducer.java -nt wc.jar ] || [ WordCount.java -nt wc.jar ]; then
        echo ">>> Compiling..."
        javac -classpath "$(hadoop classpath)" -d . WordMapper.java WordReducer.java WordCount.java
        jar -cvf wc.jar *.class >/dev/null
        echo "    wc.jar built."
    fi
}

# ---------------------------------------------------------------- start ----
echo "============================================================"
echo " Hadoop MapReduce — Word Count (interactive)"
echo "============================================================"

ensure_daemons
ensure_jar

# ---------------------------------------------------------------- input ----
echo
echo "Choose input source:"
echo "  1) Use the bundled input.txt"
echo "  2) Paste your own text"
echo "  3) Provide a path to a local text file"
read -rp "Option [1-3]: " choice

INPUT_LOCAL=""
case "$choice" in
    1)
        INPUT_LOCAL="$(pwd)/input.txt"
        ;;
    2)
        echo "Paste your text. End with a single line containing only END:"
        INPUT_LOCAL="$(mktemp /tmp/wc_input_XXXX.txt)"
        while IFS= read -r line; do
            [ "$line" = "END" ] && break
            echo "$line" >> "$INPUT_LOCAL"
        done
        ;;
    3)
        read -rp "Path to file: " INPUT_LOCAL
        if [ ! -f "$INPUT_LOCAL" ]; then
            echo "ERROR: file not found: $INPUT_LOCAL"
            exit 1
        fi
        ;;
    *)
        echo "Invalid option."
        exit 1
        ;;
esac

echo
echo "Input preview (first 5 lines):"
head -5 "$INPUT_LOCAL" | sed 's/^/    /'
echo

# ---------------------------------------------------------------- HDFS ----
echo ">>> Uploading input to HDFS at /input/..."
hadoop fs -mkdir -p /input
hadoop fs -rm -f /input/* >/dev/null 2>&1 || true
hadoop fs -put -f "$INPUT_LOCAL" /input/

echo ">>> Removing any old /output..."
hadoop fs -rm -r -f /output >/dev/null 2>&1 || true

# ---------------------------------------------------------------- run ----
echo
echo ">>> Submitting MapReduce job..."
hadoop jar wc.jar WordCount /input /output

# ---------------------------------------------------------------- show ----
echo
echo "============================================================"
echo " RESULT  (top 20 words by frequency)"
echo "============================================================"
hadoop fs -cat /output/part-r-00000 \
    | sort -k2 -n -r \
    | awk 'BEGIN{printf "%-20s %s\n","WORD","COUNT"; print "------------------------------"} {printf "%-20s %s\n",$1,$2}' \
    | head -22
echo "============================================================"
echo "(Full output stored in HDFS at /output/part-r-00000)"
echo "View raw : hadoop fs -cat /output/part-r-00000"
echo "Web UI   : http://localhost:9870  (HDFS)"
echo "           http://localhost:8088  (YARN)"
