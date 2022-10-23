from mongo import MongoAnswersDB, MongoFieldsDB


async def merge_checkboxes(fields, answers):

    fields = await MongoFieldsDB().find_all()
    data = {}
    fields_to_search = []
    for field in fields:
        if field.get("field_type") == 'checkbox':
            fields_to_search.append(
                {
                    'id': field.get('_id'),
                    'field_name': field.get('field_name')
                }
            )

    for field in fields_to_search:
        values_answers = []
        for answer in answers:
            if answer.get('to_field') == field.get('id'):
                values_answers += answer.get('answer')

        data[field.get('field_name')] = set(values_answers)
    return data
