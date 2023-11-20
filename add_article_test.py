import sqlite3
from sqlite3 import Error
import datetime
import os, random

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

# Function to insert an article with a screenshot into the database
def insert_article_with_screenshot(conn, headline, url, image_path):
    """
    Create a new article with a screenshot in the articles table
    :param conn: Connection object
    :param headline: Headline text
    :param url: URL of the article
    :param image_path: Path to the image file
    :return: article id
    """
    with open(image_path, 'rb') as file:
        blob_data = file.read()

    sql = '''INSERT INTO articles(headline, published_date, url, screenshot)
             VALUES(?,?,?,?)'''
    cur = conn.cursor()
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    cur.execute(sql, (headline, current_date, url, blob_data))
    conn.commit()
    return cur.lastrowid

# Function to generate a random headline
def generate_random_headline(word_count):
    words = ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
             'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
             'magna', 'aliqua', 'Ut', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
             'exercitation', 'ullamco', 'laboris', 'nisi', 'ut', 'aliquip', 'ex', 'ea',
             'commodo', 'consequat', 'Duis', 'aute', 'irure', 'dolor', 'in', 'reprehenderit',
             'in', 'voluptate', 'velit', 'esse', 'cillum', 'dolore', 'eu', 'fugiat', 'nulla',
             'pariatur', 'Excepteur', 'sint', 'occaecat', 'cupidatat', 'non', 'proident',
             'sunt', 'in', 'culpa', 'qui', 'officia', 'deserunt', 'mollit', 'anim', 'id',
             'est', 'laborum']
    return ' '.join(random.choice(words) for _ in range(word_count))

# Function to read and print articles from the database
def read_articles(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, headline, published_date, url FROM articles")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Main testing code
if __name__ == '__main__':
    database = "articles.db"
    image_path = 'images/1725569551490752556.png'  # Replace with the actual path to your image file
    url = 'http://example.com/article'

    # Ensure the image file exists
    if not os.path.exists(image_path):
        print(f"Image file {image_path} not found. Please check the file path.")
    else:
        # Create a database connection
        conn = create_connection(database)

        with conn:
            # Insert 10 randomly generated articles with images
            for _ in range(10):
                headline_word_count = random.randint(8, 12)
                random_headline = generate_random_headline(headline_word_count)
                insert_article_with_screenshot(conn, random_headline, url, image_path)

            # Read and print the articles
            print("Inserted articles:")
            read_articles(conn)