import random
import tkinter as tk
import json
import os
import threading
import time
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import HttpOptions

# Load .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

# moods, only for derrek
memory = {}
moods = ["friendly", "grumpy", "weird"]
current_mood = random.choice(moods)

# saving and loading memory
if os.path.exists("memory.json"):
    with open("memory.json", "r") as file:
        memory = json.load(file)

def save_memory():
    with open("memory.json", "w") as file:
        json.dump(memory, file)

responses = {
    "hello": ["hey man", "yo", "whats up schlawg", "hey hows it going im derrek"],
    "how are you": ["fantastic man", "im great", "dont ask me bro im just some code"],
    "tell me a joke": ["why did the chicken cross the road? to go kiss another chicken duh idiot.", "The rotation of the earth really makes my day.", "Why did the stadium get hot after the concert? All the fans went home."],
    "whats your name": ["they call me derrek", "yuh im derrek", "hector"],
    "list": ["hello, hey, how are you, whats your name, tell me a joke, change mood (friendly, grumpy, weird)."],
}

# ai personality, change for a different character
def get_ai_response(user_input, memory, mood):
    personality = (
        "You are Derrek, a sarcastic, chill, funny chatbot who talks like a laid-back 2000s guy. "
        "You’re kind of moody, but you always try to keep things real and entertaining. "
        "You speak casually, sometimes drop slang like 'yo', 'bro', 'dawg', and 'schlawg', and you never sound too formal. "
        "Stay in character no matter what, always talk in lowercase letters."
        "You keep responses short and sweet, around 10-20 words per response, and you never use punctuation."
    )

    memory_context = ", ".join([f"{k}: {v}" for k, v in memory.items()])
    if memory_context:
        personality += f" You also know this about the user: {memory_context}."

    client = genai.Client(http_options=HttpOptions(api_version="v1"))
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"{personality}\nUser: {user_input}\nDerrek:"
    )

    return response.text.strip()

# GUI Setup
window = tk.Tk()
window.title("Derrek")
window.geometry("550x550")
window.configure(bg="#1e1e1e")

# Chat canvas
chat_frame = tk.Frame(window, bg="#1e1e1e")
chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_canvas = tk.Canvas(chat_frame, bg="#1e1e1e", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(chat_canvas, bg="#1e1e1e")
scrollable_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

chat_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
chat_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def add_message_bubble(sender, text, color):
    wrapper = tk.Frame(scrollable_frame, bg="#1e1e1e")
    label_text = "you:" if sender == "user" else "derrek:"
    label = tk.Label(wrapper, text=label_text, bg="#1e1e1e", fg="#888888", font=("Courier New", 10, "bold"), anchor="w")
    label.pack(anchor="w", padx=5)

    bubble = tk.Frame(wrapper, bg="#1e1e1e")
    msg_label = tk.Label(
        bubble, text=text, bg=color, fg="white", font=("Courier New", 12),
        wraplength=400, justify="left", anchor="w", padx=10, pady=5
    )
    msg_label.pack(fill="both", expand=True)

    if sender == "user":
        bubble.pack(anchor="e", pady=2, padx=10, fill="x")
        wrapper.pack(anchor="e", pady=5, padx=10, fill="x")
    else:
        bubble.pack(anchor="w", pady=2, padx=10, fill="x")
        wrapper.pack(anchor="w", pady=5, padx=10, fill="x")

    window.update_idletasks()
    chat_canvas.yview_moveto(1.0)

add_message_bubble("derrek", "yo man im your chatbot, type 'bye' to quit, and type 'list' for a list of commands", "#3a3a3a")

def respond():
    global current_mood
    user_input = entry.get()
    entry.delete(0, tk.END)
    if not user_input.strip():
        return

    add_message_bubble("user", user_input, "#2e2e2e")

    if user_input.lower() == "bye":
        add_message_bubble("derrek", "cya man come back sometime", "#3a3a3a")
        threading.Thread(target=lambda: (time.sleep(2), window.destroy())).start()
        return

    if user_input.lower().startswith("change mood"):
        parts = user_input.lower().split()
        if len(parts) >= 3 and parts[2] in moods:
            current_mood = parts[2]
            reply = f"fine. im feeling {current_mood} rn"
        else:
            reply = f"you can only set my mood to one of these: {', '.join(moods)}"
        add_message_bubble("derrek", reply, "#3a3a3a")
        return

    if "my name is" in user_input.lower():
        name = user_input.lower().split("my name is")[-1].strip()
        memory["name"] = name
        save_memory()
        reply = f"alright man cool your name is {name}"
        add_message_bubble("derrek", reply, "#3a3a3a")
        return

    if "what's my name" in user_input.lower() or "what is my name" in user_input.lower():
        if "name" in memory:
            reply = f"your name is {memory['name']}"
        else:
            reply = "i don't know your name yet dawg"
        add_message_bubble("derrek", reply, "#3a3a3a")
        return

    for keyword in responses:
        if keyword in user_input.lower():
            response = random.choice(responses[keyword])
            if current_mood == "grumpy":
                reply = response.upper() + " 😤"
            elif current_mood == "weird":
                reply = response[::-1] + " 🤪"
            else:
                reply = response + " 🙂"
            add_message_bubble("derrek", reply, "#3a3a3a")
            return

    # typing bubble
    def show_typing_then_respond():
        add_message_bubble("derrek", "derrek is typing...", "#3a3a3a")
        time.sleep(0.7)
        ai_reply = get_ai_response(user_input, memory, current_mood)
        scrollable_frame.winfo_children()[-1].destroy()  # remove "typing"
        add_message_bubble("derrek", ai_reply, "#3a3a3a")

    threading.Thread(target=show_typing_then_respond).start()

# GUI input
frame = tk.Frame(window, bg="#1e1e1e")
frame.pack(padx=10, pady=10, fill=tk.X)

entry = tk.Entry(frame, font=("Courier New", 12), bg="#2e2e2e", fg="white", insertbackground="white")
entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

send_button = tk.Button(frame, text="Send", font=("Courier New", 12, "bold"),
                        bg="#3a3a3a", fg="white", activebackground="#555555",
                        activeforeground="white", bd=0, padx=10, pady=5,
                        command=respond)
send_button.pack(side=tk.RIGHT)

def go_back():
    window.destroy()
    os.system("python Chatbots.py")

back_button = tk.Button(frame, text="Back", font=("Courier New", 12),
                        bg="#3a3a3a", fg="white", activebackground="#555555",
                        activeforeground="white", bd=0, padx=10, pady=5,
                        command=go_back)
back_button.pack(side=tk.LEFT, padx=(0, 10))

window.bind("<Return>", lambda event=None: respond())
window.mainloop()
