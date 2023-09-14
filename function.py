import os
import requests
from typing import List, Dict
import json
import openai

todo_list = []

openai.api_key = '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'

def lookup_location_id(location: str):
    response = requests.get(
        url = 'https://geoapi.qweather.com/v2/city/lookup',
        params = {
            'location': location,
            'key': '7f5fef3693144725a23091d908c1b1f1'
        },
    )
    location_id = json.loads(response.text)['location'][0]['id']
    return location_id


def get_current_weather(location: str):
    location_id = lookup_location_id(location)
    response = requests.get(
        url = 'https://devapi.qweather.com/v7/weather/now',
        params = {
            'key': '7f5fef3693144725a23091d908c1b1f1',
            'location': location_id,
        }
    )
    weather_info = json.loads(response.text)
    return f"Temperature: {weather_info['now']['feelsLike']} Description: {weather_info['now']['text']} Humidity: {weather_info['now']['humidity']}"


def add_todo(todo: str):
    global todo_list
    todo_list.append(todo)
    result = ''
    for i in range(0, len(todo_list)):
        if i != 0:
            result = result + '\n'
        result += '- ' + todo_list[i]
    return result


def function_calling(messages: List[Dict]):

    function_repository = {
        'get_current_weather': get_current_weather,
        'add_todo': add_todo,
    }

    # functions = [
    #     {
    #         'name': 'get_current_weather',
    #         'description': 'Get the current weather in a given location',
    #         'parameters': {
    #             'type': 'object',
    #             'properties': {
    #                 'location': {
    #                     'type': 'string',
    #                     'description': 'The city and state',
    #                 },
    #             },
    #             'required': 'loaction',
    #         },
    #     },
    #     {
    #         'name': 'add_todo',
    #         'description': 'Add one thing to a to-do list',
    #         'parameters': {
    #             'type': 'object',
    #             'properties': {
    #                 'todo': {
    #                     'type': 'string',
    #                     'description': 'A thing planned to be done'
    #                 },
    #             },
    #             'required': 'todo',
    #         },
    #     }
    # ]

    response = requests.post(
        'http://localhost:8080/v1/chat/completions',
        json = {
            'model': 'ggml-openllama.bin',
            'messages': messages,
            'temperature': 0.1,
            'grammar_json_functions': {
                'oneOf': [
                    {
                        'type': 'object',
                        'properties': {
                            'function': { 'const': 'get_current_weather' },
                            'arguments': {
                                'type': 'object',
                                'properties': {
                                    'location': { 'type': 'string' }
                                }
                            }
                        },
                    },
                    {
                        'type': 'object',
                        'properties': {
                            'function': { 'const': 'add_todo' },
                            'arguments': {
                                'type': 'object',
                                'properties': {
                                    'todo': { 'type': 'string' }
                                }
                            }
                        },
                    },

                ],
            },
        }
    )
    print(json.loads(response.text))
    result_list = json.loads(json.loads(response.text)['choices'][0]['message']['content'])
    # response = openai.ChatCompletion.create(
    #     model = 'ggml-openllama.bin',
    #     messages = messages,
    #     functions = functions,
    #     function_calling = 'auto',
    # )
    function_name = result_list['function']
    function_arg = result_list['arguments']
    return function_repository[function_name](**function_arg)

if __name__ == "__main__":
    # add_todo('walk')
    # print(add_todo('swim'))
    messages = [{"role": "user", "content": "What's the weather like in Beijing?"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)