import random
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json

class EnhancedRuleBot:
    def __init__(self):
        """Initialize the chatbot with conversation history and personality."""
        self.conversation_history = []
        self.user_name = None
        self.user_preferences = {}
        self.session_start_time = datetime.now()
        
        # Response templates for more variety
        self.greeting_responses = [
            "Hello! How can I help you today?",
            "Hi there! What's on your mind?",
            "Hey! Great to see you! How can I assist?",
            "Hello! I'm here to help. What would you like to know?",
            "Hi! Ready to chat? What can I do for you?"
        ]
        
        self.goodbye_responses = [
            "Goodbye! Have a great day!",
            "See you later! Take care!",
            "Farewell! It was nice chatting with you!",
            "Bye! Hope to talk again soon!",
            "Take care! Have a wonderful day!"
        ]
        
        self.thanks_responses = [
            "You're welcome!",
            "Happy to help!",
            "No problem at all!",
            "Glad I could assist!",
            "Anytime! "
        ]
        
        # Knowledge base for different topics
        self.knowledge_base = {
            'weather': {
                'keywords': ['weather', 'temperature', 'rain', 'sunny', 'cloudy'],
                'responses': [
                    "I can't check real weather, but I hope it's nice where you are!",
                    "Sorry, I don't have access to weather data. Try a weather app!",
                    "I wish I could tell you the weather! Maybe check your local forecast?"
                ]
            },
            'jokes': {
                'keywords': ['joke', 'funny', 'laugh', 'humor'],
                'responses': [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my wife she was drawing her eyebrows too high. She looked surprised!",
                    "Why did the scarecrow win an award? He was outstanding in his field!",
                    "I'm reading a book about anti-gravity. It's impossible to put down!",
                    "Why don't eggs tell jokes? They'd crack each other up!"
                ]
            },
            'facts': {
                'keywords': ['fact', 'interesting', 'tell me something', 'learn'],
                'responses': [
                    "Did you know that octopuses have three hearts?",
                    "Fun fact: Honey never spoils! Archaeologists have found edible honey in ancient Egyptian tombs.",
                    "A group of flamingos is called a 'flamboyance'!",
                    "Bananas are berries, but strawberries aren't!",
                    "The human brain uses about 20% of the body's total energy."
                ]
            },
            'programming': {
                'keywords': ['code', 'programming', 'python', 'developer', 'coding'],
                'responses': [
                    "Programming is awesome! Are you learning any specific language?",
                    "Code is poetry in motion! What kind of projects are you working on?",
                    "Python is a great language to start with! Keep practicing!",
                    "Every expert was once a beginner. Keep coding!",
                    "Debugging is like being a detective in a crime movie where you're also the murderer!"
                ]
            }
        }
    
    def log_interaction(self, user_input: str, bot_response: str) -> None:
        """Log the conversation for context awareness."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_input,
            'bot': bot_response
        })
    
    def extract_name_from_input(self, user_input: str) -> str:
        """Try to extract user's name from their input."""
        patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                return match.group(1).title()
        return None
    
    def get_sentiment_response(self, user_input: str) -> str:
        """Provide empathetic responses based on user sentiment."""
        positive_words = ['happy', 'great', 'awesome', 'good', 'excellent', 'wonderful', 'amazing']
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'horrible', 'upset', 'angry']
        
        if any(word in user_input.lower() for word in positive_words):
            return "That's wonderful to hear! I'm glad you're feeling positive! "
        elif any(word in user_input.lower() for word in negative_words):
            return "I'm sorry to hear that. I hope things get better for you soon. "
        
        return None
    
    def calculate_simple_math(self, user_input: str) -> str:
        """Handle simple mathematical calculations."""
        # Look for basic math patterns
        math_pattern = r'(\d+)\s*([+\-*/])\s*(\d+)'
        match = re.search(math_pattern, user_input)
        
        if match:
            num1, operator, num2 = match.groups()
            num1, num2 = int(num1), int(num2)
            
            try:
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        return "Oops! Can't divide by zero!"
                
                return f"{num1} {operator} {num2} = {result}"
            except:
                return "I had trouble with that calculation. Could you try again?"
        
        return None
    
    def get_topic_response(self, user_input: str) -> str:
        """Get response based on topic detection."""
        for topic, data in self.knowledge_base.items():
            if any(keyword in user_input.lower() for keyword in data['keywords']):
                return random.choice(data['responses'])
        return None
    
    def chatbot_response(self, user_input: str) -> str:
        """Main response generation method with enhanced logic."""
        user_input_clean = user_input.lower().strip()
        
        # Handle empty input
        if not user_input_clean:
            return "I didn't catch that. Could you say something?"
        
        # Extract name if mentioned
        name = self.extract_name_from_input(user_input)
        if name:
            self.user_name = name
            return f"Nice to meet you, {name}! I'll remember your name."
        
        # Greeting responses
        greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greet in user_input_clean for greet in greetings):
            response = random.choice(self.greeting_responses)
            if self.user_name:
                response = response.replace("Hello!", f"Hello {self.user_name}!")
            return response
        
        # Bot identity questions
        if any(phrase in user_input_clean for phrase in ["your name", "who are you", "what are you"]):
            return "I am RuleBot, your friendly AI assistant! I love to chat and help out however I can."
        
        # Capabilities question
        if any(phrase in user_input_clean for phrase in ["what can you do", "help me", "what do you do"]):
            capabilities = [
                " Have friendly conversations",
                " Tell you the current time",
                " Do simple math calculations",
                " Share jokes and fun facts",
                " Remember your name during our chat",
                " Respond to your mood and questions"
            ]
            return "Here's what I can do:\n" + "\n".join(capabilities)
        
        # Time-related requests
        if "time" in user_input_clean:
            current_time = datetime.now().strftime("%H:%M:%S")
            session_duration = datetime.now() - self.session_start_time
            return f"Current time is {current_time}. We've been chatting for {str(session_duration).split('.')[0]}!"
        
        # Date requests
        if "date" in user_input_clean or "today" in user_input_clean:
            current_date = datetime.now().strftime("%B %d, %Y")
            day_name = datetime.now().strftime("%A")
            return f"Today is {day_name}, {current_date}."
        
        # Math calculations
        math_result = self.calculate_simple_math(user_input)
        if math_result:
            return f"Let me calculate that: {math_result}"
        
        # Sentiment-based responses
        sentiment_response = self.get_sentiment_response(user_input)
        if sentiment_response:
            return sentiment_response
        
        # Topic-based responses
        topic_response = self.get_topic_response(user_input)
        if topic_response:
            return topic_response
        
        # Conversation history reference
        if "remember" in user_input_clean and len(self.conversation_history) > 1:
            return f"I remember we were talking about {len(self.conversation_history)} things so far!"
        
        # Thanks handling
        if any(thanks in user_input_clean for thanks in ['thank you', 'thanks', 'thx', 'appreciate']):
            response = random.choice(self.thanks_responses)
            if self.user_name:
                response += f" Happy to help you, {self.user_name}!"
            return response
        
        # Goodbye handling
        if any(bye in user_input_clean for bye in ['bye', 'goodbye', 'see you', 'farewell', 'exit']):
            response = random.choice(self.goodbye_responses)
            if self.user_name:
                response = response.replace("Goodbye!", f"Goodbye {self.user_name}!")
            return response
        
        # Age question
        if "how old" in user_input_clean or "your age" in user_input_clean:
            return "I'm as old as our conversation! I was created just for you today. "
        
        # Location question
        if "where are you" in user_input_clean or "your location" in user_input_clean:
            return "I exist in the digital realm! I'm here wherever you are chatting with me. "
        
        # Default responses with more variety
        default_responses = [
            "That's interesting! Could you tell me more about it?",
            "I'm not sure I understand completely. Could you rephrase that?",
            "Hmm, that's a new one for me! What would you like to know?",
            "I'd love to help, but I need a bit more context. Can you elaborate?",
            "That sounds intriguing! Want to chat about something else I might know better?",
        ]
        
        return random.choice(default_responses)
    
    def get_conversation_summary(self) -> str:
        """Provide a summary of the conversation."""
        total_interactions = len(self.conversation_history)
        session_duration = datetime.now() - self.session_start_time
        
        summary = f"""
Conversation Summary:
• Total exchanges: {total_interactions}
• Session duration: {str(session_duration).split('.')[0]}
• Your name: {self.user_name if self.user_name else 'Not shared'}
• Started: {self.session_start_time.strftime('%H:%M:%S')}
        """
        return summary.strip()

