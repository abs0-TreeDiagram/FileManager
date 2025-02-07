# MIT License
#
# Copyright (c) 2025 Cai Jifeng
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time
from pathlib import Path
from datetime import datetime
import os
import shutil
import json

newFlieLocation=Path('./newFiles')

I=''#I for input
W=''#W for warning

#关键字查找
def search(lst, keyword):
    results = []
    for item in lst:
        if keyword.lower() in str(item).lower():
            results.append(item)
    return results

#当前位置模块
currentLocation=[]
def location(Type=None,content=''):
    if Type is None:#要输出当前位置，直接调用location()即可
        echo=''
        for i in currentLocation:
            echo+=i
        print('当前位置：',echo)
    elif Type==1:#添加位置
        if not len(currentLocation)==0:
            currentLocation.append('>')
        currentLocation.append(content)
    elif Type==2:#删除位置
        del currentLocation[len(currentLocation)-1]
        if not len(currentLocation)==0:
            del currentLocation[len(currentLocation)-1]

#输出模块：l为包含分行显示内容的列表，f为底部提示输入的字符串
def echo(l,f='',num=1):
    global I,W
    if l==[]:
        l=['','','','','','','','']
    j=8-len(l)%8
    if j==8:
        j=0
    for i in range (0,j):
        l.append('')
    pageCount=len(l)//8
    currentPage=1
    c=True
    while c==True:
        print('=============================')
        print(time.asctime())
        location()
        print('-----------------------------------------------------------------')
        for i in range ((currentPage-1)*8,currentPage*8):
            if num==0:
                print(l[i])
            else:
                print(f'{i+1}.{l[i]}')
        print('-----------------------------------------------------------------')
        print(f'第{currentPage}页，共{pageCount}页')
        print('-----------------------------------------------------------------')
        print('操作提示：')
        print('z-上一页 x-下一页 #{页码}-跳转页')
        print(f)
        print('警告：')
        print(W)
        W='无'
        print('-----------------------------------------------------------------')
        I=input()
        if not I=='':
            if I=='z':
                currentPage-=1
                if currentPage==0:
                    currentPage=1
                    W='页码超出范围'
            elif I=='x':
                currentPage+=1
                if currentPage==pageCount+1:
                    currentpage=pageCount
                    W='页码超出范围'
            elif I[0]=='#':
                try:
                    currentPage=int(I[1:])
                except ValueError:
                    c=False
                else:
                    if not currentPage in range (1,pageCount+1):
                        currentPage=1
                        W='页码超出范围'
            else:
                c=False
        else:
            c=False
    if l==['','','','','','','','']:
        l=[]
    for i in range (0,j):
        del l[len(l)-1]


def check_and_create_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        # 如果不存在，则创建文件夹
        os.makedirs(folder_path)

#导入并归档模块
newFileNames=[]
def Import():
    global newFileNames,newFlieLocation,W
    newFileNames=[f.name for f in newFlieLocation.iterdir() if f.is_file()]
    
    echo(newFileNames,'待归档文件检索完成。回车-归档 0-取消')
    print(newFileNames,'hj')
    if not I==0:
        #创建月份文件夹
        ym=str((datetime.now()).year)+'-'+str((datetime.now()).month)
        oldFileNames=[file.name for file in Path('./library').rglob('*') if file.is_file()]
        check_and_create_folder(f'./library/{ym}')
        
        #录入时间戳记录和文件移动
        newFileTimestamp={}
        for i in range (0,len(newFileNames)):
            #重名时在文件名前加上时间戳
            if newFileNames[i] in oldFileNames:
                j=str(time.time())
                l=''
                for k in j:
                    if not k=='.':
                        l+=k
                    else:
                        l+='_'
                j=l
                os.rename(f'newFiles/{newFileNames[i]}',f'newFiles/{j}{newFileNames[i]}')
                newFileNames[i]=j+newFileNames[i]
            #文件信息记录
            newFileTimestamp[newFileNames[i]]=time.time()#录入时间戳
            #移动文件
            shutil.move(f'newFiles/{newFileNames[i]}',f'library/{ym}')

        #文件时间戳信息写入
        with open('timestamp.json','r') as json_file:
            loaded_data = json.load(json_file)
        loaded_data.update(newFileTimestamp)
        with open('timestamp.json', 'w') as json_file:
            json.dump(loaded_data, json_file)

        W=f'{len(newFileNames)}个文件已归档'
    else:
        W='归档操作已取消'

