# spell_checker.py
from spellchecker import SpellChecker

# Initialize the SpellChecker object
spell = SpellChecker()

def correct_spelling(text):
    # Split the text into words
    words = text.split()
    
    # Find the misspelled words
    misspelled = spell.unknown(words)
    
    corrected_words = []
    for word in words:
        if word in misspelled:
            # Get the most likely correction for the word
            corrected_word = spell.correction(word)
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)
    
    # Return the corrected text
    corrected_text = ' '.join(corrected_words)
    return corrected_text

if __name__ == "__main__":
    # Test the function with a sample text
    user_input = "I am verry happy to meet you"
    corrected_input = correct_spelling(user_input)
    print("Original Text:", user_input)
    print("Corrected Text:", corrected_input)
