// Driver: configures and submits the MapReduce job to the Hadoop cluster.
// Wires the Mapper and Reducer classes together and sets input/output paths.
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {
    public static void main(String[] args) throws Exception {

        // Hadoop configuration loaded from XML files (core-site.xml, hdfs-site.xml etc.).
        Configuration conf = new Configuration();

        // Create the job and give it a human-readable name.
        Job job = Job.getInstance(conf, "word count");

        // Tell Hadoop which jar contains the user code (this class lives in it).
        job.setJarByClass(WordCount.class);

        // Plug in the Mapper and Reducer implementations.
        job.setMapperClass(WordMapper.class);
        job.setReducerClass(WordReducer.class);

        // Declare the output (key, value) types -- Hadoop uses these for serialization.
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // args[0] is the HDFS input path, args[1] is the HDFS output path (must not exist yet).
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // Submit the job and wait; exit 0 on success, 1 on failure.
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
