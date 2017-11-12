#coding:utf-8
import _si

class AppProcess:
    def __output(self,msg,status):
        """
        1 --- OK
        0 --- ERR
        """
        status = int(status)
        if status:
            print "%s-----------\033[1;37;42m%s\033[0m" % (format(msg,"<15"),"OK")
        else:
            print "%s***********\033[1;37;41m%s\033[0m" % (format(msg,"<15"),"ERROR")
    def start(self):
        print "\n[mount point]"
        mounts = _si.Server.mounts(True)
        for mount in mounts:
            if float(mount["used_rate"]) > 80.0:
                self.__output(mount["path"],0)
            else:
                self.__output(mount["path"],1)
        
        meminfo = _si.Server.meminfo()
        print "\n[memory %s%%]" % meminfo['mem_used_rate_reality']
        if float(meminfo['mem_used_rate_reality']) > 80.0:
            self.__output("memory",0)
        else:
            self.__output("memory",1)

    def getStatus(self):
        self.start()
def getPluginClass():
    return AppProcess

if __name__ == '__main__':
    test=AppProcess()
    test.getStatus()
