import pygame
import google.generativeai as genai
import webbrowser
from gtts import gTTS
import os

class VoiceAssistant:
    def __init__(self, google_api_key):
        # Khởi tạo pygame mixer
        pygame.mixer.init()
        
        # Cài đặt API Google Gemini
        genai.configure(api_key=google_api_key)
        
        # Chọn mô hình
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Lịch sử cuộc trò chuyện để context
        self.conversation_history = []

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

    def get_ai_response(self, user_input):
        """Lấy phản hồi từ Google Gemini"""
        try:
            # Thêm câu hỏi vào lịch sử cuộc trò chuyện
            self.conversation_history.append(user_input)

            # Gọi API Gemini
            response = self.model.generate_content(
                " ".join(self.conversation_history),
                generation_config={
                    "max_output_tokens": 150,
                    "temperature": 0.7,
                    "top_p": 1
                }
            )

            # Lấy nội dung phản hồi
            ai_response = response.text

            # Thêm phản hồi vào lịch sử
            self.conversation_history.append(ai_response)

            return ai_response

        except Exception as e:
            print(f"Lỗi Gemini: {e}")
            return "Xin lỗi, có lỗi xảy ra khi kết nối với trợ lý AI."

    def run(self):
        """Chạy trợ lý ảo"""
        self.speak("Xin chào! Tôi là trợ lý ảo. Bạn cần giúp gì?")
        
        while True:
            # Nhập lệnh từ bàn phím
            command = input("Bạn: ").strip()
            print()  # Dòng trống để tách biệt
            
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
    # Thay YOUR_API_KEY bằng API key của bạn từ Google AI Studio
    GOOGLE_API_KEY = "AIzaSyCreTztrLml5jlt1dnSN9emehKZl42IA9E"
    assistant = VoiceAssistant(GOOGLE_API_KEY)
    assistant.run()

if __name__ == "__main__":
    main()