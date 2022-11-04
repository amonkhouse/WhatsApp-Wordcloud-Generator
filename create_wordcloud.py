import os
import re

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud

cached_stopwords = stopwords.words('english')


class WhatsAppWordCloud():

    def __init__(self, chat_name):

        self.chat_name = chat_name
        self.messages = self.__load_messages()

    def __load_messages(self):
        with open(f'data/{self.chat_name}.txt', 'r') as f:
            all_lines = f.readlines()
        return all_lines

    @staticmethod
    def __starts_with_datetime(message):
        return re.match('\d{2}/\d{2}/\d{4}, \d{2}:\d{2}', message)

    @staticmethod
    def __word_is_link(word):
        return "www." in word or "https" in word or "http" in word

    @staticmethod
    def __process_message_body(message):
        return message.strip('\n').lower()

    @classmethod
    def __remove_stopwords(cls, message):
        return ' '.join([word for word in message.split() if not word in cached_stopwords and not cls.__word_is_link(word)])
    
    @classmethod
    def __get_message(cls, message):
        return cls.__remove_stopwords(cls.__process_message_body(': '.join(message.split(': ')[1:])))

    @staticmethod
    def __valid_message(message):
        return '<Media omitted>' not in message and ': ' in message

    @classmethod
    def __join_multiline_messages(cls, messages):
        parsed_messages = messages.copy()
        messages_to_remove = []
        for i, message in enumerate(messages):
            if cls.__starts_with_datetime(message):
                starts_with_datetime_index = i
            else:
                parsed_messages[starts_with_datetime_index] += message
                messages_to_remove.append(message)
        for message in messages_to_remove:
            parsed_messages.remove(message)
        return parsed_messages
    
    @classmethod
    def __parse_messages(cls, messages):
        condensed_messages = cls.__join_multiline_messages(messages)
        valid_messages = [message for message in condensed_messages if cls.__valid_message(message)]
        message_bodies = [cls.__get_message(message) for message in valid_messages]
        return ' '.join(message_bodies)

    @staticmethod
    def __plot_cloud(wordcloud, chat):
        plt.imshow(wordcloud) 
        plt.axis("off")
        plt.savefig(f'wordclouds/{chat}.png', dpi=300)

    def create_wordcloud(self):
        parsed_messages = self.__parse_messages(self.messages)
        with open('test.txt', 'w') as f:
            f.write(parsed_messages)
        wordcloud = WordCloud(width=3000, height=1500, min_word_length=3, background_color='white').generate(parsed_messages)
        self.__plot_cloud(wordcloud, self.chat_name)


if __name__ == "__main__":
    
    if not os.path.exists("wordclouds/"):
        os.makedirs("wordclouds")

    chat = input("Please enter the name of the chat you want to process: ")
    chat_wordcloud = WhatsAppWordCloud(chat)
    print("Generating wordcloud...")
    chat_wordcloud.create_wordcloud()
    print("Successfully generated wordcloud!")
