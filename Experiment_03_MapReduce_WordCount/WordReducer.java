// Reducer stage: receives all values for a given word (key) and sums them
// to produce the total count for that word.
import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

// Generic params: <InputKey, InputValue, OutputKey, OutputValue>.
// Input is (word, [1, 1, 1, ...]) after shuffle/sort by Hadoop.
// Output is (word, totalCount).
public class WordReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {

        int sum = 0;

        // Iterate the list of 1s emitted by the mapper for this word and add them up.
        for (IntWritable val : values) {
            sum += val.get();
        }

        // Emit the final (word, totalCount) pair to be written to output.
        context.write(key, new IntWritable(sum));
    }
}
