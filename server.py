from flask import Flask, request, jsonify
from openai import OpenAI

client = OpenAI()
chatContent = [
    {
        "role": "system",
        "content": "You are a rich gangster",
    },
]
app = Flask(__name__)
from flask_cors import CORS

CORS(app)  # 启用 CORS 支持 解决跨域问题


@app.route(rule="/user", methods=["GET", "post"])
def get_user():
    if request.method == "GET":
        data = request.args.get("data")
        # 根据 user_id 执行相应的操作，例如从数据库中获取用户信息
        print("get接受数据", data)
        # 构造响应数据
        user = {"data": data, "name": "John Doe", "age": 30}
        return jsonify(user)
    
    if request.method == "POST":
        data = request.get_json()
        print("post收到的数据", data)
        chatContent.append(data)
        # print("chatContent", chatContent)
        # 构造响应数据
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chatContent,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
        )
        assistantMsg = {
            "role": "assistant",
            "content": response.choices[0].message.content,
        }
        chatContent.append(assistantMsg)
        
        print("openai返回的数据", response.choices[0].message.content)

        return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)
