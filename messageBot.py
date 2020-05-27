from fbchat import Client, log
from fbchat.models import *
import apiai, codecs, json


class Mma(Client):

    def apiaiConnection(self):
        self.CLIENT_ACCESS_TOKEN = "e6f4564bb4d74d909561ad99fdf88e13"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang ='de' #default lang is ENGLISH
        self.request.session_id = "<SESSION_ID, UNIQUE FOR EACH USER>"


    def onMessage(
        self,
        author_id=None,
        message=None,
        message_object=None,
        thread_id=None,
        thread_type=ThreadType.USER,
        **kwargs
    ):
        self.markAsRead(author_id)
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        #Establish connection with apiai
        self.apiaiConnection()

        mgText = message_object.text
        self.request.query = mgText
        response = self.request.getresponse()

        obj = json.load(response)

        reply = obj['result']['fulfillment']['speech']

        if author_id != self.uid:
            self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)

        self.markAsDelivered(author_id, thread_id)


client = Mma(email='your email address', password='password')
client.listen()

