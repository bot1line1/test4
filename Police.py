import subprocess,re,os
from line import LineClient, LineGroup, LineContact, LineAPI

try:
    client = LineClient("bot1line1@yopmail", "bot1line123")
    print client.authToken
 
except:
    print "Login Failed"


while True:
    op_list = []
    timeSeen = []
    appendSeen = []
    dataResult = []
    #recheck
    userList = []
    timelist =[]
    contacts = []
    recheckData = []
    #cancelAll
    myListMember = []
    
   
    #getFriend list @
    listFriend = []

    for op in client.longPoll():
        op_list.append(op)

    for op in op_list:
        sender   = op[0]
        receiver = op[1]
        message  = op[2]

        if message.text is not None:
            msg = message.text
            # hadist
            if '/hd' in msg:
                arg = msg.split('-');
                if len(arg) > 1:
                    imam = arg[0][3:].strip();
                    nom = arg[1].strip();
                    x='wget http://hadits.stiba.ac.id/\?imam\='+imam+'\&no\='+nom+'\&type\=hadits -qO - | awk \''+'BEGIN{IGNORECASE=1;FS=\"<div class=\\"ja-newsitem\\"'+' style=\\"width: 100%;\\">|</div>";RS=EOF} {print $13}\''
                    proc=subprocess.Popen(x, shell=True, stdout=subprocess.PIPE) 
                    xx=proc.communicate()[0].strip();
                    pr = xx.replace('<p class="arab">','')
                    pr = pr.replace('<p class="indo">','')
                    pr = pr.replace('<h3>Terjemahan</h3>','Terjemahan : ')
                    pr = pr.replace('</p>','')
                    pr = pr.replace('<p>','')
                    if len(pr) == 51:
                        receiver.sendMessage('Not Found')
                    else:
                        receiver.sendMessage(pr)
                else :
                    helps  = '== help ==\n'
                    helps += '[*]tirmidzi => (At Tirmidzi) \n[*]abudaud => (Abu Daud)\n[*]ahmad => (Ahmad)\n[*]bukhari => (Bukhari)\n[*]darimi => (Ad Darimi)\n[*]ibnumajah => (Ibnu Majah) \n[*]malik => (Malik)\n[*]muslim => (Muslim)\n[*]nasai => (An Nasa\'i)\n\ncontoh: /hd darimi-63\n\n* mencari hadist imam (ad darimi) nomer 63'
                    receiver.sendMessage(helps)
            # lirik
            if '/lirik' in msg:
                arg = msg.split('-');
                if len(arg) > 1:
                    artist = arg[0][6:].strip().replace(' ','_')
                    song = arg[1].strip().replace(' ','_')
                    proc=subprocess.Popen('curl -s http://www.lyricsmode.com/lyrics/'+artist[0]+'/'+artist+'/'+song+'.html | sed \'s/<p id=\"lyrics_text\" class=\"ui-annotatable\">//;s/<\/p>/\|/\' | grep \'<br />\'', shell=True, stdout=subprocess.PIPE) 
                    x=proc.communicate()[0]
                    if(len(x) > 10):
                        first = x.replace('</li></ul></div><div class="visible-print header-print"><b>','')
                        first = first.replace('<br />','')
                        first = first.replace('&ndash;','-')
                        first = first.replace('</b></div>','\n')
                        receiver.sendMessage(first)
                    else:
                        receiver.sendMessage('not found ~')
                else:
                    receiver.sendMessage('contoh cari : lirik once-dealova')
            # kbbi
            if '/kbbi' in msg:
                arg = msg.split(' ')
                if len(arg) == 2:
                    proc=subprocess.Popen('curl -s http://kbbi.web.id/'+arg[1]+' | sed \'s/<div id=\"d1\">//;s/<\/div>/\|/\' | grep \'<div id=\"info\"\'', shell=True, stdout=subprocess.PIPE) 
                    x=proc.communicate()[0]
                    output = x[24:-7]
                    first = output.replace('<em>','(')
                    second = first.replace('</em>',')')
                    third =  second.replace('&#183;','-')
                    third = third.replace('<br/>','\n')
                    third = third.replace('</b>',' =>')
                    third = third.replace('<b>','')
                    receiver.sendMessage(third)
                else:
                    receiver.sendMessage('Tidak ditemukan, coba diulang Kembali')
            if 'clearall' in msg :
                if sender.id in myfriend:
                    proc=subprocess.Popen("echo '' > Output.txt", shell=True, stdout=subprocess.PIPE, )
                    receiver.sendMessage('refresh..')
            if 'thens' == msg:
                proc=subprocess.Popen("cat Output.txt | grep -v '.*"+receiver.id+".*' > dest.txt ; rm Output.txt ; mv dest.txt Output.txt", shell=True, stdout=subprocess.PIPE, )
                receiver.sendMessage('iya ')
            # recheck
            if 'recheck' == msg.lower():
                with open('Output.txt','r') as rr:
                    contactArr = rr.readlines()
                    for v in xrange(len(contactArr) -1,0,-1):
                        num = re.sub(r'\n', "", contactArr[v])
                        contacts.append(num)
                        pass
                    contacts = list(set(contacts))
                    for z in range(len(contacts)):
                        arg = contacts[z].split('|')
                        if arg[1] == receiver.id :
                            userList.append(arg[0])
                            timelist.append(arg[2])
                    uL = list(set(userList))
                    # print uL
                    for ll in range(len(uL)):
                        try:
                            getIndexUser = userList.index(uL[ll])
                            timeSeen.append(time.strftime("%H:%M:%S", time.localtime(int(timelist[getIndexUser]) / 1000)))
                            recheckData.append(userList[getIndexUser])
                        except IndexError:
                            conName.append('nones')
                            pass

                    contactId = client._getContacts(recheckData)
                    for v in range(len(recheckData)):
                        dataResult.append(contactId[v].displayName + '['+timeSeen[v]+']')
                        pass
                    # # print len(recheckData)
                    tukang = "V=ON Members=V\n[*]"
                    grp = '\n[*] '.join(str(f) for f in dataResult)
                    receiver.sendMessage("%s %s" % (tukang, grp))

            # contoh chat
            if 'help' in msg.lower():
                receiver.sendMessage('Cek it dot http://www.prog-indo.blogspot.com')
