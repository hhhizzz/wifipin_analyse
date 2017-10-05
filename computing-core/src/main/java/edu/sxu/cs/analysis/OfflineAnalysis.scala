package edu.sxu.cs.analysis

import org.apache.log4j.{Level, LogManager}
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.streaming.{Seconds, StreamingContext}
import it.nerdammer.spark.hbase._

object OfflineAnalysis {
  def main(args: Array[String]): Unit = {
    val zkQuorum = "host0.com,host2.com,host1.com"
    //日志输出设置为warn
    val log = LogManager.getLogger("org")
    log.setLevel(Level.WARN)

    //启动streaming
    val conf = new SparkConf().setAppName("computing-core").setMaster("local[2]")
    conf.set("spark.hbase.host", zkQuorum)
    val ssc = new StreamingContext(conf, Seconds(20))
    val spark = SparkSession
      .builder()
      .config(conf)
      .getOrCreate()
    val sc = spark.sparkContext



  }
}
