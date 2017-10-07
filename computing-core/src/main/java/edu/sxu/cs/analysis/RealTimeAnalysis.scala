package edu.sxu.cs.analysis

import java.util.Date

import edu.sxu.cs.utils.JSONUtil
import org.apache.spark.streaming.dstream.ReceiverInputDStream
import org.json.JSONObject
import it.nerdammer.spark.hbase._

object RealTimeAnalysis {
  def analysis(inputDStream: ReceiverInputDStream[(String, String)]): Unit = {
    //今天
    val today = new Date().getDay - new Date(1506787200).getDay

    val lines = inputDStream.map(_._2)
    //structure (pinNumber,JSONArray)
    val jsonArray = lines
      .map(new JSONObject(_))
      .map(obj => (obj.getInt("wifiPin"), obj.getJSONArray("data")))

    //structure (pinNumber,mac1,power1,time1)
    val dataArray = jsonArray
      .flatMapValues(JSONUtil.getArray)
      .map(data => (data._1, data._2.getString("mac"), data._2.getInt("power"), data._2.getInt("time")))
      .cache()

    //structure ((pinNumber,mac1),time1))
    val peopleFilter = dataArray
      .filter(_._3 >= (-100))
      .map(row => ((row._1, row._2), row._4))
      .cache()

    //structure (pinNumber,mac1,time)
    val timeDiff = peopleFilter
      .groupByKey()
      .map(row => (row._1._1, row._1._2, row._2.max - row._2.min))
      .cache()

    //structure (pinNumber,number)
    val peopleAll = timeDiff
      .map(row => (row._1, 1))
      .reduceByKey(_ + _)
      .cache()

    //structure (pinNumber, number)
    val peopleGetIn = timeDiff
      .filter(row => row._3 >= 8)
      .map(row => (row._1, 1))
      .reduceByKey(_ + _)
      .cache()

    //structure (pinNumber, get_in_rate)
    val rateGetIn = peopleGetIn
      .union(peopleAll)
      .map(row => (row._1, row._2 * 1.0))
      .reduceByKey({ (row1, row2) =>
        if (row1 == 0 || row2 == 0)
          0
        else if (row1 > row2)
          row2 / row1
        else
          row1 / row2
      })
      .cache()
    rateGetIn.print()

    //structure (mac1, wifiPin, time, today)
    val timeDiffSave = timeDiff
      .map(row => (row._2, row._1, row._3, today))
      .filter(row => row._3 >= 8)
      .cache()

    peopleGetIn.foreachRDD(rdd =>
      rdd.toHBaseTable("getIn")
        .inColumnFamily("getIn")
        .toColumns("number")
        .save
    )
    rateGetIn.foreachRDD(rdd =>
      rdd.toHBaseTable("getInRate")
        .inColumnFamily("getInRate")
        .toColumns("rate")
        .save
    )

    timeDiffSave
      .foreachRDD(rdd =>
        rdd.toHBaseTable("stay")
          .inColumnFamily("stay")
          .toColumns("wifiPin", "time", "day")
          .save
      )

  }
}
