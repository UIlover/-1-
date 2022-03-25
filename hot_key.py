
import win32con
import ctypes
import ctypes.wintypes
from threading import Thread,activeCount, enumerate
from time import sleep,time
import mokuai as m
import os
Motion_x=0
Motion_y=0
pid=pid = os.getpid()

class Hotkey(Thread):
  user32 = ctypes.windll.user32
  hkey_list = {}
  hkey_flags = {} #按下
  hkey_running = {} #启停
  _reg_list = {} #待注册热键信息
  
  def regiskey(self, hwnd=None, flagid=0, fnkey=win32con.MOD_ALT, vkey=win32con.VK_F9): # 注册热键，默认一个alt+F9
    return self.user32.RegisterHotKey(hwnd, flagid, fnkey, vkey)
  
  def get_reginfo(self):
    return self._reg_list
  
  def get_id(self,func):
    self_id = None
    for id in self.get_reginfo():
      if self.get_reginfo()[id]["func"] == func:
        self_id = id
        break
    if self_id:
      self.hkey_running[self_id] = True
    return self_id
  
  def get_running_state(self,self_id):
    if self.hkey_running.get(self_id):
      return self.hkey_running[self_id]
    else:
      return False
  
  def reg(self,key,func,args=None):
    id = int(str(round(time()*10))[-6:])
    fnkey = key[0]
    vkey = key[1]
    info = {
      "fnkey":fnkey,
      "vkey":vkey,
      "func":func,
      "args":args
    }
    self._reg_list[id] = info
    sleep(0.1)
    return id
  
  def fast_reg(self,id,key = (0,win32con.VK_HOME),func = lambda:print('热键注册开始')):
    if not self.regiskey(None, id, key[0], key[1]):
      print("热键注册失败")
      return None
    self.hkey_list[id] = func
    self.hkey_flags[id] = False
    return id
  
  def callback(self):
    def inner(self = self):
      for flag in self.hkey_flags:
        self.hkey_flags[flag] = False
  
      while True:
        for id, func in self.hkey_list.items():
          if self.hkey_flags[id]:
            args = self._reg_list[id]["args"]
            if args:
              thread_it(func,*args)
            else:
              thread_it(func)
            self.hkey_flags[id] = False
    return inner
  
  def run(self):
    for id in self._reg_list:
      reg_info = self._reg_list[id]
      fnkey = reg_info["fnkey"]
      vkey = reg_info["vkey"]
      func = reg_info["func"]
      self.fast_reg(id,(fnkey, vkey), func)
  
    fn = self.callback()
    thread_it(fn) # 启动监听热键按下线程
  
    try:
      msg = ctypes.wintypes.MSG()
      while True:
        if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
          if msg.message == win32con.WM_HOTKEY:
            if msg.wParam in self.hkey_list:
              self.hkey_flags[msg.wParam] = True
          self.user32.TranslateMessage(ctypes.byref(msg))
          self.user32.DispatchMessageA(ctypes.byref(msg))
    finally:
      for id in self.hkey_list:
        self.user32.UnregisterHotKey(None, id)
  
def thread_it(func, *args):
  t = Thread(target=func, args=args)
  t.setDaemon(True)
  t.start()
  
def jump():
    print('触发一次')
    try:
        os._exit(0)
    except Exception :
        print(u'第一种退出方式失败')
        os.popen('taskkill.exe /pid:'+str(pid))
def guai_xue_magic():
    print(u'改怪血一次')
    m.Write_GameMemory([0x8110C,0,0,0],1)
    m.Write_GameMemory([0x811D8,0,0,0],1)
    m.Write_GameMemory([0x812A4,0,0,0],1)
    m.Write_GameMemory([0x81370,0,0,0],1)
    m.Write_GameMemory([0x8143C,0,0,0],1)
def chuansong():
      
    print(u'鼠标：',Motion_x,Motion_y)
    mubiao_x = Motion_x*2-160
    mubiao_y = Motion_y*2-100
    m.Write_GameMemory([0x75720,0x43F0,0,0],mubiao_x)
    m.Write_GameMemory([0x75720,0x43F2,0,0],mubiao_y)
def main():
  hotkey = Hotkey()
  hotkey.reg(key = (win32con.MOD_ALT,win32con.VK_HOME),func=jump) #alt home键 开始
  hotkey.reg(key = (win32con.MOD_ALT,win32con.VK_F6),func=guai_xue_magic) #alt F6 改怪血
  hotkey.reg(key = (win32con.MOD_ALT,win32con.VK_F7),func=chuansong) #alt F6 改怪血
  hotkey.start() #启动热键主线程
if __name__ == '__main__':
  main()