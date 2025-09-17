from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from multimodel_hatespeech_detection.proper_tamil_translation import tamil_normalizer

input_file = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\corpus_source\\vadivelu_dialogues\\vadivelu_dialogues_1.txt"
output_file = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\corpus_source\\vadivelu_dialogues\\transliterated_vadivelu_dialogues.txt"


with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "a", encoding="utf-8") as fout:
    for line in fin:
        words = line.strip().split()
        translit_words = []
        for word in words:
            translit_word = tamil_normalizer.transliterate_to_tamil(word)
            translit_word = tamil_normalizer.correct_tamil_spelling(translit_word)
            translit_words.append(translit_word)
        fout.write(" ".join(translit_words) + "\n")

print(f"✅ Word-by-word transliteration appended to {output_file}")