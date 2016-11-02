# -*- coding: utf-8 -*-

import logging
import random
import sys
import os

logger = logging.getLogger(__name__)
#sys.setdefaultencoding("utf-8")



class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:")
        self.send_message(channel_id, txt)


    def write_greeting(self, channel_id, user_id):

        with open('test.txt', 'r') as filestream:
            for line in filestream:
                greetings = line.split(",")


        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)
# Section for initial conversation between grossman and patient
    def write_convo1(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = ["Hello! This chatbot has been created to help you identify questions you want to ask your doctor, so you can get what you need from your appointment."]
        self.send_message(channel_id, suggestion)
        self.clients.send_user_typing_pause(channel_id)
        question = ["Are you Here for an appointment?"]
        self.send_message(channel_id, question)
    def write_convo2(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "No personal information will be collected, and nothing typed here will be seen by a doctor. This purpose of this chat is to help you prepare for an appointment."
        self.send_message(channel_id, suggestion)
    def write_convo2(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "To start, have you thought about the most important question you want to ask your doctor? "
        self.send_message(channel_id, suggestion)
    def write_convo3(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Terrific! You are on your way to making sure you have a productive appointment."
        self.send_message(channel_id, suggestion)
    def write_convo3_neg(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        suggestion = "Okay, thank you for learning more about this chatbot today! Have a good appointment!"
        self.send_message(channel_id, suggestion)


    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
