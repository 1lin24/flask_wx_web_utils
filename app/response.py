from flask import jsonify

class Response(object):
    def __init__(self, rs_code, data={}):
        self.rs_code = rs_code
        self.data = data
        self.rs_msg = self.get_rs_msg(rs_code)

    '''
        错误码规则:
        200 正常
        
        其它错误码则以: -ABBCC的负数形式出现,如:-20101
        
        A: 表示错误级别,分为:1,系统级别 2,服务级别
        B: 表示错误对应的模块
        C: 表示具体错误代码

        本规则参考微博开放平台文档:http://open.weibo.com/wiki/Error_code
    '''
    def get_rs_msg(self, rs_code):
        rs_info = {
                    200: 'ok'
                    }

        msg = 'undefined rs_code'
        return rs_info.get(rs_code, msg)

    def json(self):
        return jsonify(self.__dict__)

