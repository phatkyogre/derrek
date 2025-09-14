# derrek
super cool chatbot that uses gemini

***step 1***: make a virtual environment:
  
  python -m venv .venv
  
  to activate it: .venv\Scripts\activate

***step 2*8*: install dependencies:
  
  pip install -r requirements.txt

**step 3**: update .env with your gemini api key.
  
  change "GEMINI_API_KEY=your_api_key_here" to have your actual api key. you can get this at: https://aistudio.google.com/apikey

***step 4***: run the program.
  
  python derrek_bot.py

***OPTIONAL step 5***: build an exe
  
  pip install pyinstaller
  
  pyinstaller --onefile --windowed --add-data ".env;." Derrek.py

  
  ***THIS MIGHT NOT WORK.***

***hard coded commands***:

list: shows a list of every command

change mood <mood> : changes the way he talks. current moods are friendly, grumpy, weird

bye: closes the bot

my name is <name> : teaches derrek your name. he will remember this.

what's my name: derrek will say your name if he knows it.


have fun!!!


***disclaimer: derrek can get MEAN. do not use this chatbot if you are sensitive.***

thanks for using my crappy little project.
