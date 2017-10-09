package edu.sxu.cs.analysis


import org.apache.log4j.{Level, LogManager}
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka.KafkaUtils


/**
  * 分析程序入口
  *
  * Created by Qiwei Huang on 2017/10/04 16:35.
  * E-mail address is qiwei_huang@qq.com.
  * Copyright © Qiwei Huang SXU. All Rights Reserved.
  *
  * @author Qiwei Huang
  */
object Main {
  def main(args: Array[String]): Unit = {
    //需要用到的参数
    val zkQuorum = "host0.com,host2.com,host1.com"
    val group = "1"
    val topics = "test"
    val numThreads = "2"

    //把日志记录调整为WARN级别，以减少输出
    val log = LogManager.getLogger("org")
    log.setLevel(Level.WARN)

    //启动streaming
    val conf = new SparkConf().setAppName("computing-core").setMaster("local[2]")
    conf.set("spark.hbase.host", zkQuorum)
    val ssc = new StreamingContext(conf, Seconds(20))


    //从kafka获取数据

    // 将topics转换成topic-->numThreads的哈稀表
    val topicMap = topics.split(",").map((_, numThreads.toInt)).toMap
    // 创建连接Kafka的消费者链接
    val inputDStream = KafkaUtils.createStream(ssc, zkQuorum, group, topicMap)

    //实时分析
    RealTimeAnalysis.analysis(inputDStream)




    ssc.start()
    ssc.awaitTermination()

  }
}
