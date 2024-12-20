import os
import pygame   #Để phát âm thanh.
import speech_recognition as sr  #Để nhận diện giọng nói.
import time
import sys
import ctypes
import wikipedia    # Để tìm kiếm thông tin và mở trình duyệt.
import datetime
import json
import re
import webbrowser   # Để tìm kiếm thông tin và mở trình duyệt.
import smtplib
import requests
import urllib
import urllib.request as urllib2
from selenium import webdriver  #Điều khiển trình duyệt tự động.
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS   #Chuyển văn bản thành âm thanh.
from youtube_search import YoutubeSearch    #Tìm kiếm video trên YouTube.
import xml.etree.ElementTree as ET
import requests     #Tương tác với các API bên ngoài.

#  Khai báo biến mặc định
wikipedia.set_lang('vi')    #Thiết lập ngôn ngữ tiếng Việt cho Wikipedia.
language = 'vi'
path = ChromeDriverManager().install()  #Cài đặt trình điều khiển Chrome thông qua ChromeDriverManager

# Chức năng chuyển văn bản thành âm thanh
def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("sound.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("sound.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    os.remove("sound.mp3")


# Chức năng chuyển âm thanh thành văn bản
def get_audio(mode='mixed'):
    if mode == 'speech':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Tôi: ", end='')
            audio = r.listen(source, phrase_time_limit=5)
            try:
                text = r.recognize_google(audio, language="vi-VN")
                print(text)
                return text
            except:
                print("...")
                return 0
    elif mode == 'text':
        print("Tôi: ", end='')
        text = input()
        return text
    else:  # mixed mode
        print("Nhập 'n' để nhập văn bản, hoặc nhấn Enter để nói")
        choice = input("Lựa chọn: ")
        if choice.lower() == 'n':
            print("Tôi: ", end='')
            return input()
        else:
            return get_audio('speech')

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            print("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(2)
    stop()
    return 0

# Chức năng giao tiếp, chào hỏi
def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
    else:
        speak("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))

# Chức năng hiển thị thời gian
def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")

def get_day(text):
    now = datetime.datetime.now()
    if "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")

# Chức năng mở ứng dụng hệ thống, website và chức năng tìm kiếm từ khóa trên Google
def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
    elif "word" in text:
        speak("Mở Microsoft Word")
        # Replace with the actual path to WINWORD.EXE on your computer
        os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE')
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        # Replace with the actual path to EXCEL.EXE on your computer
        os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")

def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở.")
        return True
    else:
        return False

def open_google_and_search(text):
    search_for = text.split("kiếm", 1)[1]
    speak('Okay!')
    driver = webdriver.Chrome(path)
    driver.get("http://www.google.com")
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys(str(search_for))
    que.send_keys(Keys.RETURN)

def send_email(text):
    speak('Bạn gửi email cho ai nhỉ')
    recipient = get_text()
    if 'phát' in recipient:
        speak('Nội dung bạn muốn gửi là gì')
        content = get_text()
        mail = smtplib.SMTP('thachsungbucac.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('banconcop113@gmail.com', 'liuhinphat2003')
        mail.sendmail('banconcop113@gmail.com',
                      'banconcop113@gmail.com', content.encode('utf-8'))
        mail.close()
        speak('Email của bạn vùa được gửi. Bạn check lại email nhé hihi.')
    else:
        speak('Bot không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?')

#dự báo thời tiết
def get_city_name(city):
    # Chuyển đổi các tên thành phố hoặc quốc gia về tên chuẩn
    city_mappings = {
        "sài gòn": "saigon",
        "hồ chí minh": "saigon",
        "hà nội": "hanoi",
        "thủ đô": "hanoi",
        "vietnam": "vietnam",
        "việt nam": "vietnam",
        "đà nẵng": "danang",
        "hải phòng": "haiphong"
    }
    
    # Kiểm tra xem có trong danh sách mapping không, nếu có thì trả về tên chuẩn
    city = city.strip().lower()
    return city_mappings.get(city, city)

def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Lấy tên thành phố người dùng nhập
    city = get_text()
    
    # Nếu không nhập thành phố, thoát khỏi hàm
    if not city:
        return
    
    # Chuyển đổi tên thành phố nếu có trong mapping
    city = get_city_name(city)
    
    api_key = "0b15f52ee69644ae8e36ff3eb8022bd7"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    
    # Gửi yêu cầu đến OpenWeatherMap API
    response = requests.get(call_url)
    data = response.json()
    
    # Kiểm tra kết quả trả về từ API
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
  

        
        now = datetime.datetime.now()  
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay {description}.""".format(
            day=now.day, month=now.month, year=now.year, 
            hourrise=sunrise.hour, minrise=sunrise.minute,
            hourset=sunset.hour, minset=sunset.minute,
            temp=current_temperature, pressure=current_pressure, 
            humidity=current_humidity, description=weather_description
        )
        
        speak(content)
        time.sleep(20)
    else:
        speak("Không tìm thấy địa chỉ của bạn")

# Chức năng phát nhạc trên Youtube
def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    mysong = get_text()

    try:
        # Tìm kiếm bài hát trên YouTube
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        
        if result:
            # Mở bài hát đầu tiên trong danh sách kết quả
            url = 'https://www.youtube.com' + result[0]['url_suffix']
            webbrowser.open(url)
            speak("Bài hát bạn yêu cầu đã được mở.")
        else:
            speak("Xin lỗi, tôi không tìm thấy bài hát nào phù hợp.")
    except Exception as e:
        # Xử lý lỗi
        speak("Đã xảy ra lỗi trong quá trình tìm kiếm bài hát. Vui lòng thử lại sau.")
        print(f"Lỗi: {e}")


    # Chức năng đọc báo ngày hôm nay
def read_news():
    speak("Bạn muốn đọc loại báo gì? Có các mục:tin mới nhất, thế giới, thời sự, kinh doanh, giải trí, thể thao, pháp luật, giáo dục, tin nổi bật ,khoa học, sức khỏe, số hóa,xe, tâm sự, cười, tin xem nhiều")
    category = get_text()
    
    # Dictionary mapping categories to RSS URLs
    rss_urls = {
        "tin mới nhất": "https://vnexpress.net/rss/tin-moi-nhat.rss",
        "thế giới": "https://vnexpress.net/rss/the-gioi.rss",
        "thời sự": "https://vnexpress.net/rss/thoi-su.rss",
        "kinh doanh": "https://vnexpress.net/rss/kinh-doanh.rss",
        "giải trí": "https://vnexpress.net/rss/giai-tri.rss",
        "thể thao": "https://vnexpress.net/rss/the-thao.rss",
        "pháp luật":"https://vnexpress.net/rss/phap-luat.rss",
        "giáo dục": "https://vnexpress.net/rss/giao-duc.rss",
        "tin nổi bật": "https://vnexpress.net/rss/tin-noi-bat.rss",
        "sức khỏe": "https://vnexpress.net/rss/suc-khoe.rss",
        "đời sống": "https://vnexpress.net/rss/gia-dinh.rss",
        "du lịch": "https://vnexpress.net/rss/du-lich.rss",
        "khoa học": "https://vnexpress.net/rss/khoa-hoc.rss",
        "số hóa": "https://vnexpress.net/rss/so-hoa.rss",
        "xe": "https://vnexpress.net/rss/oto-xe-may.rss",
        "ý kiến":"https://vnexpress.net/rss/y-kien.rss",
        "tâm sự": "https://vnexpress.net/rss/tam-su.rss",
        "cười": "https://vnexpress.net/rss/cuoi.rss",
        "tin xem nhiều": "https://vnexpress.net/rss/tin-xem-nhieu.rss",

    }
    
    # Get RSS URL based on category
    rss_url = None
    for key in rss_urls:
        if key in category.lower():
            rss_url = rss_urls[key]
            break
    
    if not rss_url:
        speak("Xin lỗi, tôi không tìm thấy mục báo này. Vui lòng thử lại với một mục khác.")
        return
        
    try:
        # Fetch and parse RSS feed
        response = requests.get(rss_url)
        response.encoding = 'utf-8'  # Ensure proper encoding
        root = ET.fromstring(response.text)
        
        # Get all news items
        items = root.findall('.//item')
        
        speak(f"Có {len(items)} tin mới nhất trong mục {category}. Tôi sẽ đọc các 10 tin đầu của các tiêu đề cho bạn.")
        
        # Read titles and store links
        news_dict = {}
        for i, item in enumerate(items[:10], 1):  # Limit to first 10 news items
            title = item.find('title').text
            link = item.find('link').text
            news_dict[i] = {'title': title, 'link': link}
            speak(f"Tin {i}: {title}")
            
        speak("Bạn muốn đọc tin số mấy? Hãy nói số thứ tự của tin.")
        choice = get_text()
        
        # Convert spoken number to integer
        try:
            number = int(''.join(filter(str.isdigit, choice)))
            if number in news_dict:
                speak(f"Đang mở tin số {number}")
                webbrowser.open(news_dict[number]['link'])
            else:
                speak("Số tin không hợp lệ. Vui lòng thử lại.")
        except:
            speak("Tôi không hiểu số tin bạn chọn. Vui lòng thử lại.")
            
    except Exception as e:
        speak("Có lỗi xảy ra khi đọc tin tức. Vui lòng thử lại sau.")
        print(f"Error: {str(e)}")

# Chức năng tìm định nghĩa trên từ điển wikipedia
def tell_me_about():
    try:
        speak("Bạn muốn hỏi về gì ạ")
        search_query = get_text()
        
        # First API call to search for the term
        search_url = f"https://vi.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(search_query)}&format=json"
        search_response = requests.get(search_url)
        search_data = search_response.json()
        
        # Check if we got any search results
        if not search_data.get('query', {}).get('search'):
            speak("Xin lỗi, tôi không tìm thấy thông tin về chủ đề này")
            return
            
        # Get the page ID of the first result
        page_id = search_data['query']['search'][0]['pageid']
        
        # Second API call to get the content
        content_url = f"https://vi.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={page_id}&format=json&explaintext=1"
        content_response = requests.get(content_url)
        content_data = content_response.json()
        
        # Extract the content
        extract = content_data['query']['pages'][str(page_id)]['extract']
        
        # Split content into paragraphs
        paragraphs = [p for p in extract.split('\n') if p.strip()]
        
        # Read all paragraphs continuously
        if paragraphs:
            for paragraph in paragraphs:
                speak(paragraph)
                time.sleep(2)  # Adjust the delay as needed
        
        speak('Cảm ơn bạn đã lắng nghe!')
        
    except Exception as e:
        print(f"Error: {str(e)}")
        speak("Xin lỗi, đã có lỗi xảy ra khi tìm kiếm thông tin. Vui lòng thử lại.")   


# Chức năng hiển thị các khả năng của trợ lý ảo
def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Gửi email
    6. thời tiết
    7. mở nhạc
    8. Thay đổi hình nền máy tính
    9. Đọc báo hôm nay
    10. Kể bạn biết về thế giới """)



#  Kết hợp tất cả chức năng Trợ lý ảo Tiếng Việt 
def assistant():
    speak("Xin chào, bạn tên là gì nhỉ?")
    name = get_text()
    if name:
        speak("Chào bạn {}".format(name))
        speak("Bạn cần Bot Alex có thể giúp gì ạ?")
        while True:
            text = get_text()
            if not text:
                break
            elif any(phrase in text for phrase in [
                "dừng",
                "tạm biệt",
                "chào robot",
                "ngủ thôi" 
            ]):
                stop()
                break
            elif "bot có thể làm gì" in text:
                help_me()
            elif any(phrase in text for phrase in [
                "chào trợ lý ảo",
                "chào",
                "chào bạn",
                "chào em",
                "chào bot"
            ]):
                hello(name)
            elif any(phrase in text for phrase in [ 
                 "mấy giờ rồi",
                 "bi giờ là mấy giờ rồi",
                 "mấy giờ rồi bot",
                 "bi giờ là mấy giờ rồi bot"
                ]):
                get_time(text) 
            elif any(phrase in text for phrase in [
                "hôm nay là ngày mấy",
                "hôm nay là ngày mấy vậy bot"
            ]):
                get_day(text)
            elif "mở" in text:
                if "mở google và tìm kiếm" in text:
                    open_google_and_search(text)
                elif "." in text:
                    open_website(text)
                else:
                    open_application(text)
            elif "email" in text or "mail" in text or "gmail" in text:
                send_email(text)
            elif any(phrase in text for phrase in [
                "thời tiết",
                "hôm nay thời tiết như thế nào",
                "hôm nay trời có mưa không",
                "tôi muốn biết thời tiết hôm nay như nào"
            ]):
                current_weather()
            elif "mở nhạc" in text:
                play_song()
            elif "đọc báo" in text:
                read_news()
            elif "tôi muốn hỏi" in text:
                tell_me_about()
            else:
                speak("Bạn cần Bot giúp gì ạ?")

 # Thêm vào cuối file
if __name__ == "__main__":
    assistant()