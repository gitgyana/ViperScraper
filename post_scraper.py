import re
from datetime import datetime


class PostScraper:
    """
    Scrapes post data including images and download links from a forum
    """

    def __init__(self, forum_name, forum_link):
        """
        Initialize host filters and data structures
        """
        self.forum_data = []
        self.img_hosts = ['pixhost.to', 'imgur.com', 'imageban.ru']
        self.file_hosts = ["rapidgator", "katfile", "subyshare", "mexa"] 
        self.img_extn = ('.jpg', '.jpeg', '.png', '.gif')
        self.vid_extn = ('.mp4', '.avi', '.mkv', '.zip', '.rar')
        self.forum_name = forum_name
        self.forum_link = forum_link

    def parse_date(self, date_text):
        """
        Parse date from post format into YYYY.MM.DD format
        """
        try:
            date_text = re.sub(r'\s+', ' ', date_text.strip())
            
            # Pattern: "30th September 2025"
            date_match = re.search(r'(\d{1,2}\w{0,2}\s+\w+\s+\d{4})', date_text)
            
            if date_match:
                date_str = date_match.group(1)
                
                date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
                
                try:
                    return datetime.strptime(date_str, '%d %B %Y').strftime('%Y.%m.%d')
                except:
                    return date_str

        except Exception as e:
            print(f"Error parsing date: {e}")

        return date_text

    def extract_post_data(self, post_li):
        """
        Extract date and postlink from a post
        """
        try:
            post_data = {}

            # Date and post link
            posthead = post_li.find('div', class_='posthead')
            if posthead:
                date_span = posthead.find('span', class_='postdate')
                if date_span:
                    date_text = date_span.get_text(strip=True)
                    post_data['date'] = self.parse_date(date_text)

                post_counter = posthead.find('a', class_='postcounter')
                if post_counter:
                    post_data['postlink'] = post_counter.get('href', '')

            return post_data

        except Exception as e:
            print(f"Error extracting post data: {e}")
            return None

    def find_posts(self, soup):
        """
        Find all posts from forum
        """
        try:
            postlist = soup.find('div', {'id': 'postlist'})
            if not postlist:
                print("No postlist found")
                return []

            posts_ol = postlist.find('ol', {'id': 'posts'})
            if not posts_ol:
                print("No posts ol found")
                return []

            posts = posts_ol.find_all('li', class_='postbitlegacy')
            print(f"Found {len(posts)} posts on this page")

            page_data = []
            for post in posts:
                post_data = self.extract_post_data(post)
                if post_data:
                    post_data['forum_name'] = self.forum_name
                    post_data['forum_link'] = self.forum_link
                    page_data.append(post_data)

            return page_data

        except Exception as e:
            print(f"Error finding posts: {e}")
            return []


def main():
    """
    Entry point for running the post scraper
    """
    scraper = PostScraper()


if __name__ == "__main__":
    main()
