package edu.sxu.cs.analysis

import org.apache.hadoop.hbase.{CellUtil, HBaseConfiguration}
import org.apache.hadoop.hbase.client.Result
import org.apache.hadoop.hbase.io.ImmutableBytesWritable
import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import it.nerdammer.spark.hbase._
import java.util.Calendar
import org.apache.log4j.{Level, LogManager}

import scala.collection.JavaConversions._

object OfflineEachHour {
  def main(args: Array[String]): Unit = {
    //时间设置，从2018-10-01开始计算
    val cal = Calendar.getInstance
    val today = (System.currentTimeMillis() - 1506787200000L) / (1000 * 3600 * 24)
    val currentHour = cal.get(Calendar.HOUR_OF_DAY)

    val zkQuorum = "host0.com,host2.com,host1.com"
    //日志输出设置为warn
    val log = LogManager.getLogger("org")
    log.setLevel(Level.WARN)
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
    config.set(TableInputFormat.INPUT_TABLE, "stay")

    val hbaseDataStay = sc.newAPIHadoopRDD(config, classOf[TableInputFormat], classOf[ImmutableBytesWritable], classOf[Result])

    //structure (wifiPin,number)
    val wifiPinCount = hbaseDataStay
      .map(row => (Bytes.toInt(row._2.getValue("stay".getBytes(), "wifiPin".getBytes())), Bytes.toString(row._2.getRow)))
      .map(row => (row._1, 1))
      .reduceByKey(_ + _)

    //structure ((mac,wifiPin),key,value)
    val dataListStay = hbaseDataStay
      .map(row => ((Bytes.toString(row._2.getRow), Bytes.toInt(row._2.getValue("stay".getBytes(), "wifiPin".getBytes()))), row._2))
      .flatMapValues(_.listCells())
      .map(row => (row._1._2, Bytes.toString(CellUtil.cloneQualifier(row._2)), Bytes.toInt(CellUtil.cloneValue(row._2)), row._2.getTimestamp))
      .cache()

    //structure (wifiPin,time_sum)
    val sumStay = dataListStay
      .filter(row => row._2.equals("time"))
      .filter(row => row._4 > currentHour)
      .map(row => (row._1, row._3))
      .reduceByKey(_ + _)
      .cache()

    //structure (wifiPin, time_avg)
    val resultStay = sumStay
      .join(wifiPinCount)
      .map(row => (row._1, row._2._1 * 1.0 / row._2._2))
      .cache()


    resultStay
      .map(row => (row._1, row._2, today, currentHour))
      .toHBaseTable("remain")
      .inColumnFamily("remain")
      .toColumns("time", "day", "hour")
      .save


  }
}
