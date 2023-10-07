from flask import Flask, request, jsonify
from helper.openai_api import text_completion

app = Flask(__name__)
@app.route('/your_route')
def your_route():
    result = text_completion('Call OpenAI API for text completion')

@app.route('/')
def home():
    return 'All is well...'

@app.route('/dialogflow/es/receiveMessage', methods=['POST'])
def es_receive_message():
    try:
        data = request.get_json()
        query_text = data['queryResult']['queryText']
        result = text_completion(query_text)

        if result['status'] == 1:
            return jsonify({
                'fulfillmentText': result['response']
            })
        else:
            return jsonify({
                'fulfillmentText': 'Something went wrong.'
            })

    except Exception as e:
        return jsonify({
            'fulfillmentText': f'Something went wrong. Error: {str(e)}'
        })

@app.route('/dialogflow/cx/receiveMessage', methods=['POST'])
def cx_receive_message():
    try:
        data = request.get_json()
        query_text = data['text']
        result = text_completion(query_text)

        if result['status'] == 1:
            return jsonify({
                'fulfillment_response': {
                    'messages': [
                        {
                            'text': {
                                'text': [result['response']],
                                'redactedText': [result['response']]
                            },
                            'responseType': 'HANDLER_PROMPT',
                            'source': 'VIRTUAL_AGENT'
                        }
                    ]
                }
            })
        else:
            return jsonify({
                'fulfillment_response': {
                    'messages': [
                        {
                            'text': {
                                'text': ['Something went wrong.'],
                                'redactedText': ['Something went wrong.']
                            },
                            'responseType': 'HANDLER_PROMPT',
                            'source': 'VIRTUAL_AGENT'
                        }
                    ]
                }
            })
    except Exception as e:
        return jsonify({
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': [f'Something went wrong. Error: {str(e)}'],
                            'redactedText': [f'Something went wrong. Error: {str(e)}']
                        },
                        'responseType': 'HANDLER_PROMPT',
                        'source': 'VIRTUAL_AGENT'
                    }
                ]
            }
        })

if __name__ == '__main__':
    app.run()
