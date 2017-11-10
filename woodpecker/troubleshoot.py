#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-11-10 21:10:43

# File Name: troubleshoot.py
# Description:

"""
import os,sys
reload(sys)
sys.setdefaultencoding('utf8')
import re

class CheckProcess:
    def __init__(self,name):
        self.name=name
        self.__loadPlugins(name)

    def __loadPlugins(self,name):
        checkPath=os.path.split(os.path.realpath(__file__))[0]
        check_list=[]
        if os.path.exists(checkPath+'/plugins/'+self.name):
            for filename in os.listdir(checkPath+'/plugins/'+self.name):
                if not filename.endswith('.py') or filename.startswith('_'):
                    continue
                try:
                    int(filename[0])
                except:
                    continue
                check_list.append(filename)
        else:
            print "[*] Plugins directory not in here!"
            print "[*] Done."
        new_check_list = sorted(check_list,key = lambda i:int(re.match(r'(\d+)',i).group()))
        for check_file in new_check_list:
            self.__runPlugins(check_file,name)

    def __runPlugins(self,filename,name):
        plugins_name=os.path.splitext(filename)[0]
        plugin=__import__('plugins.'+self.name+'.'+plugins_name,fromlist=[plugins_name])
        clazz=plugin.getPluginClass()
        print clazz
        clazz().getStatus()

def check():
    """
    """
    CheckProcess('app')


if __name__=="__main__":
    import sys, inspect
    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                          str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
        except Exception, e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
