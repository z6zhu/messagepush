/*
Navicat MySQL Data Transfer

Source Server         : msgpush
Source Server Version : 50634
Source Host           : rdshvolo9wz425h29nlco.mysql.rds.aliyuncs.com:3306
Source Database       : jx_msg_log

Target Server Type    : MYSQL
Target Server Version : 50634
File Encoding         : 65001

Date: 2018-01-09 19:03:51
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for log_msg_send_record_test
-- ----------------------------
DROP TABLE IF EXISTS `log_msg_send_record_test`;
CREATE TABLE `log_msg_send_record_test` (
  `id` varchar(64) NOT NULL,
  `company` int(11) DEFAULT NULL,
  `mobile` varchar(20000) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `sendTime` varchar(50) DEFAULT NULL,
  `requestStatus` varchar(1000) DEFAULT NULL,
  `returnStatus` varchar(50) DEFAULT NULL,
  `message` varchar(50) DEFAULT NULL,
  `remainPoint` varchar(50) DEFAULT NULL,
  `taskId` varchar(50) DEFAULT NULL,
  `successCounts` varchar(50) DEFAULT NULL,
  `createTime` datetime DEFAULT NULL,
  `updateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
