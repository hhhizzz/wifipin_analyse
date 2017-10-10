package edu.sxu.cs.analysis

import org.apache.hadoop.hbase.{CellUtil, HBaseConfiguration}
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.log4j.{Level, LogManager}
import it.nerdammer.spark.hbase._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import scala.collection.JavaConversions._

object OfflineEachDay {
  def main(args: Array[String]): Unit = {
    val oneDayBefore = System.currentTimeMillis() - 24 * 3600 * 1000

    val today = timeToDay(oneDayBefore)

    val zkQuorum = "host0.com,host2.com,host1.com"
    //日志输出设置为warn
    val log = LogManager.getLogger("org")
    log.setLevel(Level.WARN)
    //设置spark环境
    val conf = new SparkConf().setAppName("computing-core-offline")
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
    config.set(TableInputFormat.INPUT_TABLE, "stay")

    val hbaseDataStay = sc.newAPIHadoopRDD(config, classOf[TableInputFormat], classOf[ImmutableBytesWritable], classOf[Result])


    //structure (mac, wifiPin, timeStamp)
    val dataList = hbaseDataStay
      .map(row => (Bytes.toString(row._2.getRow), row._2.getColumnCells("stay".getBytes(), "wifiPin".getBytes())))
      .flatMapValues(_.toList)
      .map(row => (row._1, Bytes.toInt(CellUtil.cloneValue(row._2)), row._2.getTimestamp))
      .cache()

    //structure (wifiPin, SpaceDay)
    val spaceDay = dataList
      .filter(row => row._3 < oneDayBefore)
      .map(row => ((row._1, row._2), row._3))
      .reduceByKey(math.max)
      .map(row => (row._1._2, today - timeToDay(row._2)))
      .groupByKey()
      .mapValues(row => 1.0 * row.sum / row.size)
      .cache()


    spaceDay.map(row => (row._1, row._2, today))
      .toHBaseTable("spaceDay")
      .inColumnFamily("spaceDay")
      .toColumns("spaceDay", "day")
      .save

  }

  def timeToDay(timeStamp: Long): Long = {
    (timeStamp - 1506787200000L) / (1000 * 3600 * 24)
  }

}
