import pandas
from fpdf import FPDF


df = pandas.read_csv("articles.csv", dtype={"id": str})
print(df)

class Article:

    def __init__(self, article_id):
        self.article_id = article_id
        self.name = df.loc[df["id"] == article_id,
        "name"].squeeze()
        self.price = df.loc[df["id"] == article_id,
        "price"].squeeze()

    def update_stock(self):
        """Updates the stock after user buys an article"""
        df.loc[df["id"] == self.article_id, "in stock"] = df.loc[df["id"] == self.article_id, "in stock"].squeeze() - 1
        df.to_csv("articles.csv", index=False)

    def available(self):
        """Checks if article is in stock"""
        stock = df.loc[df["id"] == self.article_id, "in stock"].squeeze()
        return stock


class Recipt:
    def __init__(self, article_object):
        self.article = article_object

    def generate_recipt(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.article.article_id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article.name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article.price}", ln=1)

        pdf.output("receipt.pdf")

article_id = input("Enter the id of the article to buy: ")
article = Article(article_id)

if article.available():
    article.update_stock()
    recipt = Recipt(article)
    recipt.generate_recipt()
else:
    print("Article not available")