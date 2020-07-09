#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 16:14
# @Author  : turn1tup
# @FileName: charset_test.py
import codecs
import urllib.parse
from enum import Enum

class DataEncoder():
    URL_ENCODE = urllib.parse.quote

class Charset:
    bom_map = {
        'utf16':codecs.BOM_UTF16,
        'u16':codecs.BOM_UTF16,
        'u16':codecs.BOM_UTF16,
        'UTF-8-SIG':codecs.BOM_UTF8,
        'utf16be':codecs.BOM_UTF16_BE,
        'utf16le':codecs.BOM_UTF16_LE,
        'utf8':codecs.BOM_UTF8,
        'utf32':codecs.BOM_UTF32,
        'utf32be':codecs.BOM_UTF32_BE,
        'utf32le':codecs.BOM_UTF32_LE,
    }
    '''
    @staticmethod
    def get_useful_charset(data_file="useful_charset.txt"):
        useful_c = set()
        with open(data_file, encoding="utf-8") as fr:
            for line in fr:
                ls = line.split("\t")
                if ls[3] != "useful":
                    continue
                useful_c.add(ls[0].strip().upper())
                ls2 = ls[1].split(",")
                for c in ls2:
                    useful_c.add(c.strip().upper())
        useful_c.remove("")
        return list(useful_c)
    '''
    @staticmethod
    def encode(s,charset="utf-8"):
        if not isinstance(s,str):
            raise Exception

        charset_f = charset.lower().replace("-","")
        if charset_f =="utf7":
            raise Exception("not implement")

        else:
            try:
                s = s.encode(encoding=charset)
            except UnicodeEncodeError:
                raise UnicodeEncodeError
            return s

    @staticmethod
    def set_spe_charset(
            s,
            reserved_chars="&=",
            charset="ibm037",
            resulst_data_format_func=DataEncoder.URL_ENCODE,
            remove_bom = True,
    ):
        '''

        :param s:
        :param reserved_chars:不被改变的保留字符，默认 &=
        :param charset:
        :param resulst_data_format_func: 结果输出使用的编码，默认 DataEncodeType.URL_ENCODE
        :param remove_bom: 默认删除 bom 标识 ，如UTF16BE 字符BOM标识为 FE FF
        :return:
        '''
        if not isinstance(s,str):
            raise Exception
        s_result = ""
        char_pos_list = [len(s)]
        pos = 0
        while len(char_pos_list)>0:

            for char in reserved_chars:
                char_pos = s.find(char,pos)
                if char_pos>-1:
                    char_pos_list.append(char_pos)
            char_pos_list = list(set(char_pos_list))
            char_pos_list.sort()
            if len(char_pos_list)==0:
                break
            special_char_pos = char_pos_list.pop(0)

            str_part = s[pos:special_char_pos]
            str_part = Charset.set_str_charset(str_part,charset=charset,remove_bom=remove_bom,resulst_data_format_func=resulst_data_format_func)

            s_result+= str_part
            if special_char_pos+1<=len(s):
                s_result+= s[special_char_pos]

            pos = special_char_pos+1
        return s_result


    @staticmethod
    def set_str_charset(s,
                        charset="ibm037",
                        remove_bom=True,
                        resulst_data_format_func=None
                        ):
        '''
        :param s: 需要设置字符集的字符串
        :param charset: 字符集
        :return:
        '''
        if not isinstance(s,str):
            raise Exception

        try:
            s = s.encode(encoding=charset)
        except UnicodeEncodeError:
            raise UnicodeEncodeError
        if remove_bom==True:
            s= Charset.remove_bom(s,charset)
        else:
            s = Charset.add_bom(s, charset)
        if resulst_data_format_func:
            s = resulst_data_format_func(s)
        return s

    @staticmethod
    def remove_bom(b,charset):
        if not isinstance(b,bytes):
            raise Exception
        charset = charset.replace("-","").replace("_","").strip().replace(" ","").lower()

        for k,v in Charset.bom_map.items():
            if charset==k and b.startswith(v):
                l = len(v)
                b = b[l:]
        return b
    @staticmethod
    def add_bom(b,charset):
        if not isinstance(b,bytes):
            raise Exception
        charset = charset.replace("-","").replace("_","").strip().replace(" ","").lower()

        for k,v in Charset.bom_map.items():
            if charset==k and not b.startswith(v):
                l = len(v)
                b = v+b
        return b


if __name__ == '__main__':
    charset= "utf-16be"
    data = '''<?xml version="1.0" encoding="{charset}"?>
<jsp:root xmlns:jsp="http://java.sun.com/JSP/Page"
  version="1.2">
<jsp:directive.page contentType="text/html"/>
<jsp:declaration>
</jsp:declaration>
<jsp:scriptlet>
out.write("I'm turn1tup!");
</jsp:scriptlet>
<jsp:text>
</jsp:text>
</jsp:root>
'''.format(charset=charset)
    print((Charset.set_str_charset(data, charset=charset,remove_bom=True,resulst_data_format_func=DataEncoder.URL_ENCODE)))
