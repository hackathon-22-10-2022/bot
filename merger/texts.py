



def merge_texts(texts: list[str]) -> str:
    if len(texts) in [0, 1]:
        return "".join(texts)

    list_of_texts = []

    for text in texts:
        list_of_texts.append({'body': text.strip(), 'length': len(text)})

    sorted_list_of_texts = sorted(list_of_texts, key=lambda d: d['length'], reverse=True)

    sorted_list_of_texts[0]['body'] = "«%s»" % sorted_list_of_texts[0]['body']
    for text in sorted_list_of_texts[1:]:
        if text['body'] not in sorted_list_of_texts[0]['body']:
            sorted_list_of_texts[0]['body'] += f"\n«{text['body']}»"

    return sorted_list_of_texts[0]['body']
