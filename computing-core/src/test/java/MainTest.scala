import java.text.SimpleDateFormat

import org.apache.hadoop.hbase.HBaseConfiguration
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object MainTest {
  def main(args: Array[String]): Unit = {
    val formater = new SimpleDateFormat("EEE MMM dd HH:mm:ss yyyy")
    val time = formater.parse("Fri Oct 13 22:15:05 2017")
    print(time.getTime)
  }
}
