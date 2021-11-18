# -*- coding: UTF-8 -*-
import re

print(re.search(r'ods\.(\w)+', 'xxx ods. ods  ods.x_abx_234  ods._yyyx23__ 2 dd od sss od.s ', re.I | re.S))


# print(re.findall(r'ods\.(\w)+', 'xxx ods. ods  ods.x_abx_234  ods._yyyx23__ 2 dd od sss od.s ', re.I | re.S))
#
# ma = re.match(r'ods\.(\w)+', 'xxx ods. ods  ods.x_abx_234  ods._yyyx23__ 2 dd od sss od.s ', re.I | re.S)
# print(ma)
#
# # print(re.search(r'ods\.(\w)+', 'xxx ods. ods  ods.x_abx_234  ods._yyyx23__ 2 dd od sss od.s ', re.I | re.S))
#
# print(re.search(r'ods\.re+(\w)', 'xxx ods. ods  ods.x_abx_234  2 dd od sss od.s ', re.I | re.S))
