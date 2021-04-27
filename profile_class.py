import sys

class Profile():
    def __init__(id, idList, cred, watcher):
        self.twoFikID = id
        self.list = idList
        self.credential = cred
        self.watcher = watcher

    def getId(self, id):
        for profile in self.list:
            if profile.twoFikID == id:
                return profile.watcher
        return False

    def StartWatch(self):
        
        
    def on_snapshot(doc_snapshot, changes, read_time):
        #print('_____________________________________________________________________________________________________________')
    
        if serverVar.initMessage is True:
            for change in changes:
                print(f'changeType: {change.type.name}')
                if change.type.name == 'ADDED':
                    #doc = change.document.id
                    doc = change.document.to_dict()
                    print('_____________________________________________________________________________________________________________')
                    print(f'doc: {doc}')
                    print('_____________________________________________________________________________________________________________')
                    sender = get_real_name(messages.get('from'))
                    recipient = get_real_name(messages.get('to'))
                    #print(f'recipient: {recipient}')
                    time_of_reception = messages.get('time')
                    text = messages.get('body')
                    nameList = ["sender", "recipient", "time", "text"]
                    dataList = [str(sender), str(recipient), str(time_of_reception), str(text)]
                    TD_CLI.SendMessage(nameList, dataList)

        else:
            for doc in doc_snapshot:
                messages = doc.to_dict()
                #print(f'messages: {messages}')
                sender = get_real_name(messages.get('from'))
                recipient = get_real_name(messages.get('to'))
                #print(f'recipient: {recipient}')
                time_of_reception = messages.get('time')
                text = messages.get('body')
                nameList = ["sender", "recipient", "time", "text"]
                dataList = [str(sender), str(recipient), str(time_of_reception), str(text)]
                serverVar.TD_CLI.SendMessage(nameList, dataList)
                #print(f"sender:     {sender}")
                #print(f"recipient:  {recipient}")
                #print(f"time:       {time_of_reception}")
                #print(f"text:       {text}")
                #print('_____________________________________________________________________________________________________________')
            initMessage = True