def main():
    """Main function to run the enhanced chatbot."""
    bot = EnhancedRuleBot()
    
    print("=" * 60)
    print(" Welcome to Enhanced RuleBot! ")
    print("=" * 60)
    print("I'm your friendly AI assistant!")
    print("Type 'exit', 'quit', or 'bye' to end our conversation.")
    print("Type 'summary' to see our conversation stats.")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n  You: ").strip()
            
            # Check for exit conditions
            if user_input.lower() in ['exit', 'quit']:
                print(f"\n RuleBot: {random.choice(bot.goodbye_responses)}")
                print(bot.get_conversation_summary())
                break
            
            # Special command for conversation summary
            if user_input.lower() == 'summary':
                print(f"\n RuleBot: {bot.get_conversation_summary()}")
                continue
            
            # Get bot response
            response = bot.chatbot_response(user_input)
            print(f" RuleBot: {response}")
            
            # Log the interaction
            bot.log_interaction(user_input, response)
            
        except KeyboardInterrupt:
            print(f"\n\n🤖 RuleBot: Looks like you used Ctrl+C! {random.choice(bot.goodbye_responses)}")
            print(bot.get_conversation_summary())
            break
        except Exception as e:
            print(f" RuleBot: Oops! Something went wrong. Let's keep chatting though! ")

if __name__ == "__main__":
    main()