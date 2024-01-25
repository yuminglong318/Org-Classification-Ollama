import json
import requests
from config import *

with open("descriptions.json", "r", encoding="utf-8") as f:
    descriptions = json.load(f)
    categories = [key for key in descriptions.keys()]

class Chatbot:
    def __init__(self, categories, descriptions) -> None:
        self.model = CHAT_MODEL
        self.system_prompt = {
            "role": "system", 
            "content": f"""You are an AI classifier to classify organizations. You will be given the title and description of an organization from the user. Classify it into the following categories based on the descriptions and your knowledge and just answer one of the following categories, no other words.
            % CATEGORIES: 
            {categories}

            % DESCRIPTIONS: 
            {descriptions}
            """
        }
        self.history = []
        self.messages = []

    def get_response(self):
        response = requests.post(
            "http://0.0.0.0:11434/api/chat",
            json={"model": self.model, "messages": self.messages},
		    stream=True
        )
        response.raise_for_status()
        output = ""

        for line in response.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body.get("done") is False:
                message = body.get("message", "")
                content = message.get("content", "")
                output += content

            if body.get("done", False):
                message["content"] = output
                return message


    def chat(self, user_input):
        self.messages = [self.system_prompt, {'role': 'user', 'content': user_input}]
        bot_response = self.get_response()
        return bot_response['content']
    
def get_classification_ollama(description, title):

    bot = Chatbot(categories, descriptions)
    human_message = f"""
    % Title
    {title}
    % Description
    {description}
    """

    output = bot.chat(human_message)
    for category in categories:
        if category in output:
            return category

description = "Tau Beta Sigma is a National Honorary Band Sorority that provides service to collegiate bands, encourages the advancement of women in the band profession, and promotes and enriches an appreciation of band music through recognition, leadership development."
title = "Tau Beta Sigma"

