// Reducer for the weather job.
// Receives (year, [list of all temperatures recorded that year]).
// Emits (year, "max=<MAX_TEMP>, min=<MIN_TEMP>").
// The user / driver scans the final output to pick hottest (largest max)
// and coolest (smallest min) year.
import java.io.IOException;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WeatherReducer extends Reducer<IntWritable, DoubleWritable, IntWritable, Text> {

    @Override
    public void reduce(IntWritable year, Iterable<DoubleWritable> temps, Context context)
            throws IOException, InterruptedException {

        double max = Double.NEGATIVE_INFINITY;
        double min = Double.POSITIVE_INFINITY;

        // One pass over all temperatures for this year.
        for (DoubleWritable t : temps) {
            double v = t.get();
            if (v > max) max = v;
            if (v < min) min = v;
        }

        context.write(year, new Text("max=" + max + ", min=" + min));
    }
}