#数据获取
def timestampList():
    with open('timestamp.json','r') as json_file:
        loaded_data = json.load(json_file)
    return loaded_data

def tagList():
    with open('tag.json','r') as json_file:
        loaded_data = json.load(json_file)
    return loaded_data

#tag编辑
def tagUpdate(t,l):
    with open('tag.json','r') as json_file:
        loaded_data = json.load(json_file)
    if t in loaded_data:
        loaded_data[t]+=l
    else:
        loaded_data[t]=l
    with open('tag.json', 'w') as json_file:
        json.dump(loaded_data, json_file)
            
def tagging():
    global I,W
    location(1,'标签选定/新建')
    
    I=''
    j=0
    while I=='':
        if j==1:
            W='标签名称不能为空'
        echo([],'输入标签名称')
        if I=='':
            j=1
        elif I[0]==' ':
            W='标签名不能以空格开头'
    location(2)
    
    tagName=I
    #检查tag是否已用
    with open('tag.json','r') as json_file:
        loaded_data = json.load(json_file)
    if tagName in loaded_data:
        selected=loaded_data[tagName]
        W='你正在为已有标签指定文件'
    else:
        selected=[]
        W='你正在为一个新标签指定文件'
    
    filelist=timestampList()
    filelist=sorted(filelist, key=filelist.get)
    echol=list(filelist)
    for i in selected:
        echol[echol.index(i)]+='√'
        
    location(1,'文件选定')
    i=1
    while i==1:
        echo(echol,'{序号}-选定文件 {回车}-确认')
        if I=='':
            i=0
        else:
            try:
                I=int(I)
            except:
                W='输入错误'
            else:
                if I in range(1,len(filelist)+1):
                    if filelist[I-1] in selected:
                        W='勿重复选择'
                    else:
                        selected.append(filelist[I-1])
                        W=f'已选择{filelist[I-1]}'
                        echol[I-1]+='√'
                else:
                    W='输入超出范围'
    location(2)
    tagUpdate(tagName,selected)
    W='标签指定完成'
    
def find_file(filename, search_path):
    """遍历给定路径，寻找特定文件"""
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def editTag():
    global I,W
    with open('tag.json', 'r') as json_file:
        loaded_data = json.load(json_file)
    taglist=list(loaded_data)
    i=1
    echol=taglist
    j=1
    while i==1:
        location(1,'选择标签')
        echo(echol,'{序号}-选择标签 s-搜索标签 {回车}-返回上一级')
        try:
            I=int(I)
            selected=echol[I-1]
        except:
            if I=='s':
                echo(echol,'输入关键词')
                echol=search(echol,I)
            else:
                i=0
                j=0
        else:
            i=0
    location(2)
    if not j==0:
        location(1,f'标签：{selected}')
        echo(['已选择的标签：',selected],'1-编辑标签名称 2-查看包含文件 del-删除标签（尚未实装） 回车-取消操作并退出',0)
        if I=='1':
            i=1
            while i==1:
                echo(['已选择的标签：',selected],'输入新标签名称')
                checklist=taglist
                pop=checklist.pop(checklist.index(selected))
                if I=='':
                    W='标签名不能为空'
                elif I[0]==' ':
                    W='标签名不能以空格开头'
                elif selected in checklist:
                    W='标签名不得与其他标签名相同'
                else:
                    with open('tag.json','r') as json_file:
                        loaded_data = json.load(json_file)
                    loaded_data[I]=loaded_data.pop(selected)
                    with open('tag.json', 'w') as json_file:
                        json.dump(loaded_data, json_file)
                    W='标签修改成功'
                    i=0
        elif I=='2':
            location(1,f'标签为{selected}的文件')
            with open('tag.json','r') as json_file:
                loaded_data = json.load(json_file)
            j=1
            while j==1:
                echo(loaded_data[selected],'{序号}-打开文件 回车-退出')
                try:
                    I=int(I)
                    current_directory = os.getcwd()  # 获取当前工作目录
                    found_file_path = find_file(loaded_data[selected][I-1], current_directory)
                    os.startfile(found_file_path)
                except:
                    j=0
            location(2)
        location(2)
