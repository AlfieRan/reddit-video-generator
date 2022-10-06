from gtts import gTTS

# Language in which you want to convert
language = 'en'
accent = 'com.au'

def create(text, path):
	print("Generating audio...")
	myobj = gTTS(text=text, lang=language, slow=False, tld=accent)
	print("Saving audio...")
	myobj.save(path)
	print("Done with audio!")
