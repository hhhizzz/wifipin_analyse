package edu.sxu.cs.analysis

import edu.sxu.cs.utils.JSONUtil
import org.apache.spark.streaming.dstream.ReceiverInputDStream
import org.json.JSONObject

object RealTimeAnalysis {
  def analysis(inputDStream: ReceiverInputDStream[(String, String)]): Unit = {
    val lines = inputDStream.map(_._2)
    //structure (pinNumber,JSONArray)
    val jsonArray = lines
      .map(new JSONObject(_))
      .map(obj => (obj.getInt("wifiPin"), obj.getJSONArray("data")))

    //structure (mac1,pinNumber,power1)
    val dataArray = jsonArray.
      flatMapValues(JSONUtil.getArray)
      .map(data => (data._2.getString("mac"), data._1, data._2.getInt("power"))).cache()

    //检测到用户数 structure (pinNumber, number)
    val countByPin = dataArray.map(line => (line._2, 1)).reduceByKey(_ + _)
    countByPin.print()

//    //存入hbase
//    import it.nerdammer.spark.hbase._
//    dataArray.foreachRDD(rdd =>
//      rdd.toHBaseTable("mac")
//        .inColumnFamily("mac")
//        .toColumns("wifiPin", "power")
//        .save
//    )

  }
}
