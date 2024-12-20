import json
import os
import random
import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import wikipediaapi

class EnhancedSelfLearningAssistant:
    def __init__(self, knowledge_file='knowledge.json'):
        # Khởi tạo cơ sở tri thức
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
        
        # Vectorizer để chuyển đổi văn bản
        self.vectorizer = TfidfVectorizer()
        
        # Khởi tạo Wikipedia API
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent='MyAssistantLearningBot/1.0',  
            language='vi',  
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        
        # Huấn luyện ban đầu
        self.train_initial_knowledge()
    
    def load_knowledge(self):
        """Tải hoặc khởi tạo cơ sở tri thức"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    knowledge = json.load(f)
            except json.JSONDecodeError:
                knowledge = {}
        else:
            knowledge = {}
        
        # Đảm bảo các khóa cần thiết luôn tồn tại
        if 'conversations' not in knowledge:
            knowledge['conversations'] = []
        if 'responses' not in knowledge:
            knowledge['responses'] = {}
        if 'learned_patterns' not in knowledge:
            knowledge['learned_patterns'] = []
        if 'wikipedia_cache' not in knowledge:
            knowledge['wikipedia_cache'] = {}
        
        return knowledge
    
    def save_knowledge(self):
        """Lưu cơ sở tri thức"""
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=4)
    
    def train_initial_knowledge(self):
        """Huấn luyện ban đầu với một số mẫu dữ liệu"""
        initial_data = [
            {"input": "xin chào", "response": "Chào bạn! Tôi là trợ lý ảo."},
            {"input": "bạn khỏe không", "response": "Tôi rất khỏe, cảm ơn bạn!"},
            {"input": "tên bạn là gì", "response": "Tôi là trợ lý ảo tự học."},
            {"input": "nhà sáng lập facebook", "response": "Mark Zuckerberg là nhà sáng lập Facebook."},
            {"input": "nhà sáng lập apple", "response": "Steve Jobs và Steve Wozniak là những nhà sáng lập Apple."},
            {"input": "mấy giờ rồi", "response": "Tôi có thể giúp bạn biết giờ hiện tại."},
            {"input": "bây giờ là mấy giờ", "response": "Tôi có thể giúp bạn biết giờ hiện tại."}
        ]
        
        for item in initial_data:
            self.learn(item['input'], item['response'])
    
    def get_current_time(self):
        """Lấy thời gian hiện tại"""
        now = datetime.datetime.now()
        return f"Bây giờ là {now.strftime('%H:%M:%S')} ngày {now.strftime('%d/%m/%Y')}"
    
    def learn(self, user_input, response):
        """Phương thức học từ các tương tác"""
        # Chuẩn hóa đầu vào
        normalized_input = self.normalize_text(user_input)
        
        # Thêm cuộc hội thoại vào kho kiến thức
        self.knowledge['conversations'].append({
            'input': normalized_input,
            'response': response
        })
        
        # Cập nhật từ điển các câu trả lời
        if normalized_input not in self.knowledge['responses']:
            self.knowledge['responses'][normalized_input] = [response]
        else:
            if response not in self.knowledge['responses'][normalized_input]:
                self.knowledge['responses'][normalized_input].append(response)
        
        # Lưu kiến thức
        self.save_knowledge()
    
    def normalize_text(self, text):
        """Chuẩn hóa văn bản để so sánh"""
        return text.lower().strip()
    
    def find_best_response(self, user_input):
        """Tìm câu trả lời phù hợp nhất"""
        # Chuẩn hóa đầu vào
        normalized_input = self.normalize_text(user_input)
        
        # Kiểm tra các từ khóa về thời gian
        time_keywords = ['giờ', 'mấy giờ', 'bây giờ', 'hiện tại']
        if any(keyword in normalized_input for keyword in time_keywords):
            return self.get_current_time()
        
        # Nếu đã học trước đó
        if normalized_input in self.knowledge['responses']:
            return random.choice(self.knowledge['responses'][normalized_input])
        
        # Sử dụng cosine similarity để tìm câu tương tự
        try:
            # Chuẩn bị dữ liệu để so sánh
            all_inputs = list(self.knowledge['responses'].keys())
            all_inputs.append(normalized_input)
            
            # Vectorize
            vectors = self.vectorizer.fit_transform(all_inputs)
            
            # Tìm độ tương tự
            similarity = cosine_similarity(vectors[-1], vectors[:-1])[0]
            
            # Nếu có câu tương tự với độ tương đồng cao
            if max(similarity) > 0.6:
                similar_index = list(similarity).index(max(similarity))
                similar_input = all_inputs[similar_index]
                return random.choice(self.knowledge['responses'][similar_input])
        except:
            pass
        
        # Nếu không tìm thấy
        return "Tôi chưa hiểu. Bạn có thể dạy tôi không?"
    
    def interact(self):
        """Giao diện tương tác với người dùng"""
        print("Trợ lý ảo tự học: Xin chào! Hãy trò chuyện với tôi.")
        
        while True:
            user_input = input("Bạn: ").strip()
            
            # Thoát khỏi chương trình
            if user_input.lower() in ['thoát', 'bye', 'kết thúc']:
                print("Trợ lý: Tạm biệt!")
                break
            
            # Tìm và trả lời
            response = self.find_best_response(user_input)
            print("Trợ lý:", response)
            
            # Học từ phản hồi của người dùng
            if response == "Tôi chưa hiểu. Bạn có thể dạy tôi không?":
                print("Trợ lý: Bạn có thể dạy tôi câu trả lời phải không?")
                teach_response = input("Bạn (câu trả lời): ").strip()
                if teach_response:
                    self.learn(user_input, teach_response)
                    print("Trợ lý: Cảm ơn, tôi đã học được điều mới!")

# Chạy trợ lý
def main():
    assistant = EnhancedSelfLearningAssistant()
    assistant.interact()

if __name__ == "__main__":
    main()