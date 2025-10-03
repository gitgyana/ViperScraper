import re
from datetime import datetime


class PostScraper:
    """
    Scrapes post data including images and download links from a forum
    """

    def __init__(self, forum_name=None, forum_link=None):
        """
        Initialize host filters and data structures
        """
        self.forum_data = []
        self.img_hosts = ['pixhost.to', 'imgur.com', 'imageban.ru']
        self.file_hosts = ["rapidgator", "katfile", "subyshare", "mexa"] 
        self.img_ext = ('.jpg', '.jpeg', '.png', '.gif')
        self.vid_ext = ('.mp4', '.avi', '.mkv', '.zip', '.rar')
        self.forum_name = forum_name
        self.forum_link = forum_link

    def parse_date(self, date_text):
        """
        Parse date from post format into YYYY.MM.DD format
        """
        try:
            date_text = re.sub(r'\s+', ' ', date_text.strip())
            
            # Handle "Today,HH:MM" and "Yesterday,HH:MM"
            if 'Today' in date_text:
                today = datetime.today()
                return today.strftime('%Y.%m.%d')

            if 'Yesterday' in date_text:
                yesterday = datetime.today() - timedelta(days=1)
                return yesterday.strftime('%Y.%m.%d')

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
        Extract data and metadata from a post
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

            # Extract title, images, and download links
            bold_content = post_li.find('b')
            if bold_content:
                title_text = ''
                for content in bold_content.contents:
                    if isinstance(content, str) and content.strip():
                        title_text = content.strip()
                        break

                post_data['title'] = title_text

                post_data['img_srcs'] = []
                post_data['img_files'] = []
                post_data['downloadlinks'] = []

                img_links = bold_content.find_all('a', target='_blank')

                for link in img_links:
                    href = link.get('href', '')
                    img_tag = link.find('img')

                    is_image_host = any(domain in href for domain in self.img_hosts)
                    is_image_ext = href.endswith(self.img_ext)
                    has_img_inside = img_tag is not None

                    if is_image_host or is_image_ext or has_img_inside:
                        post_data['img_srcs'].append(href)

                        if img_tag:
                            img_src = img_tag.get('src', '')
                            if img_src:
                                post_data['img_files'].append(img_src)

                    is_file_host = any(host in href for host in self.file_hosts)
                    is_video_ext = href.endswith(self.vid_ext)
                    if is_file_host or is_video_ext:
                        post_data['downloadlinks'].append(href)

                if not post_data['img_srcs']:
                    post_data.pop('img_srcs', None)

                if not post_data['img_files']:
                    post_data.pop('img_files', None)

                if not post_data['downloadlinks']:
                    post_data.pop('downloadlinks', None)
                    
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

            posts = [
                li for li in posts_ol.find_all('li', class_='postbitlegacy')
                if not (li.get('id', '').startswith('post_thanks_box_'))
            ]

            print(f"Found {len(posts)} posts on this page")

            page_data = []
            for post in posts:
                post_data = self.extract_post_data(post)
                if post_data:
                    if self.forum_name:
                        post_data['forum_name'] = self.forum_name

                    if self.forum_link:
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
