import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import openai
import webbrowser
import datetime


class VoiceAssistant:
    def __init__(self, openai_api_key):
        # Khởi tạo pygame mixer
        pygame.mixer.init()
        
        # Cài đặt API OpenAI
        openai.api_key = openai_api_key
        
        # Cài đặt nhận dạng giọng nói
        self.recognizer = sr.Recognizer()
        
        # Lịch sử cuộc trò chuyện để context
        self.conversation_history = [
            {"role": "system", "content": "Bạn là trợ lý ảo thân thiện, trợ giúp người dùng bằng tiếng Việt. Hãy trả lời ngắn gọn và rõ ràng."}
        ]

    def speak(self, text):
        """Chuyển văn bản thành giọng nói bằng tiếng Việt"""
        print("Trợ Lý:", text)
        
        # Tạo file âm thanh tạm thời
        tts = gTTS(text, lang='vi')
        filename = "temp.mp3"
        tts.save(filename)
        
        # Phát âm thanh
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Đợi cho âm thanh phát xong
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Xóa file tạm
        pygame.mixer.music.unload()
        os.remove(filename)

    def listen(self):
        """Nghe và chuyển giọng nói thành văn bản"""
        with sr.Microphone() as source:
            print("Đang nghe...")
            # Điều chỉnh độ nhiễu
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                # Lắng nghe âm thanh
                audio = self.recognizer.listen(source, timeout=5)
                
                # Nhận dạng giọng nói
                text = self.recognizer.recognize_google(audio, language="vi-VN")
                print("Bạn:", text)
                return text
            
            except sr.UnknownValueError:
                self.speak("Xin lỗi, tôi không nghe rõ. Bạn có thể nói lại không?")
                return ""
            except sr.RequestError:
                self.speak("Xin lỗi, có lỗi kết nối. Vui lòng kiểm tra internet.")
                return ""

    def get_ai_response(self, user_input):
        """Lấy phản hồi từ OpenAI"""
        try:
            # Thêm câu hỏi vào lịch sử cuộc trò chuyện
            self.conversation_history.append(
                {"role": "user", "content": user_input}
            )

            # Gọi API OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Mô hình tiết kiệm chi phí nhất
                messages=self.conversation_history,
                max_tokens=150  # Giới hạn độ dài câu trả lời
            )

            # Lấy nội dung phản hồi
            ai_response = response.choices[0].message.content

            # Thêm phản hồi vào lịch sử
            self.conversation_history.append(
                {"role": "assistant", "content": ai_response}
            )

            return ai_response

        except Exception as e:
            print(f"Lỗi OpenAI: {e}")
            return "Xin lỗi, có lỗi xảy ra khi kết nối với trợ lý AI."

    def run(self):
        """Chạy trợ lý ảo"""
        self.speak("Xin chào! Tôi là trợ lý ảo. Bạn cần giúp gì?")
        
        while True:
            # Nghe lệnh
            command = self.listen()
            
            if not command:
                continue

            # Kiểm tra lệnh thoát
            if "kết thúc" in command.lower() or "thoát" in command.lower():
                self.speak("Tạm biệt! Hẹn gặp lại.")
                break

            # Xử lý lệnh đặc biệt
            if "google" in command.lower():
                search_terms = command.replace("google", "").strip()
                search_url = f"https://www.google.com/search?q={search_terms}"
                webbrowser.open(search_url)
                self.speak(f"Đang tìm kiếm '{search_terms}' trên Google")
                continue

            # Lấy phản hồi từ AI
            response = self.get_ai_response(command)
            
            # Trả lời bằng giọng nói
            self.speak(response)

def main():

    OPENAI_API_KEY = "sk-1234efgh5678ijkl1234efgh5678ijkl1234efgh"
    assistant = VoiceAssistant(OPENAI_API_KEY)
    assistant.run()

if __name__ == "__main__":
    main()