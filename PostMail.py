class Email(object):
    """
    # smtp服务器以及相关配置信息
    smtp_server = 'smtp.163.com'
    from_addr = 'XXXX@163.com'
    password = 'XXXXXX'   # 网易授权码,非邮箱登入密码.
    to_addr = 'XXXX@XXXX.cn'    # 接收邮箱
    type = 'html'               发送html格式(html格式发送邮件,比较容易被当做垃圾邮件处理)的邮件内容,还可以选择为"plain",纯文本格式
    title = '使用smtp库发送'     # 邮件标题
    content = '''               # html格式的邮件内容
        <html>
            <body>
                <h1>附件是相关的IPv6材料</h1>
                <p>地址：<a href="https://blog.csdn.net/linqunbin">Bruce的博客</a>
                </p>
            </body>
        </html>
        '''
    """
    def __init__(self, smtp_server, from_addr, password, to_addr, type, title, content, photo_path):
        self.smtp_server = smtp_server
        self.from_addr = from_addr
        self.password = password
        self.to_addr = to_addr
        self.type = type
        self.title = title
        self.content = content
        self.photo_path = photo_path

    # 1 创建邮箱(写好邮件内容 发送人 收件人和标题等)
    def msg(self):
        from email.mime.text import MIMEText
        from email.utils import formataddr
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage
        # 发送html邮件
        msg_root = MIMEMultipart('related')
        # 发件人昵称和邮箱,可以写成 formataddr(('林群彬', from_addr))
        msg_root['From'] = formataddr((self.from_addr, self.from_addr))
        # 收件人昵称和邮箱,可以写成 formataddr(('Bruce Lin', from_addr))
        msg_root['To'] = formataddr((self.to_addr, self.to_addr))
        msg_root['Subject'] = self.title
        # 指定图片为当前目录
        fp = open(self.photo_path, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msg_root.attach(msgImage)

        msg_alternative = MIMEMultipart('alternative')
        msg_alternative.attach(MIMEText(self.content, 'html', 'utf-8'))

        msg_root.attach(msg_alternative)

        return msg_root

    # 2 登入账号
    def server(self):
        import smtplib
        # 明文传输端口号是25
        # server = smtplib.SMTP(self.smtp_server, 25)

        # TLS加密: 端口号是587，通信过程加密，邮件数据安全，使用正常的smtp端口。
        # 对于TLS加密方式需要先建立SSL连接，然后再发送邮件。此处使用starttls()来建立安全连接
        # server = smtplib.SMTP(self.smtp_server, 587)
        # server.starttls()

        # SSL加密: 端口号是465，通信过程加密，邮件数据安全。
        server = smtplib.SMTP_SSL(self.smtp_server, 465)
        server.login(self.from_addr, self.password)
        return server

    # 3 发送邮件
    def send_msg(self):
        email_msg = self.msg()
        email_server = self.server()
        try:
            email_server.sendmail(self.from_addr, self.to_addr, email_msg.as_string())
            email_server.quit()
            return "邮件发送成功."
        except Exception as e:
            return '邮件发送失败,错误代码为: %s' % e

if __name__ == '__main__':
    mail_msg = """
    <p>Python 邮件发送测试...</p>
    <p>图片演示：</p>
    <p><img src="cid:image1"></p>
    """
    email = Email(
        smtp_server='smtp.163.com',
        from_addr='fox_benjiaming@163.com',
        password='Kaisa9130',
        to_addr='2623538943@qq.com',
        type='plain',
        title='邮件发送实验',
        content=mail_msg,
        photo_path='test.png'
    )
    print(email.send_msg())
