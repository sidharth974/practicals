// Mapper for the weather job.
// Input  : CSV lines of the form "year,temperature".
// Output : (year, temperature) pairs that the Reducer will group by year.
import java.io.IOException;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WeatherMapper extends Mapper<LongWritable, Text, IntWritable, DoubleWritable> {

    @Override
    public void map(LongWritable offset, Text line, Context context)
            throws IOException, InterruptedException {

        String s = line.toString().trim();

        // Skip the CSV header line.
        if (s.isEmpty() || s.startsWith("year")) {
            return;
        }

        // Parse "year,temperature" carefully -- malformed rows are silently skipped.
        String[] parts = s.split(",");
        if (parts.length < 2) {
            return;
        }
        try {
            int    year = Integer.parseInt(parts[0].trim());
            double temp = Double.parseDouble(parts[1].trim());
            context.write(new IntWritable(year), new DoubleWritable(temp));
        } catch (NumberFormatException e) {
            // Bad row -- skip silently so a single dirty line doesn't kill the job.
        }
    }
}
