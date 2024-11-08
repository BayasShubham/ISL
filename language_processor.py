import nltk
import spacy
import language_tool_python # type: ignore
from googletrans import Translator
from gtts import gTTS
from IPython.display import Audio, display

# Download necessary data for NLTK (if needed during runtime)
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

class LanguageProcessor:
    def __init__(self):
        """Initialize the Translator and Language Tools."""
        self.translator = Translator()
        self.tool = language_tool_python.LanguageTool('en-US')

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate the given text to the specified target language."""
        try:
            translated_text = self.translator.translate(text, dest=target_language).text
            print(f"Translated text: {translated_text}")
            return translated_text
        except Exception as e:
            print(f"Error in translation: {e}")
            return text

    def text_to_speech(self, text: str, language_code: str) -> None:
        """Convert the given text to speech and play it."""
        try:
            tts = gTTS(text=text, lang=language_code, slow=False)
            audio_file = "output.mp3"
            tts.save(audio_file)
            display(Audio(audio_file, autoplay=True))
        except Exception as e:
            print(f"Error converting text to speech: {e}")

    def process_text(self, text: str, language_code: str) -> None:
        """Translate the text and then convert it to speech."""
        translated_sentence = self.translate_text(text, language_code)
        self.text_to_speech(translated_sentence, language_code)

    def correct_sentence(self, words: list) -> str:
        """Construct a meaningful sentence from a collection of words and refine it with grammar check."""
        pos_tags = nltk.pos_tag(words)
        subject = verb = obj = None
        for word, tag in pos_tags:
            if tag.startswith('PRP'):  # Pronoun
                subject = word
            elif tag.startswith('VB'):  # Verb
                verb = word
            elif tag.startswith('NN'):  # Noun
                obj = word
        sentence = f"{subject} {verb} {obj}." if subject and verb and obj else " ".join(words) + "."
        matches = self.tool.check(sentence)
        corrected_sentence = language_tool_python.utils.correct(sentence, matches)
        return corrected_sentence
