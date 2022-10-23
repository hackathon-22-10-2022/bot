from mongo import MongoFieldsDB


def _merge_texts(texts: list[str]) -> str:
    if len(texts) in [0, 1]:
        return "".join(texts)

    list_of_texts = []

    for text in texts:
        list_of_texts.append({"body": text.strip(), "length": len(text)})

    sorted_list_of_texts = sorted(
        list_of_texts, key=lambda d: d["length"], reverse=True
    )

    sorted_list_of_texts[0]["body"] = "«%s»" % sorted_list_of_texts[0]["body"]
    for text in sorted_list_of_texts[1:]:
        if text["body"] not in sorted_list_of_texts[0]["body"]:
            sorted_list_of_texts[0]["body"] += f"\n«{text['body']}»"

    return sorted_list_of_texts[0]["body"]


async def merge_texts(fields, answers):

    fields = await MongoFieldsDB().find_all()
    data = {}
    fields_to_search = []
    for field in fields:
        if field.get("field_type") == "text":
            fields_to_search.append(
                {"id": field.get("_id"), "field_name": field.get("field_name")}
            )

    result = {}
    for field in fields_to_search:
        answers_2 = []
        for answer in answers:
            if answer.get("to_field") == field.get("id"):
                answers_2.append(answer.get("answer"))
        print(f"{answers_2=}")
        result[field.get("field_name")] = _merge_texts(answers_2)
    return result
