import org.apache.hadoop.hbase.HBaseConfiguration
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession

object MainTest {
  def main(args: Array[String]): Unit = {
    val zkQuorum = "host0.com,host2.com,host1.com"
    //设置spark环境
    val conf = new SparkConf().setAppName("computing-core-offline").setMaster("local[2]")
    conf.set("spark.hbase.host", zkQuorum)
    val spark = SparkSession
      .builder()
      .config(conf)
      .getOrCreate()
    val sc = spark.sparkContext
    val config = HBaseConfiguration.create()
    config.addResource("hbase-site.xml")
    config.addResource("core-site.xml")
    config.set(TableInputFormat.SCAN_MAXVERSIONS, "999999")
    config.set(TableInputFormat.INPUT_TABLE, "remain")

    val hbaseDataStay = sc.newAPIHadoopRDD(config, classOf[TableInputFormat], classOf[ImmutableBytesWritable], classOf[Result])

    hbaseDataStay
      .mapValues(result => Bytes.toDouble(result.getValue("remain".getBytes(), "time".getBytes())))
      .foreach(println)
  }
}
