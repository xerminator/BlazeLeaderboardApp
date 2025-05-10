# Normalizes non-English month names to English abbreviations
MULTILANG_MONTHS = {
    # English
    "jan": "jan", "feb": "feb", "mar": "mar", "apr": "apr", "may": "may", "jun": "jun", "jul": "jul", "aug": "aug", "sep": "sep", "oct": "oct", "nov": "nov", "dec": "dec",
    
    # Dutch (Nederlands)
    "jan": "jan", "feb": "feb", "mrt": "mar", "apr": "apr", "mei": "may", "jun": "jun", "jul": "jul", "aug": "aug", "sep": "sep", "okt": "oct", "nov": "nov", "dec": "dec",
    
    # French (Français)
    "jan": "jan", "févr": "feb", "mar": "mar", "avr": "apr", "mai": "may", "juin": "jun", "juil": "jul", "août": "aug", "sept": "sep", "oct": "oct", "nov": "nov", "déc": "dec",
    
    # German (Deutsch)
    "jan": "jan", "feb": "feb", "mär": "mar", "apr": "apr", "mai": "may", "jun": "jun", "jul": "jul", "aug": "aug", "sep": "sep", "okt": "oct", "nov": "nov", "dez": "dec",
    
    # Spanish (Español)
    "ene": "jan", "feb": "feb", "mar": "mar", "abr": "apr", "may": "may", "jun": "jun", "jul": "jul", "ago": "aug", "sep": "sep", "oct": "oct", "nov": "nov", "dic": "dec",
    
    # Italian (Italiano)
    "gen": "jan", "feb": "feb", "mar": "mar", "apr": "apr", "mag": "may", "giu": "jun", "lug": "jul", "ago": "aug", "set": "sep", "ott": "oct", "nov": "nov", "dic": "dec",
    
    # Portuguese (Português)
    "jan": "jan", "fev": "feb", "mar": "mar", "abr": "apr", "mai": "may", "jun": "jun", "jul": "jul", "ago": "aug", "set": "sep", "out": "oct", "nov": "nov", "dez": "dec",
    
    # Russian (Русский)
    "янв": "jan", "фев": "feb", "мар": "mar", "апр": "apr", "май": "may", "июн": "jun", "июл": "jul", "авг": "aug", "сен": "sep", "окт": "oct", "ноя": "nov", "дек": "dec",
    
    # Chinese (Simplified)
    "一月": "jan", "二月": "feb", "三月": "mar", "四月": "apr", "五月": "may", "六月": "jun", "七月": "jul", "八月": "aug", "九月": "sep", "十月": "oct", "十一月": "nov", "十二月": "dec",
    
    # Arabic (العربية)
    "يناير": "jan", "فبراير": "feb", "مارس": "mar", "أبريل": "apr", "مايو": "may", "يونيو": "jun", "يوليو": "jul", "أغسطس": "aug", "سبتمبر": "sep", "أكتوبر": "oct", "نوفمبر": "nov", "ديسمبر": "dec",
    
    # Hindi (हिन्दी)
    "जनवरी": "jan", "फरवरी": "feb", "मार्च": "mar", "अप्रैल": "apr", "मई": "may", "जून": "jun", "जुलाई": "jul", "अगस्त": "aug", "सितंबर": "sep", "अक्टूबर": "oct", "नवंबर": "nov", "दिसंबर": "dec",
    
    # Japanese (日本語)
    "１月": "jan", "２月": "feb", "３月": "mar", "４月": "apr", "５月": "may", "６月": "jun", "７月": "jul", "８月": "aug", "９月": "sep", "１０月": "oct", "１１月": "nov", "１２月": "dec",
    
    # Korean (한국어)
    "1월": "jan", "2월": "feb", "3월": "mar", "4월": "apr", "5월": "may", "6월": "jun", "7월": "jul", "8월": "aug", "9월": "sep", "10월": "oct", "11월": "nov", "12월": "dec",
    
    # Finnish (Suomi)
    "tam": "jan", "hel": "feb", "maa": "mar", "huhti": "apr", "tou": "may", "kes": "jun", "hei": "jul", "elo": "aug", "syy": "sep", "loka": "oct", "marras": "nov", "jou": "dec",
    
    # Swedish (Svenska)
    "jan": "jan", "feb": "feb", "mar": "mar", "apr": "apr", "maj": "may", "jun": "jun", "jul": "jul", "aug": "aug", "sep": "sep", "okt": "oct", "nov": "nov", "dec": "dec",
    
    # Greek (Ελληνικά)
    "ιαν": "jan", "φεβ": "feb", "μαρ": "mar", "απρ": "apr", "μαϊ": "may", "ιουν": "jun", "ιουλ": "jul", "αυγ": "aug", "σεπ": "sep", "οκτ": "oct", "νου": "nov", "δεκ": "dec",
    
    # Turkish (Türkçe)
    "oca": "jan", "şub": "feb", "mar": "mar", "nis": "apr", "may": "may", "haz": "jun", "tem": "jul", "ağu": "aug", "eyl": "sep", "ekim": "oct", "kas": "nov", "aralık": "dec"
}


def normalize_month(base_part):
    parts = base_part.lower().split(".")
    if parts and parts[0] in MULTILANG_MONTHS:
        parts[0] = MULTILANG_MONTHS[parts[0]]
    return ".".join(parts)
