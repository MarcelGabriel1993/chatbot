#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiml
import rospy
import os
import sys

from chatbot.msg import ChatMessage
from std_msgs.msg import String

#This imports the service file
from chatbot.srv import chatService

class Chatbot():
  def __init__(self):
    self._kernel = aiml.Kernel()
    rospy.init_node('chatbot_service')
	
    s = rospy.Service("chatService", chatService, self._handle_service)

  def initialize(self, aiml_dir):
    self._kernel.learn(os.sep.join([aiml_dir, '*.aiml']))
    properties_file = open(os.sep.join([aiml_dir, 'bot.properties']))
    for line in properties_file:
      parts = line.split('=')
      key = parts[0]
      value = parts[1]
      self._kernel.setBotPredicate(key, value)
    rospy.logwarn('Done initializing chatbot.')
    rospy.spin()

  def _handle_service(self, chat_message):
    requestString = str(chat_message.question)
    requestString = requestString.replace('ä','ae')
    requestString = requestString.replace('ö','oe')
    requestString = requestString.replace('ü','ue')
    requestString = requestString.replace('ß','ss')

    response = ''
    response = self._kernel.respond(requestString)

    return response

def main():
  chatbot = Chatbot()
  aiml_dir = sys.argv[1]
  chatbot.initialize(aiml_dir)
    
if __name__ == '__main__':
  main()
