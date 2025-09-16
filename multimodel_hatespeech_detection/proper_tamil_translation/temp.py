dic_file = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\tamil\\ta_TA.dic"
txt_file = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\tamil\\tamil_words.txt"

with open(dic_file, "r", encoding="utf-8-sig") as f, open(txt_file, "w", encoding="utf-8-sig") as out:
    lines = f.readlines()
    for line in lines[1:]:  # skip first line if it has word count
        word = line.split("/")[0].strip()
        out.write(f"{word} 1\n")  # '1' as dummy frequency


# To test if the encoding is good
# with open(dic_file, "r", encoding="utf-8-sig") as f:
#     for i, line in enumerate(f):
#         print(line.strip())
#         if i > 10:
#             break