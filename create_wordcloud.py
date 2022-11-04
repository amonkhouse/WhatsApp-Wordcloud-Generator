import os
import re
import sys

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud

cached_stopwords = stopwords.words('english')


class WhatsAppWordCloud():

    def __init__(self, chat_name, datetime_format):

        self.chat_name = chat_name
        self.datetime_format = datetime_format
        self.messages = self.__load_messages()

    def __load_messages(self):
        try:
            with open(f'{os.getcwd()}/data/{self.chat_name}.txt', 'r') as f:
                all_lines = f.readlines()
            return all_lines
        except:
            print(
                "Error loading data. Are you sure your file exists in the data/ folder?")
            sys.exit()

    def __starts_with_datetime(self, message):
        return re.match(self.datetime_format, message)

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
        return '<Media omitted>' not in message and 'image omitted' not in message and ': ' in message

    def __join_multiline_messages(self, messages):
        starts_with_datetime_index = 0
        parsed_messages = messages.copy()
        messages_to_remove = []

        for i, message in enumerate(messages):
            if self.__starts_with_datetime(message):
                starts_with_datetime_index = i
            else:
                parsed_messages[starts_with_datetime_index] += message
                messages_to_remove.append(message)
        for message in messages_to_remove:
            parsed_messages.remove(message)
        return parsed_messages

    def __parse_messages(self, messages):
        condensed_messages = self.__join_multiline_messages(messages)
        valid_messages = [
            message for message in condensed_messages if self.__valid_message(message)]
        message_bodies = [self.__get_message(
            message) for message in valid_messages]
        return ' '.join(message_bodies)

    @staticmethod
    def __plot_cloud(wordcloud, chat):
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig(f'wordclouds/{chat}.png', dpi=300)

    def create_wordcloud(self):
        parsed_messages = self.__parse_messages(self.messages)
        wordcloud = WordCloud(width=3000, height=1500, min_word_length=3,
                              background_color='white').generate(parsed_messages)
        self.__plot_cloud(wordcloud, self.chat_name)


def get_os_datetime_format():

    os = input("Are you using IOS or Android? ").lower()
    if os not in ['ios', 'android']:
        print("Please specify 'IOS' or 'Android'.")
        sys.exit()

    if os == 'android':
        return '\d{2}/\d{2}/\d{4}, \d{2}:\d{2}'
    else:
        return '\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}\]'


if __name__ == "__main__":

    if not os.path.exists("wordclouds/"):
        os.makedirs("wordclouds")

    datetime_format = get_os_datetime_format()
    chat = input("Please enter the name of the chat you want to process: ")
    chat_wordcloud = WhatsAppWordCloud(chat, datetime_format)
    print("Generating wordcloud...")
    chat_wordcloud.create_wordcloud()
    print("Successfully generated wordcloud!")
