from app import huey


def call_GPT_API(input_data):
    print("TO JEST MÓJ INPUT DATA")
    print(input_data)
    return ["API_CALL"]  # Tu może być błąd


@huey.task()
def enqueue_GPT_call(input_data):
    result = call_GPT_API(input_data)
    return result
