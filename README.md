# Wi-Fi Pin Analysis

> WIFI探针是一种可以记录附近mac地址的嗅探器，可以根据收集到的mac地址进行数据分析，获得附近的人流量、入店量、驻留时长等信息  
> 本系统以Spark + Hadoop为核心，搭建了基于WIFI探针的大数据分析系统

## 介绍

### Airdump.py

用于产生探针数据 运行于OpenWrt操作系统的路由器中

### Computing-Core

使用spark对数据进行处理 存入hbase和mysql中

## web-Core

展示系统后端

## Receive-Core

从wifi探针收集数据