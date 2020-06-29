

import smtplib
from email.mime.text import MIMEText
from datetime import datetime


class Email(object):

    





    
    def __init__(self,username,password,sender,targets_list):

        self.username =username
        self.password = password
        self.sender = sender
        self.targets_list = targets_list
        print(username+" "+password+" "+sender)
        print(self.targets_list)
    def sendMessage(self,port,ip,rPort,data):
        timestamp = datetime.now()
        smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
        smtp_ssl_port = 465
        #using the f input
        body=f"""
             <h4>Unauthorized access detected</h4>
             <p>{timestamp}</p>
             <ul>
             <li>port        :{port}</li>
             <li>IP          :{ip}</li>
             <li>Remote Port :{rPort}</li>
             <li>Data        :{data}</li>
             </ul> 
             """
        print(body)

        msg = MIMEText(body, _subtype='html', _charset='windows-1255')

        msg['Subject'] = 'Unathorized Network Intrution'
        msg['From'] = self.sender
        msg['To'] = ', '.join(self.targets_list)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.targets_list, msg.as_string())
        server.quit()
