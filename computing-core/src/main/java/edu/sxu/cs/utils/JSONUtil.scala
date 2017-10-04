package edu.sxu.cs.utils

import org.json.{JSONArray, JSONObject}

object JSONUtil {
  def getArray(json: JSONArray): Array[JSONObject] = {
    val length = json.length()
    val result = new Array[JSONObject](length)
    for (i <- 0 until length) {
      result.update(i, json.getJSONObject(i))
    }
    result
  }
}
