from flask import Flask, request, jsonify
import psycopg2
import os 

app = Flask(__name__)

# conn = psycopg2.connect(
#     host='192.168.62.131',
#     port='5432',
#     database='blog_db',
#     user='blogapp',
#     password='KBaM534TMpUWTEFU'
# )
conn = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD')
)

@app.route('/users', methods=['POST'])
def create_user():
    
    # 獲取從請求中傳遞的使用者資料
    user_data = request.json

    # 在資料庫中插入新的使用者資料
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO users (name, email) VALUES (%s, %s)',
        (user_data['name'], user_data['email'])
    )

    conn.commit()
    cursor.close()

    return jsonify({'message': 'User created successfully'})


@app.route('/users/<user_id>/articles', methods=['POST'])
def create_article(user_id):
    # 獲取從請求中傳遞的文章資料
    article_data = request.json 
    
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO articles (user_id, title, content) VALUES (%s, %s, %s)',
        (user_id, article_data['title'], article_data['content'])
    )
    conn.commit()
    return jsonify({'message': 'Article created successfully'})


@app.route('/users/<user_id>/articles', methods=['GET'])

def get_user_articles(user_id):

    # 從資料庫中查詢指定使用者的文章
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM articles WHERE user_id = %s",
        (user_id,)
    )
    articles = cursor.fetchall()
    cursor.close()

    # 將查詢結果轉換為 JSON 格式回應
    article_list = []
    for article in articles:
        article_dict = {
            'id': article[0],
            'user_id': article[1],
            'title': article[2],
            'content': article[3]
        }
        article_list.append(article_dict)

    return jsonify(article_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
