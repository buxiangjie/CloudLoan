# -*- coding: UTF-8 -*-
"""
@auth:buxiangjie
@date:2020-05-12 11:26:00
@describe: 修改saas数据的一些接口
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Query, Form, Depends, File, UploadFile, Request
from dateutil.relativedelta import relativedelta
from common.tools_api_sql import ToolsSql
from tools_api.item import *
from typing import List
from fastapi import status

router = APIRouter()


@router.get("/", name="首页", status_code=status.HTTP_200_OK)
async def index():
	return "hello world"


@router.delete("/ids", name="删除异常数据")
async def ids(env: str, dtype: str, lis: List):
	"""
	- env: 数据所在环境 test/qa
	- dtype: 数据类型 projectid/assetid
	- lis: ID列表[1,2,3,4]
	"""
	if dtype == "asset":
		for i in lis:
			mes = ToolsSql.del_asset_data(environment=env, asset_id=i)
		return mes
	elif dtype == "project":
		for i in lis:
			mess = ToolsSql.del_project_data(environment=env, projectid=i)
		return mess
	else:
		return "不支持的类型"


@router.post("/file", name="文件上传测试")
async def upload_file(file: UploadFile = File(...)):
	content = await file.read()
	return {"file": content}


@router.post("/overdue/change", name="修改还款计划为逾期")
def change_overdue(item: OverdueItem):
	"""
	- environment: 要修改数据的环境 test/qa
	- project_id: 进件ID
	- period: 期数 有两种方式 1. 单期数 比如:n=1,2,3 代表从第一期开始，要逾期n期 2. 区间数 比如:5-7 代表从第5期开始[5，6，7]3期
	- start_date: 填写期数的最后一期还款计划时间 比如period=2 start_date=2020-12-24 则还款计划时间会变更为{1: 2020-11-24, 2:202012-24}
	"""
	if "-" in item.period:
		periods_list = item.period.split("-")
		pers = list(range(int(periods_list[0]), int(periods_list[1]) + 1))
		count = int(periods_list[1]) - int(periods_list[0])
	else:
		pers = list(range(1, int(item.period) + 1))
		count = int(item.period) - 1
	try:
		for per in pers:
			business_date = ''
			if per == pers[-1]:
				business_date = item.start_date
			else:
				business_date = str(item.start_date - relativedelta(months=count)).split(" ")[0]
			ToolsSql.change_repayment_plan_date(item.environment, per, business_date, item.project_id)
			count -= 1
		return {"code": 2000, "msg": "执行成功"}
	except Exception as e:
		return {"code": 5000, "msg": str(e)}