def tag():
    global W
    i=1
    while i==1:
        echo(['为文件指定标签','标签编辑和查看'],'{序号}-进入 {回车}-返回上一级')
    
        if I=='1':
            location(1,'标签指定')
            tagging()
            location(2)
        elif I=='2':
            location(1,'标签编辑和查看')
            editTag()
            location(2)

        else:
            i=0

#文件查找
def fileSearch():
    global I,W
    filelist=list(timestampList())
    #处理文件列表，以显示文件创建时间
    echol=filelist.copy()
    creationTime=[]
    for i in range(0,len(echol)):
        filepath=find_file(echol[i], './library')
        creationTime.append(os.path.getctime(filepath))
    combined = zip(creationTime,echol)
    sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # 解压缩排序后的结果
    sorted_list1, sorted_list2 = zip(*sorted_combined)

    # 将结果转换回列表
    creationTime = list(sorted_list1)
    echol = list(sorted_list2)
    filelist=echol.copy()
    for i in range(0,len(creationTime)):
        readable_time = time.ctime(creationTime[i])
        creationTime[i]=readable_time
    for i in range(0,len(echol)):
        echol[i]=creationTime[i]+'  '+echol[i]
    i=1
    taglist=tagList()
    while i==1:
        echo(echol,'{标签名}-用标签在结果中搜索  {空格}{序号}-文件详细信息及操作  {回车}-退出')
        if I=='':
            i=0
        elif I[0]==' ':
            I=I[1:]
            try:
                I=int(I)
                filename=filelist[I-1]
            except:
                W='序号输入错误'
                j=0
            else:
                j=1
            if j==1:
                filepath=find_file(filename, './library')
                ct=os.path.getctime(filepath)
                ct = time.ctime(ct)
                it=timestampList()
                it=it[filename]
                it=time.ctime(it)
                tags=''
                
                for key,value in taglist.items():
                    if filename in value:
                        tags+='#'+key+' '
            location(1,'文件详情页')
            while j==1:
                echo([filename,f'创建日期：{ct}',f'录入日期：{it}',f'相关标签：{tags}'],'{空格}-打开 {回车}-退出',0)
                if I==' ':
                    current_directory = os.getcwd()  # 获取当前工作目录
                    found_file_path = find_file(filename, current_directory)
                    os.startfile(found_file_path)
                else:
                    j=0
            location(2)
        else:
            if I in taglist:
                new_filelist=[]
                new_echol=[]
                for k in range (0,len(echol)):
                    if filelist[k] in taglist[I]:
                        new_filelist.append(filelist[k])
                        new_echol.append(echol[k])
                filelist=new_filelist
                echol=new_echol
                W=f'成功检索与#{I}相关的文件'
            else:
                W='标签输入错误'
#主循环
main=['导入并归档','标签操作','文件查找','','','','','关于本程序']
c=1#控制循环
location(1,'首页')
while c==1:
    echo(main,'输入序号进入相应模块，0-退出')
    
    if I=='1':
        location(1,'文件导入')
        Import()
        location(2)
    elif I=='2':
        location(1,'标签操作')
        tag()
        location(2)

    elif I=='3':
        location(1,'文件查找')
        fileSearch()
        location(2)
    elif I=='8':
        location(1,'关于')
        echo(['FileManager 文件管理工具 v1.1.0_beta',
              'Copyright © 2025 蔡继丰',
              '版权所有',
              '本项目遵循MIT许可协议',
              'This project is licensed under the MIT License.',
              '本程序允许任意复制、传播和修改，但需保留原署名和版权声明'],'{空格}-查看许可协议 {回车}-退出',0)
        if I==' ':
            echo(['MIT License',
                  'Copyright (c) 2025 Cai Jifeng',
                  'Permission is hereby granted, free of charge, to any person obtaining a copy',
                  'of this software and associated documentation files (the "Software"), to deal',
                  'in the Software without restriction, including without limitation the rights',
                  'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell',
                  'copies of the Software, and to permit persons to whom the Software is',
                  'furnished to do so, subject to the following conditions:',
                  '',
                  'The above copyright notice and this permission notice shall be included in all',
                  'copies or substantial portions of the Software.',
                  '',
                  'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR',
                  'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,',
                  'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE',
                  'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER',
                  'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,',
                  'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE',
                  'SOFTWARE.'],'{回车}-退出',0)
        location(2)
        

    elif I=='0':
        c=0
        
    
            
    
            
        
        
    
    
