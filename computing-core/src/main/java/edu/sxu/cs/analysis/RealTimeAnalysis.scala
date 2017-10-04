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

    //structure (pinNumber,(mac1,power1))
    val dataArray = jsonArray.
      flatMapValues(JSONUtil.getArray)
      .map(data => (data._1, (data._2.getString("mac"), data._2.getInt("power")))).cache()

    //检测到用户数 structure (pinNumber, number)
    val countByPin = dataArray.map(line=>(line._1,1)).reduceByKey(_+_)
    countByPin.print()

  }
}
