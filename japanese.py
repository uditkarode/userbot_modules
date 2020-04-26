import re
import requests
from .. import command, module

def romajiToJapanese(romaji):
    romaji = romaji.lower()
    currentAlphabet = hiragana
    hiraganaIsCurrent = True
    resultStr = ""
    i = 0
    while i < len(romaji):
        if romaji[i] == "*":  # switch alphabets
            if hiraganaIsCurrent:
                currentAlphabet = katakana
                hiraganaIsCurrent = False
            else:
                currentAlphabet = hiragana
                hiraganaIsCurrent = True
            i += 1
        elif romaji[i] == " ":  # check wa rule
            if i + 3 < len(romaji):
                if romaji[i:i + 4] == " wa ":  # ha/wa rule
                    resultStr += " %s " % currentAlphabet["ha"]
                    i += 4
                    continue
            resultStr += " "
            i += 1
        elif i + 2 < len(romaji) and romaji[i] == "n" and romaji[i + 1:i + 2] == "n" and romaji[
                                                                                         i + 1:i + 3] not in currentAlphabet:  # n rule
            resultStr += currentAlphabet["sakuon"]
            i += 1
        else:
            checkLen = min(3, len(romaji) - i)
            while checkLen > 0:
                check_str = romaji[i:i + checkLen]
                if check_str in currentAlphabet:
                    resultStr += currentAlphabet[check_str]
                    i += checkLen
                    if i < len(romaji):
                        if romaji[i] == "o" and romaji[i - 1:i] == "o" and hiraganaIsCurrent:  # oo = ou rule
                            resultStr += currentAlphabet["u"]
                            i += 1
                        elif romaji[i] == "e" and romaji[i - 1:i] == "e" and hiraganaIsCurrent:  # ee = ei rule
                            resultStr += currentAlphabet["i"]
                            i += 1
                        elif romaji[i] == romaji[i - 1:i] and not hiraganaIsCurrent:
                            if romaji[i] == "n":
                                break
                            elif romaji[i] in ["a", "e", "i", "o", "u"]:
                                resultStr += currentAlphabet["pause"]
                            else:
                                resultStr += currentAlphabet["sakuon"]
                            i += 1
                    break
                elif checkLen == 1:
                    if check_str == "?":
                        resultStr += "？"

                    if check_str == ".":
                        resultStr += "。"

                    if check_str == "!":
                        resultStr += "！"

                    elif check_str not in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                                           "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
                                           "z", ".", "!", "?"]:  # print any characters that aren't a letter
                        resultStr += check_str
                    elif i + 1 < len(romaji):  # little tsu rule
                        if check_str == romaji[i + 1:i + 2]:
                            resultStr += currentAlphabet["sakuon"]
                    i += 1
                    break
                checkLen -= 1
    return resultStr
def clean(src_str, clean_squares=True):
    ret = src_str.replace('\'', '')
    if clean_squares:
        ret = ret.replace('[', '').replace(']', '')
    return ret

hiragana = {"a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
            "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
            "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
            "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
            "za": "ざ", "ji": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
            "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
            "da": "だ", "de": "で", "do": "ど",
            "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
            "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
            "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
            "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",
            "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
            "ya": "や", "yu": "ゆ", "yo": "よ",
            "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
            "wa": "わ", "wo": "を",
            "n": "ん",
            "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
            "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
            "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
            "ja": "じゃ", "ju": "じゅ", "jo": "じょ",
            "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
            "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
            "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
            "bya": "びゃ", "byu": "びゅ", "byo": "びょ",
            "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",
            "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
            "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
            "vu": "ゔ",
            "sakuon": "っ"}
