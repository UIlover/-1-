import mokuai as m
import threading   #导入线程模块
import tkinter as tk   #导入tkinter的类模块命名tk
import time #导入时间模块
import hot_key  #导入热键模块
from PIL import Image, ImageTk #图片模块

##################### 全局变量 (声明放在住mian的文件里
window = tk.Tk()   #定义主窗口
UI_cl=["red","blue","cyan","orange","pink","lime","Silver","Gray"]
map_data=None
hk =hot_key.main()  #初始化热键


##################### 实例类
m.game_win_Re() #初始化窗口信息和地图ID
ren1=m.ren([0x75720,0x2638,0,0],
         [0x75720,0x2620,0,0],
         [0x75720,0x2644,0,0],
         [0x75720,0x262C,0,0],
         [],
         1)
ren2=m.ren([0x75720,0x263A,0,0],
         [0x75720,0x2622,0,0],
         [0x75720,0x2646,0,0],
         [0x75720,0x262E,0,0],
         [0x75720,0x4564,0,0],
         2)
ren3=m.ren([0x75720,0x263C,0,0],
         [0x75720,0x2624,0,0],
         [0x75720,0x2648,0,0],
         [0x75720,0x2630,0,0],
         [0x75720,0x4420,0,0],
         3)
guai1=m.guai([0x8110C,0,0,0],
           1)
guai2=m.guai([0x811D8,0,0,0],
           2)
guai3=m.guai([0x812A4,0,0,0],
           3)
guai4=m.guai([0x81370,0,0,0],
           4)
guai5=m.guai([0x8143C,0,0,0],
           5)
ren_list = [ren1,ren2,ren3]
guai_list = [guai1,guai2,guai3,guai4,guai5] #怪物列表
##################### 游戏数据读取进程
def Read_Property ():
    global map_data
    while(1):
        m.game_win_Re() #窗口信息和地图ID
        for i in range(len(ren_list)):
            ren_list[i].shuju_Update()
        for i in range(len(guai_list)):
            guai_list[i].shuju_Update()
        #print(m.Map_path)
        time.sleep(0.1)   #延迟100MS
thread_game_Re = threading.Thread(target=Read_Property)   #进程准备，必须放在进程函数后面
thread_game_Re.start()   #进程执行
##################### UI设置
window.overrideredirect(True)   #去掉边框
window.config(background =UI_cl[4]) # 设置窗口红色背景
window.attributes('-transparentcolor',UI_cl[4],'-topmost',True)   # 设置窗口透明，置于顶层
map_win= tk.Toplevel()
map_win.overrideredirect(True)
map_win.title("游戏地图")
map_win.geometry('1032x1028+200+100')
map_win.iconbitmap('bitbug_favicon.ico')
#map_label=tk.Label(map_win,width=1032,height=1028) #地图label组件
#map_label.pack()
map_win.state("withdrawn") #地图窗口隐藏
Map_HuaBan=tk.Canvas(map_win,
                     width=1032,height=1028,bg="pink",
                     highlightthickness=0)
Map_HuaBan.create_rectangle(0, 0, 160, 100, fill='')
Map_HuaBan.pack()
    #####################  Mpa 界面
def close_map():  #关闭地图
    map_win.state("withdrawn")
    openMap_bt.configure(text = "打开地图", command=back_map)
def back_map():   #再现地图
    map_win.deiconify()
    openMap_bt.configure(text = "关闭地图", command=close_map)
openMap_bt = tk.Button(window, text="打开地图", command=back_map,width=8, height=1,bg=UI_cl[3])
openMap_bt.place(relx=0.01)  #打开地图按钮

##################### 绑定鼠标地图事件
def Motion_coordinate(event): #返回给热键模块，方便后期执行
    hot_key.Motion_x=event.x
    hot_key.Motion_y=event.y
map_win.bind('<Motion>',Motion_coordinate)

##################### 热键提示
hk_tip = tk.Label(window,width=16,height=1,text="Alt+home 关闭程序",fg='blue',font=('微软雅黑',12))
hk_tip.place(relx=0.15)
#初始化UI属性
ren_UI={'Label':[],  
         'xueGB':[],
         'xuetiao':[],
         'moGB':[],
         'motiao':[]}
guai_UI={'Label':[],
         'xueGB':[],
         'xuetiao':[],
         'text':[]}
for key in ren_UI.keys():
        ren_UI[key]=ren_UI[key]+[None,None,None]
for key in guai_UI.keys():
       guai_UI[key]=guai_UI[key]+[None,None,None,None,None]
