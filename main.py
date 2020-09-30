from bs4 import BeautifulSoup
import requests
import re

cfURL = "http://codeforces.com"
class Crawler:

    def getLink(self):
        content = requests.get(cfURL + "/problemset/page/1", params={"order": "BY_SOLVED_DESC"}).text
        soup = BeautifulSoup(content, "lxml")
        problems = soup.find_all("a", href = re.compile("/problemset/problem/.*"))
        links = [cfURL + item.attrs['href'] for item in problems[::2]]
        return links

    def down(self, url):
        content = requests.get(url).text
        statement = BeautifulSoup(content, "lxml").find("div", class_ = "problem-statement")
        title = statement.find("div", class_ = "title")
        passages = statement.find("div", class_ = None)
        passage = ''.join(item.text + "\r\n" for item in passages.find_all("p"))
        return (title.text, passage)

if __name__ == '__main__':
    c = Crawler()
    links = c.getLink()
    print(str(len(links)) + " problems found on homepage.")
    f = open("cfProblems.md", "w", encoding = "utf-8")
    for link in links[:30]:
        title, passage = c.down(link)
        f.write("# " + title + "\r\n")
        f.write(passage)
        print(title + " successfully written.")
    f.close()
