# WhatsApp Wordcloud Generator

This project contains code to create a Wordcloud that shows you the most commonly used words in a WhatsApp chat.

## Setup

This project runs using Python 3.

### Installing requirements

Before running the main program, you must install the requirements and download the English stopwords corpus that is used in processing messages. Stopwords are common words such _the_, _a_, _and_.

1. Install requirements by running `pip install -r requirements.txt`
2. Download the stopwords corpus by running `python setup.py`

### Download WhatsApp data

You can find out how to download chat history [here](https://faq.whatsapp.com/196737011380816). Make sure to export without media! Place your files in a `data/` folder at the top level of this project. They must have the `.txt` suffix.

## Running the main program

To create a Wordcloud, run `python create_wordcloud.py`. The program will prompt you for the name of the file that you want to process. This file must be in a folder called `data` and have a `.txt` suffix. As an example, if you have a file called "Amy.txt" in your data folder, you would only need to type "Amy".
Wordclouds will be saved to a `wordclouds` folder.

## Extras

There's no tests or much error handling here yet sorry xx
