def normalize(str):
    # Decodes shit that python cannot cuz it has a stroke everytime
    return str.replace("\xa0", " ").replace("Ã©", "é").replace("Ã\x89", "É").replace("Ã¨", "è").replace("Ã§", "ç")