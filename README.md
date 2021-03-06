<h1 align="center"><img src="./icon/32.png" height="21px" alt=""> Auto-Collect-Paper-Toolkit </h1>

<p align="center">
    <a href="https://github.com/linwhitehat/ACPT4dblp">
        <img alt="GitHub manifest version" src="https://img.shields.io/github/v/release/linwhitehat/ACPT4dblp?color=%23EA4AAA&label=Github&logo=github&logoColor=%23EA4AAA">
    </a>
</p>

ACPT can automatically obtain the paper address of the conference/journal in the dblp paper database, and automatically download the pdf file of the paper and the pdf file of the speech manuscript from the official conference address.

自动化收集论文工具箱，能够自动对可访问的会议或期刊官网中的收录论文进行下载，为科研工作者批量查找和下载大量论文提供便利，修改配置文件即可实现目标会议的指定年限论文集自动下载工作。

## Preview

![ACPT result](./img/ACPT.png "ACPT result")

## Install

1. Application Environment

    - Windows 10 x64
    - Python 3
    
2. Dependency

    - chrome browser
    - [chromedriver.exe](https://chromedriver.chromium.org/downloads)
    - dependency library
        - selenium (pip install selenium)
        
        - requests (pip install requests)
        
        - lxml (pip install lxml)
        
3. ACPT

    - Get the program
        - Use GitHub's cloning method to download the source code
        - Get the compressed package file (.zip) from the [release](https://github.com/linwhitehat/ACPT4dblp/releases)

## Usage

### config

    Please fill in the following content in the configuration file according to the actual situation.

    - basic
    
        - c_service_dir: chromedriver storage path
        - years: range of the year when the paper was obtained
        - dblp_url: link address of conference or journal in dblp
    
    - xpath
    
        - topic_path: focus of conference papers on the dblp_url page
        - paper_path: title of the conference paper in the dblp_url page
        - paper_link_path: paper on the dblp_url page points to the link address of the official website
    
    - file
    
        - paper_pdf_path: paper download link address on the conference website
        - ppt_pdf_path: PPT download link address of the paper presentation on the conference official website
    
    - file_option
    
        - paper_pdf_path: paper download link address on the conference website
        - ppt_pdf_path: PPT download link address of the paper presentation on the conference official website
    
    - save
    
        - file_path: local storage path of the paper and PPT
        
### run

    Please ensure that the config file and the ACPT.py file are in the same file directory.
    Then execute the ACPT program in the python3 environment until the program ends.
    
``` shell
    python3 ACPT.py
```

## Note

1. The default configuration and processing logic are designed according to the official website structure published by [USENIX](https://www.usenix.org/conferences). If you need the configuration of other journals or conference websites, there are two solutions.

    - Modify the logic yourself

    - [Submit](https://github.com/linwhitehat/ACPT4dblp/issues/new) the target conference or journal that needs to be crawled, and I will add it to the toolkit (requires free time)
    
2. The storage path is processed by layer 2 by default, such as the conference name (NSDI) under the F disk, and finally write F:/NSDI/ in the config file.

    - If you use a multi-layer path, please write the established path into the configuration file.
    
3. The version of chromedriver needs to be adapted to the current browser version.

    - View the current version of the Chrome browse, chrome://settings/help
    
    - Download the corresponding version of chromedriver, https://chromedriver.chromium.org/downloads.
    
    - If you are using Firefox browser, you can also download firefoxfdriver to replace chromedriver, please pay attention to the code adjustment at this time.
    
4. Problems.
     
     If your network environment is unable to access the resources on the target website, it will cause problems such as slow acquisition speed, abnormalities or errors.
     
    - Delay
    
    For example, the USENIX conference website will play a presentation video from the YouTube website, but this part of the resource is not accessible in China, so it will cause a waiting time of 2-3 minutes. Fortunately, this effect will not make the paper unavailable.
    
    - Error
    
    If you do not have access to the paper resources, you will not be able to get the complete paper.

## Guide

Waiting...

## Contributing
Feel free to dive in!
[Open new issue](https://github.com/linwhitehat/ACPT4dblp/issues/new) or submit PRs.

## License
[MIT](LICENSE) © linwhitehat
