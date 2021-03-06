# -*- coding: UTF-8 -*-
"""
@auth:bxj
@date:2019-10-25 09:30
@describe:任买医美线下还款流水推送接口字段必填项校验
"""
import unittest
import json
import ddt
import sys
from common.common_func import Common
from common.open_excel import excel_table_byname
from config.configer import Config


@ddt.ddt
class OfflineRepay(unittest.TestCase):
	file = Config().get_item('File', 'rmkj_required_case_file')
	excel_data = excel_table_byname(file, 'offline_repay')

	def setUp(self):
		self.env = sys.argv[3]

	def tearDown(self):
		pass

	@ddt.data(*excel_data)
	def test_offline_repay(self, data):
		param = json.loads(data['param'])
		headers = json.loads(data['headers'])
		rep = Common.response(faceaddr=data['url'], headers=headers,
							  data=json.dumps(param, ensure_ascii=False), product='cloudloan',
							  environment=self.env)
		self.assertEqual(int(rep['resultCode']), data['resultCode'])


if __name__ == '__main__':
	unittest.main()