katakana = {"a": "ア", "i": "イ", "u": "ウ", "e": "エ", "o": "オ",
            "ka": "カ", "ki": "キ", "ku": "ク", "ke": "ケ", "ko": "コ",
            "ga": "ガ", "gi": "ギ", "gu": "グ", "ge": "ゲ", "go": "ゴ",
            "sa": "サ", "shi": "シ", "su": "ス", "se": "セ", "so": "ソ",
            "za": "ザ", "ji": "ジ", "zu": "ズ", "ze": "ゼ", "zo": "ゾ",
            "ta": "タ", "chi": "チ", "tsu": "ツ", "te": "テ", "to": "ト",
            "da": "ダ", "de": "デ", "do": "ド",
            "na": "ナ", "ni": "ニ", "nu": "ヌ", "ne": "ネ", "no": "ノ",
            "ha": "ハ", "hi": "ヒ", "fu": "フ", "he": "ヘ", "ho": "ホ",
            "ba": "バ", "bi": "ビ", "bu": "ブ", "be": "ベ", "bo": "ボ",
            "pa": "パ", "pi": "ピ", "pu": "プ", "pe": "ペ", "po": "ポ",
            "ma": "マ", "mi": "ミ", "mu": "ム", "me": "メ", "mo": "モ",
            "ya": "ヤ", "yu": "ユ", "yo": "ヨ",
            "ra": "ラ", "ri": "リ", "ru": "ル", "re": "レ", "ro": "ロ",
            "wa": "ワ", "wo": "ヲ",
            "n": "ン",
            "kya": "キャ", "kyu": "キュ", "kyo": "キョ",
            "gya": "ギャ", "gyu": "ギュ", "gyo": "ギョ",
            "sha": "シャ", "shu": "シュ", "sho": "ショ",
            "ja": "ジャ", "ju": "ジュ", "jo": "ジョ",
            "cha": "チャ", "chu": "チュ", "cho": "チョ",
            "nya": "ニャ", "nyu": "ニュ", "nyo": "ニョ",
            "hya": "ヒャ", "hyu": "ヒュ", "hyo": "ヒョ",
            "bya": "ビャ", "byu": "ビュ", "byo": "ビョ",
            "pya": "ピャ", "pyu": "ピュ", "pyo": "ピョ",
            "mya": "ミャ", "myu": "ミュ", "myo": "ミョ",
            "rya": "リャ", "ryu": "リュ", "ryo": "リョ",
            "vu": "ヴ",
            "va": "ヴァ", "vi": "ヴィ", "ve": "ヴェ", "vo": "ヴォ",
            "wi": "ウィ", "we": "ウェ",
            "fa": "ファ", "fi": "フィ", "fe": "フェ", "fo": "フォ",
            "che": "チェ",
            "di": "ディ", "du": "ドゥ",
            "ti": "ティ", "tu": "トゥ",
            "je": "ジェ",
            "she": "シェ",
            "sakuon": "ッ",
            "pause": "ー"}

class JapaneseUtils(module.Module):
    name = "JapaneseUtils"
    disabled = False

    @command.desc("Search the readings and meanings of a Kanji")
    @command.usage("[kanji to search]", reply=True)
    @command.alias("sk")
    async def cmd_kanji(self, ctx: command.Context):
        text = ctx.input
        await ctx.respond("searching for kanji: " + text)
        async with self.bot.http.get("https://kanjiapi.dev/v1/kanji/" + text) as resp:
            try:
                json = await resp.json()
            except:
                await ctx.respond("`Something went wrong!`")
            meanings = clean(str(json['meanings']))
            on_readings = clean(str(json['on_readings']))
            kun_readings = clean(str(json['kun_readings']))
            jlpt = json['jlpt']
            await ctx.respond("• **Kanji**: " + text + "\n\n **Meanings**: `" + meanings + "`\n\n **JLPT**: `" + str(jlpt)
                  + "`\n\n **音読み**: " + on_readings + "\n\n **訓読み**: " + kun_readings)

    @command.desc("Search the readings and meanings of all Kanji in a sentence")
    @command.usage("[sentence to search for kanji in]", reply=True)
    @command.alias("ekanji", "ek")
    async def cmd_extractkanji(self, ctx: command.Context):
        text = ctx.input
        await ctx.respond("extracting kanjis from sentence...")
        kanjis = re.findall(r'[㐀-䶵一-鿋豈-頻]', text)
        meanings = []
        on_readings = []
        kun_readings = []
        jlpt = []
        result = "「**" + text + "**」ではこの漢字を見つけた:"

        for kanji in kanjis:
            async with self.bot.http.get("https://kanjiapi.dev/v1/kanji/" + kanji) as resp:
                try:
                    json = await resp.json()
                except:
                    await ctx.respond("`Something went wrong!`")
                    return
                jlpt.append(str(json['jlpt']))
                meanings.append(clean(str(json['meanings'])))
                on_readings.append(clean(str(json['on_readings'])))
                kun_readings.append(clean(str(json['kun_readings'])))

        for i in range(len(kanjis)):
            kanji = kanjis[i]
            meaning = meanings[i]

            result += "\n\n• **" + kanji + "** (JLPT: `N" + jlpt[i]  + "`)\n   `" + meaning + "`\n  **音読み**: " + on_readings[i] + "\n   **訓読み**: " + kun_readings[i]

        await ctx.respond(result)

    @command.desc("Search for kanjis used to write a word")
    @command.usage("[word to search kanji for in romaji or kana]", reply=True)
    @command.alias("fkanji", "fk")
    async def cmd_findkanji(self, ctx: command.Context):
        text = romajiToJapanese(ctx.input)
        await ctx.respond("searching for kanji to be used...")
        async with self.bot.http.get("https://kanjiapi.dev/v1/reading/" + text) as resp:
            try:
                json = await resp.json()
            except:
                await ctx.respond("`Something went wrong!`")
                return
            kanjis = []
            meanings = []
            result = "the word「**" + text + "**」can we written using the following kanji:"

        for kanji in json['main_kanji']:
            kanjis += kanji
            meanings.append(clean(str(requests.get("https://kanjiapi.dev/v1/kanji/" + kanji).json()['meanings'])))

        for i in range(len(kanjis)):
            kanji = kanjis[i]
            meaning = meanings[i]

            result += "\n\n• " + kanji + " - `" + meaning + "`"

        await ctx.respond(result)
