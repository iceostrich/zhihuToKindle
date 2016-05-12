import urllib.request
import re,os
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MyMail:
    def __init__(self, posthost, user, password, postfix):
        self.posthost = posthost
        self.user = user
        self.password = password
        self.postfix = postfix
        self.msg = MIMEMultipart()

    def mailContent(self, sub, mailText, attach_path, attach_file):
        self.msg['Subject'] = sub
        self.msg.attach(MIMEText(mailText))
        att = MIMEText(open(attach_path + attach_file, 'rb').read(), 'base64', 'gb2312')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment;filename=' + attach_file
        self.msg.attach(att)

    def sendmail(self, mailto_list=None):
        if mailto_list is None:
            mailto_list = []
        self.msg['From'] = self.user + "<" + self.user + "@" + self.postfix + ">"
        self.msg['To'] = ";".join(mailto_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.posthost)  # 连接服务器
            server.login(self.user, self.password)  # 登录操作
            server.sendmail(self.msg['from'], mailto_list, self.msg.as_string())
            server.close()
            return True
        except Exception as e:
            print(e)
            return False


def save2file(filename, content):
    # 保存为电子书文件
    filename += ".txt"
    f = open(filename, 'a')
    f.write(content)
    f.close()


def getAnswer(answerID):
    host = "http://www.zhihu.com/question/"
    url = host + answerID
    print(url)
    resp = urllib.request.urlopen(url).read()
    bs = BeautifulSoup(resp, "html.parser")
    title = bs.title
    # 获取的标题
    filename_old = title.string.strip()
    print(filename_old)
    filename = re.sub('[\/:*?"<>|]', '-', filename_old)  # 用来保存内容的文件名，因为文件名不能有一些特殊符号，所以使用正则表达式过滤掉

    save2file(filename, title.string)
    detail = bs.find("div", class_="zm-editable-content")
    save2file(filename, "\n\n\n\n-----------------------Question Detail--------------------------\n\n")
    # 获取问题的补充内容
    for i in detail.strings:
        save2file(filename, i)

    answer = bs.find_all("div", class_="zm-editable-content clearfix")
    k = 0
    index = 0
    for each_answer in answer:

        save2file(filename, "\n-------------------------answer %s via  -------------------------\n" % k)

        for a in each_answer.strings:
            # 循环获取每一个答案的内容，然后保存到文件中
            save2file(filename, a)
        k += 1
        index += 1
    return os.getcwd() + '\\', filename + '.txt'


if __name__ == "__main__":
    attach_path, attach_file = getAnswer('46696983')

    mymail = MyMail("smtp.wo.cn", "15693100995", "751119", "wo.cn")
    mymail.mailContent('convert', attach_file, attach_path, attach_file)
    if mymail.sendmail(['961313680@qq.com']):
        print('Done!')
    else:
        print('False!')

    print(mymail.user)