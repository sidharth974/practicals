#!/usr/bin/env bash
# ============================================================
# Hadoop 3.4.1 single-node setup + run Experiment 3 (Word Count)
# Tested on Kali / Ubuntu 22.04+ with Java 11
# Idempotent — safe to re-run if any step fails.
# ============================================================
set -e

HADOOP_VERSION=3.4.1
HADOOP_DIR=/opt/hadoop
JAVA11=/usr/lib/jvm/java-11-openjdk-amd64
PROJECT_DIR="$HOME/SITRC/Experiment_03_MapReduce_WordCount"

echo ">>> [1/9] Installing Java 11 + SSH + tools"
sudo apt-get update -y || true
sudo apt-get install -y openjdk-11-jdk ssh pdsh wget

echo ">>> [2/9] Starting SSH daemon (Kali disables by default)"
sudo systemctl enable --now ssh
[ -f "$HOME/.ssh/id_rsa" ] || ssh-keygen -t rsa -P '' -f "$HOME/.ssh/id_rsa"
grep -qF "$(cat ~/.ssh/id_rsa.pub)" ~/.ssh/authorized_keys 2>/dev/null || \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
ssh -o StrictHostKeyChecking=no localhost "echo SSH OK"

echo ">>> [3/9] Downloading Hadoop $HADOOP_VERSION"
if [ ! -d "$HADOOP_DIR" ]; then
    cd /tmp
    [ -f hadoop-${HADOOP_VERSION}.tar.gz ] || \
        wget https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz
    sudo tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt/
    sudo mv /opt/hadoop-${HADOOP_VERSION} "$HADOOP_DIR"
    sudo chown -R "$USER:$USER" "$HADOOP_DIR"
else
    echo "    Hadoop already installed — skipping."
fi

echo ">>> [4/9] Writing env vars to ~/.bashrc"
if ! grep -q "HADOOP_HOME=$HADOOP_DIR" ~/.bashrc; then
cat >> ~/.bashrc <<EOF

# Hadoop
export JAVA_HOME=$JAVA11
export HADOOP_HOME=$HADOOP_DIR
export HADOOP_MAPRED_HOME=\$HADOOP_HOME
export HADOOP_COMMON_HOME=\$HADOOP_HOME
export HADOOP_HDFS_HOME=\$HADOOP_HOME
export YARN_HOME=\$HADOOP_HOME
export PDSH_RCMD_TYPE=ssh
export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin
EOF
fi
export JAVA_HOME=$JAVA11
export HADOOP_HOME=$HADOOP_DIR
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export PDSH_RCMD_TYPE=ssh
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin

# Bake JAVA_HOME into Hadoop's own env file (Java 11 specifically — Hadoop 3.4 chokes on Java 21)
sudo sed -i "s|^export JAVA_HOME=.*|export JAVA_HOME=$JAVA11|" "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"
grep -q "^export JAVA_HOME=$JAVA11" "$HADOOP_HOME/etc/hadoop/hadoop-env.sh" || \
    echo "export JAVA_HOME=$JAVA11" | sudo tee -a "$HADOOP_HOME/etc/hadoop/hadoop-env.sh" >/dev/null

echo ">>> [5/9] Writing pseudo-distributed XML configs"
CONF=$HADOOP_HOME/etc/hadoop
sudo tee $CONF/core-site.xml >/dev/null <<'EOF'
<configuration>
  <property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property>
</configuration>
EOF
sudo tee $CONF/hdfs-site.xml >/dev/null <<'EOF'
<configuration>
  <property><name>dfs.replication</name><value>1</value></property>
</configuration>
EOF
sudo tee $CONF/mapred-site.xml >/dev/null <<'EOF'
<configuration>
  <property><name>mapreduce.framework.name</name><value>yarn</value></property>
  <property><name>mapreduce.application.classpath</name>
    <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
  </property>
</configuration>
EOF
sudo tee $CONF/yarn-site.xml >/dev/null <<'EOF'
<configuration>
  <property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>
  <property><name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
  </property>
</configuration>
EOF

echo ">>> [6/9] Killing any stale daemons + clearing pid files"
jps | awk '$2!="Jps" && $2!="Main" {print $1}' | xargs -r kill -9 2>/dev/null || true
rm -f /tmp/hadoop-$USER-*.pid /tmp/yarn-$USER-*.pid

echo ">>> [7/9] Formatting HDFS (only if not already formatted)"
if [ ! -d "/tmp/hadoop-$USER/dfs/name" ]; then
    hdfs namenode -format -force -nonInteractive >/dev/null 2>&1
    echo "    Format OK"
else
    echo "    Already formatted — skipping"
fi

echo ">>> [8/9] Starting daemons directly (no pdsh, avoids the Kali start-dfs.sh hang)"
hdfs --daemon start namenode
hdfs --daemon start datanode
hdfs --daemon start secondarynamenode
yarn --daemon start resourcemanager
yarn --daemon start nodemanager
sleep 5
jps

echo ">>> [9/9] Compiling and running Experiment 3"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "    SKIP: $PROJECT_DIR not found. Clone the repo first."
else
    cd "$PROJECT_DIR"
    PATH=$JAVA11/bin:$PATH javac -classpath "$(hadoop classpath)" -d . *.java
    jar -cvf wc.jar *.class >/dev/null
    hadoop fs -mkdir -p /input
    hadoop fs -put -f input.txt /input
    hadoop fs -rm -r -f /output 2>/dev/null || true
    hadoop jar wc.jar WordCount /input /output
    echo "============= RESULT ============="
    hadoop fs -cat /output/part-r-00000
    echo "=================================="
fi

echo
echo "DONE.  HDFS UI: http://localhost:9870  |  YARN UI: http://localhost:8088"
echo "Stop with:"
echo "  yarn --daemon stop nodemanager && yarn --daemon stop resourcemanager"
echo "  hdfs --daemon stop secondarynamenode && hdfs --daemon stop datanode && hdfs --daemon stop namenode"
