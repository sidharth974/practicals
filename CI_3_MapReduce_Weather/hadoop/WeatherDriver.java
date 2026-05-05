// Driver for the Hadoop MapReduce weather job.
// Wires the Mapper and Reducer together and submits the job to YARN.
// Usage: hadoop jar weather.jar WeatherDriver <inputPath> <outputPath>
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WeatherDriver {

    public static void main(String[] args) throws Exception {

        if (args.length != 2) {
            System.err.println("Usage: hadoop jar weather.jar WeatherDriver <input> <output>");
            System.exit(2);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "weather max-min by year");

        // Tell Hadoop which jar to ship to the cluster nodes.
        job.setJarByClass(WeatherDriver.class);
        job.setMapperClass(WeatherMapper.class);
        job.setReducerClass(WeatherReducer.class);

        // Mapper output types (must match WeatherMapper signature).
        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(DoubleWritable.class);

        // Reducer / final output types.
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // Submit and wait. Exit 0 on success, 1 on failure.
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