#先全部UI画出来，初始化
for i in range(len(ren_list)):
    ren_UI['Label'][i]=tk.Label (window,bg=UI_cl[7])
    ren_UI['Label'][i].place(relx=ren_list[i].ui_adjust,#当前角色UI修正
            height=60,
            relwidth=0.33,
            y=m.game_h) #总状态栏位置在游戏窗口
    ren_UI['xueGB'][i]=tk.Canvas(ren_UI['Label'][i],
                            bg=UI_cl[6],
                            width=200,
                            height=10,
                            highlightthickness=0)#角色的背景
    ren_UI['xueGB'][i].pack(side="top",pady='2px')
    ren_UI['xuetiao'][i]=ren_UI['xueGB'][i].create_rectangle(0, 0, 0, 10, fill=UI_cl[5])#角色血条,前面假self是实例变量
    ren_UI['moGB'][i]=tk.Canvas(ren_UI['Label'][i],
                         bg=UI_cl[6],
                         width=200,
                         height=10,
                         highlightthickness=0)#角色的背景
    ren_UI['moGB'][i].pack(side="top",pady='2px')
    ren_UI['motiao'][i]=ren_UI['moGB'][i].create_rectangle(0, 0, 30, 10, fill=UI_cl[1])
    text =tk.Label(ren_UI['Label'][i],width=4,height=1,text=ren_list[i].shuxing[6])  #顺序很重要，字在血上面
    text.pack(pady='2px',side="bottom")
for i in range(len(guai_list)):
    guai_UI['Label'][i]=tk.Label (window,bg=UI_cl[4])
    guai_UI['Label'][i].place(relx=guai_list[i].ui_adjust,#当前角色UI修正
                        relheight=0.1,
                        relwidth=0.2,
                        y=m.game_h*0.1) #总状态栏位置在游戏窗口
    guai_UI['xueGB'][i]=tk.Canvas(guai_UI['Label'][i],
                          bg=UI_cl[6],
                          width=100,
                          height=10,
                          highlightthickness=0)
    guai_UI['xueGB'][i].pack(side="bottom",pady='2px')
    guai_UI['xuetiao'][i]= guai_UI['xueGB'][i].create_rectangle(0, 0, 0, 10, fill=UI_cl[0])
    guai_UI['text'][i] =tk.Label(guai_UI['Label'][i],width=5,height=1,text=guai_list[i].shuxing[4])
    #guai_UI['text'][i] =tk.Label(guai_UI['Label'][i],width=12,height=1,text=guai_list[i].shuxing[4]+'  血:'+str(guai_list[i].shuxing[0]))
    guai_UI['text'][i].pack(pady='1',side="bottom")
##################### UI更新线程
#print("jiba%s" %m.game_x)
def Update_Ui():
    while(1):   
        window.geometry(m.game_win_Re())
        #判断角色或者怪物是否存活画UI
        for i in range(len(ren_list)):
            if(ren_list[i].shuxing[4]):
                ren_UI['Label'][i].place(relx=ren_list[i].ui_adjust,#当前角色UI修正
                                         height=60,
                                         relwidth=0.33,
                                         y=m.game_h) #总状态栏位置在游戏窗口
                ren_UI['xueGB'][i].coords(ren_UI['xuetiao'][i],
                                          0,0,200*ren_list[i].shuxing[7],
                                          10)
                ren_UI['moGB'][i].coords(ren_UI['motiao'][i],
                                         0,0,200*ren_list[i].shuxing[8],
                                         10)
            else:
                 ren_UI['Label'][i].place_forget()
        for i in range(len(guai_list)):
            if(guai_list[i].shuxing[2]):
                guai_UI['Label'][i].place(relx=guai_list[i].ui_adjust,#当前角色UI修正
                                          relheight=0.1,
                                          relwidth=0.2,
                                          y=m.game_h*0.1) #总状态栏位置在游戏窗口
                guai_UI['xueGB'][i].coords(guai_UI['xuetiao'][i],
                                          0,0,100*guai_list[i].shuxing[5],
                                          10)
            else:
                 guai_UI['Label'][i].place_forget()
        time.sleep(0.1)   #延迟100MS
thread_game_Re = threading.Thread(target=Update_Ui)   #进程准备，必须放在进程函数后面
thread_game_Re.start()   #进程执行
##################### 地图读取进程
def mapupdate():
    global map_data
    linshi=0
    mubiao=None
    dian=None
    while(1):
        m.GetGameMapId()
        if(m.map_id!=linshi):
            PngToDate = Image.open(m.Map_path)  #转换PNG图片
            mapDate = ImageTk.PhotoImage(PngToDate)
            Map_HuaBan.create_image(516,514,image=mapDate)  #地图输入到画板
        linshi=m.map_id
        Map_HuaBan.delete(mubiao)
        Map_HuaBan.delete(dian)
        mubiao=Map_HuaBan.create_rectangle(m.Map_x/2, m.Map_y/2, m.Map_x/2+160, m.Map_y/2+100, fill='',outline = 'blue',width=2)
        dian=Map_HuaBan.create_rectangle(m.Map_x/2+79, m.Map_y/2+49, m.Map_x/2+81, m.Map_y/2+51, fill='',outline = 'blue',width=2)
        #画矩形是四点定位
        #print(m.Map_path)
        time.sleep(0.1)   #延迟100MS
thread_game_Re = threading.Thread(target=mapupdate)   #进程准备，必须放在进程函数后面
thread_game_Re.start()   #进程执行
window.mainloop()   #循环刷新窗口
