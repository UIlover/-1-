import Memory64
import win32gui
import os
from tkinter import messagebox
map_id=0
Map_path=''
Map_x=0
Map_y=0
jubing =win32gui.FindWindow("SDL_app","Pal")#获取句柄
if(jubing<=0):
    messagebox.showinfo("提示","没找到游戏")
    try:
        os._exit(0)
    except Exception :
        print(u'退出失败')
game_pid = Memory64.FindWindowPid("SDL_app","Pal")   #读取类名“SDL_app”，窗口名为“Pal”的game_pid
addr = Memory64.SetupProcess(game_pid)   #设置进程，名为“addr（地址）”
modlue =addr.GetBaseAddr64("sdlpal.exe")   #获取名sdlpal.exe”的模块基址为modlue
############################################## 读取内存轮子 ###########################################
def Read_GameMemory(add=[]):
    linshi=[modlue]+add
    linshi = [i for i in linshi if i != 0]#Python 删除列表None值
    lengs =len(linshi)
    linshicun = modlue   #临时数据linshicun
    i=0
    while i < lengs-1:#判断读取内存次数
        if i== lengs-2:#判断取的字节数
            wei=2
        else:
            wei=4
        linshicun= addr.ReadMemory64(linshicun+linshi[i+1],wei)
        i+=1
    return linshicun   #返回结果
############################################## 写入内存轮子 ###########################################
def Write_GameMemory(add=[],var=1):
    linshi=[modlue]+add
    linshi = [i for i in linshi if i != 0]#Python 删除列表None值
    lengs =len(linshi)
    linshicun = modlue   #临时数据linshicun
    i=0
    while i < lengs-2:#判断读取内存次数
        linshicun= addr.ReadMemory64(linshicun+linshi[i+1])
        i+=1
    addr.WriteMemory64(linshicun+linshi[i+1],var,2)
############################################## 窗口信息读取 ###########################################
def game_win_Re():
    global game_x,game_y,game_w,game_h
    rect = win32gui.GetWindowRect(jubing)
    game_x = rect[0]   #游戏窗口左边
    game_y = rect[1]   #游戏窗口上边
    game_w = rect[2] - game_x   #游戏窗口宽
    game_h = rect[3] - game_y   #游戏窗口高
    return str(game_w)+'x'+str(int(game_h+80))+"+"+str(game_x)+"+"+str(game_y)
############################################## 地图信息读取 ###########################################
def GetGameMapId():
    global map_id,Map_path,Map_x,Map_y
    map_id = Read_GameMemory([0x75748,0x4,0x10004,0])# 地图ID暂时不用
    Map_path = os.getcwd()+"\\Map\\mini\\"+str(map_id)+".png"
    Map_x=Read_GameMemory([0x75720,0x43F0,0,0])
    Map_y=Read_GameMemory([0x75720,0x43F2,0,0])
############################################## 人的类 ###########################################
class ren():#人模块
    #实例化的时候运行一次==易语言XXX被创建时运行，只是用来创建一些必要的变量(适合写一次的东西)
    def __init__(self,
                 xue_16=[0,0,0,0],
                 xue_top_16=[0,0,0,0],
                 mo_16=[0,0,0,0],
                 mo_top_16=[0,0,0,0],
                 State_16=[0,0,0,0],
                 jueseid=1):
        self.shuxing_16=[xue_16,#16地址打组
                         xue_top_16,
                         mo_16,
                         mo_top_16,
                         State_16]
        self.shuxing=[0, #xue #角色属性初始化
                      0, #xueTop
                      0, #mo
                      0, #moTop
                      False, #State
                      jueseid, #id
                      "角色" +str(jueseid), #name
                      0,  #血比例
                      0]  #魔比例
        self.ui_adjust=(jueseid-1)*0.333 #UI修正
    #更新状态
    def shuju_Update(self):
        if (self.shuxing[5] !=1):#判断是不是主角1
            #不是主角1在判断是否存活
            if (self.shuxing[5] == Read_GameMemory(self.shuxing_16[4])):
                self.shuxing[4]=True
            else:self.shuxing[4]=False #如果不是真一定要改写为假，因为初始化的假不会在赋值
        else:
            self.shuxing[4]=True
        if(self.shuxing[4]):#如果存活，开始读取数据
            for i in range(4) :#for循环4次
                self.shuxing[i]=Read_GameMemory(self.shuxing_16[i])
            if(self.shuxing[1]>0):
                self.shuxing[7]=self.shuxing[0]/self.shuxing[1] #血比例
            if(self.shuxing[3]>0):
                self.shuxing[8]= self.shuxing[2]/self.shuxing[3] #魔比例
class guai():#怪物类还是不能继承人类怪物血上限没有数据
    #怪物函数入口重载
    def __init__(self,
                 xue_16=[0,0,0,0],
                 jueseid=1):
        self.shuxing_16=[xue_16]#16地址打组
        self.shuxing=[0, #xue #角色属性初始化
                      0, #xueTop
                      False, #State
                      jueseid, #id
                      "怪物" +str(jueseid), #name
                      0]  #血比例
        self.ui_adjust=(jueseid-1)*0.2 #UI修正
    def shuju_Update(self):
        self.shuxing[0]=Read_GameMemory( self.shuxing_16[0])
        if(0<self.shuxing[0]<65000): #判断是否存活
            if(self.shuxing[0]>=self.shuxing[1]):#判断是否大于血值
                self.shuxing[1]=self.shuxing[0]  #赋值上限
            self.shuxing[2]=True
        else:
            self.shuxing[2]=False
        if(self.shuxing[1]>0):
            self.shuxing[5]=self.shuxing[0]/self.shuxing[1]#属性列表最后添加血比例
                