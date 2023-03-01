from pytube import YouTube 
import speech_recognition as sr 
import moviepy.editor as mp
import speech_recognition as sr
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import openai
import os
import speech_recognition as sr
from pydub import AudioSegment
import pandas as pd
def fetch_links(search_word:str) -> list:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-Advertisement")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    youtube_url = f"https://www.youtube.com/results?search_query={search_word}"
    driver.get(youtube_url)
    time.sleep(3)
    item = []
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    item_count = 5
    while item_count > len(item):
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    url_list = [link.get('href') for link in soup.find_all('a') if '/watch?' in str(link) for data in soup] 
    final_urls = []
    for i in url_list:
        final_urls.append("https://www.youtube.com"+str(i))
    return final_urls
def Download(link) -> str:
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_lowest_resolution()
    status = {"Status": 0}   
    try:
        youtubeObject.download(filename="video.mp4")
        title = "video"
        status["Status"] = 1
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    if status["Status"] == 1:
        print("Lets start processing the video")
        return title
def OpenAi_fetct(sentence:str) -> dict:
        api_key = '<Your API_KEY>'
        openai.api_key = api_key
        response = openai.Completion.create(
          engine="text-davinci-003",
         prompt=f"divide the sentence into parts to see What are the most important things that are mentioned in sentence. Whether it is positive or not. return Dictionary. Two keys 'Keywords', 'Sign'. 'Keywords' return as a list and 'Sign' = Positive or Negative or neutral). Sentence is: {dat}",
         max_tokens=1024,
            n=1,
        stop=None,
        temperature=0.5,
        )
        return response.choices[0].text
def clean_data(RAW_TEXT):
    df = pd.DataFrame(RAW_TEXT)
    df = df.replace('\n',' ', regex=True)
    df['Result'] = df['Result'].str.extract(r'({.*})', expand=False)
    df['Result'] = df['Result'].str.strip()
    df['Result'] = df['Result'].str.replace(' ', '')
    df['Result'] = df['Result'].str.replace("'", '')
    df['Result'] = df['Result'].str.replace('"', '')
    df['Result'] = df['Result'].str.replace("'", '').str.replace('"', '').str.replace("Keywords", '"key_words"').str.replace("Sign", '"sign"')
    df['Result'] = df['Result'].str.replace(r'\[', r'["').str.replace(r'\]', r'"]').str.replace(r',', r'", "')
    df['Result'] = df['Result'].str.replace(r'""', r'"')
    df['Result'] = df['Result'].str.replace(r']"', r']').str.replace(r'"\[', r'[')
    save_to_file(df)
    return
def save_to_file(df:pd.DataFrame):
    try:
        df.to_csv('test_data_bigger.csv', index=False, encoding='utf-8')

    except Exception as e:
        print("Exception: "+str(e))
    try:
        df.to_excel('test_data_bigger.xlsx', index=False, encoding='utf-8')
    except Exception as e:
        print("Exception: "+str(e))
    return
search_word = input(str("Give me a word to search:"))
links = fetch_links(search_word)
RAW_TEXT = []
for link in links: 
    try:
        title = Download(link)
    except:
        clean_data(RAW_TEXT)
        break
    video_name = f"{title}.mp4"
    clip = mp.VideoFileClip(video_name)
    clip.audio.write_audiofile("audio.wav")
    file = f"audio.wav"
    file_audio = AudioSegment.from_wav("audio.wav")
    duration = len(AudioSegment.from_wav(file))
    interval = int(25 * (duration/1000))
    start, end, counter, flag = 0, duration, 1, 0  
    counter = 1
    for i in range(0,2*duration,interval):
        if i == 0:
            start = 0
            end = interval
        else:
            start = end
            end = end + interval
        if end > duration:
            end = duration 
            flag = 1
        chunk = file_audio[start:end]
        filename = f"chunk{counter}.wav"
        if start < duration:
            chunk.export(filename, format="wav")
        counter = counter + 1
        AUDIO_FILE = filename
        r = sr.Recognizer()
        try:
            with sr.AudioFile(AUDIO_FILE) as source:
                audio = r.record(source)
            try:
                s = r.recognize_google(audio,show_all=False)
                dat = s.split("}")
                dat = dat[-1]
                sentence = dat
                data = {"Sentecne": sentence, "Result": OpenAi_fetct(dat)}       
                RAW_TEXT.append(data)
                try:
                    os.remove(AUDIO_FILE)
                except:
                    pass
            except Exception as e:              
                print("Exception: "+str(e))
                try:
                    os.remove(AUDIO_FILE)
                except:
                    pass
        except Exception as e:
            print("Exception: "+str(e))
            try:
                os.remove(AUDIO_FILE)
            except:
                pass
clean_data(RAW_TEXT)













