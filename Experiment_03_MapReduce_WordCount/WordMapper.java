// Mapper stage: reads each input line and emits (word, 1) pairs.
// Hadoop's framework feeds one line at a time as `value`.
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

// Generic params: <InputKey, InputValue, OutputKey, OutputValue>.
// Input key is the byte offset (Object). Input value is the line (Text).
// Output is (word, 1) -> (Text, IntWritable).
public class WordMapper extends Mapper<Object, Text, Text, IntWritable> {

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {

        // Split the line into individual word tokens (default delimiters: whitespace).
        StringTokenizer st = new StringTokenizer(value.toString());

        // For every token emit (word, 1). The framework will group these by key.
        while (st.hasMoreTokens()) {
            context.write(new Text(st.nextToken()), new IntWritable(1));
        }
    }
}
