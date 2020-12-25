#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/11/6 20:24
# @Author  : lin
# @FileName: collect_paper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os,time,requests
from lxml import etree

def Read_config():
    configs = {}

    config_file = open('config','r')
    config_data = config_file.read()
    config_file.close()

    configs_list = config_data.split('\n\n')
    for data in configs_list:
        config_item = data.split('\n')
        config_length = len(config_item)
        name = config_item[0].split('[')[1].split(']')[0]
        for i in range(1,config_length):
            item_data = config_item[i].split(' = ')[1]
            if 'year' in config_item[i]:
                time_list = item_data.split('[')[1].split(']')[0].split('-')
                if time_list[0] == time_list[1]:
                    item_data = [time_list[0]]
                else:
                    item_data = []
                    time_length = int(time_list[1]) - int(time_list[0])
                    for j in range(time_length+1):
                        item_data.append(str(int(time_list[0]) + j))
            if name not in configs:
                configs[name] = []
                configs[name].append(item_data)
            else:
                configs[name].append(item_data)
    
    return configs

def get_html(url,type,configs):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    }
    c_service = Service(configs['basic'][0])
    c_service.command_line_args()
    options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2,
             "profile.managed_default_content_settings.stylesheet": 2,
             "profile.managed_default_content_settings.flash": 2}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--headless')

    c_service.start()
    brower = webdriver.Chrome(options=options)
    if type == 'paper':
        try:
            brower.get(url)
            html_source = brower.page_source
            html = etree.HTML(html_source)
            brower.quit()
            c_service.stop()
            return html
        except Exception as e:
            print("error %s:\ncan't visit %s"%(e,url))
            brower.get(url)
            html_source = brower.page_source
            html = etree.HTML(html_source)
            brower.quit()
            c_service.stop()
            return html
    else:
        brower.get(url)
        html_source = brower.page_source
        html = etree.HTML(html_source)
        brower.quit()
        c_service.stop()
        return html

def get_pdf(html,year,configs):
    topic_list = html.xpath(configs['xpath'][0])
    paper_list = html.xpath(configs['xpath'][1])
    paper_links = html.xpath(configs['xpath'][2])
    error_paper = []

    for i in range(1, len(paper_list)):
        append_num = 0
        presentation_url = paper_links[i]
        paper_html = get_html(presentation_url,type='paper',configs=configs)
        paper_pdf = paper_html.xpath(configs['file'][0])
        if paper_pdf == []:
            paper_pdf = paper_html.xpath(configs['file_option'][0])
        ppt_pdf = paper_html.xpath(configs['file'][1])
        if ppt_pdf == []:
            ppt_pdf = paper_html.xpath(configs['file_option'][1])

        if paper_pdf == [] and ppt_pdf == []:
            print("collect %s error"%paper_list[i])
            error_paper.append(i)
        elif ppt_pdf != []:
            if len(paper_pdf) > 1:                                                                   
                print(paper_list[i + append_num]," -> ",paper_pdf[1]," -> ppt: ",ppt_pdf[0])
                write_pdf(paper_pdf[1], paper_list[i + append_num], year, 'paper',i,configs)
                write_pdf(ppt_pdf[0], paper_list[i + append_num], year, 'ppt',i,configs)
            else:
                print(paper_list[i + append_num], " -> ", paper_pdf[0], " -> ppt: ", ppt_pdf[0])
                write_pdf(paper_pdf[0], paper_list[i + append_num], year, 'paper',i,configs)
                write_pdf(ppt_pdf[0], paper_list[i + append_num], year, 'ppt',i,configs)
        else:
            if len(paper_pdf) > 1:
                print(paper_list[i + append_num], " -> ", paper_pdf[1], " without ppt")
                write_pdf(paper_pdf[1], paper_list[i + append_num], year, 'paper',i,configs)
            else:
                print(paper_list[i + append_num], " -> ", paper_pdf[0], " without ppt")
                write_pdf(paper_pdf[0], paper_list[i + append_num], year, 'paper',i,configs)

        time.sleep(3)
    if error_paper != []:
        print("error paper indexes: \n",error_paper)

def write_pdf(url,title,year,type,num,configs):
    headers = {
        'Connection': 'close',
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }
    response = ''
    while response == '':
        try:
            response = requests.get(url, verify =False, headers=headers, timeout=(5,10))
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
            
    file_path = configs['save'][0] + year + '/'
    if not os.path.exists(configs['save'][0]):
        os.mkdir(configs['save'][0])
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        print("create dir %s successfully."%file_path)
    if type == 'ppt':
        PDF_path = file_path + '{0}.{1}'.format(str(num) + "_" + title.replace(':', '').replace('?', '').replace('/','-') + "_ppt", 'pdf')
    else:
        PDF_path = file_path + '{0}.{1}'.format(str(num) + "_"  + title.replace(':', '').replace('?', '').replace('/','-'), 'pdf')
    if not os.path.exists(PDF_path):
        with open(PDF_path, 'wb') as f:
            print('capturing：' + title)
            f.write(response.content)
            f.close()
    else:
        print('already downloaded: ' + title)

if __name__ == '__main__':
    configs = Read_config()
    year = configs['basic'][1]
    for i in range(0,len(year)):
        url = configs['basic'][2]+year[i]+'.html'
        html = get_html(url,type='dblp',configs=configs)
        get_pdf(html,year[i],configs)
        print(year[i]," year completed.")
