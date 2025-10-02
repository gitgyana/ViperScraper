import re
from datetime import datetime


class PostScraper:
    """
    Scrapes post data including images and download links from a forum
    """

    def __init__(self):
        """
        Initialize host filters and data structures
        """
        self.forum_data = []
        self.img_hosts = ['pixhost.to', 'imgur.com', 'imageban.ru']
        self.file_hosts = ["rapidgator", "katfile", "subyshare", "mexa"] 
        self.img_extn = ('.jpg', '.jpeg', '.png', '.gif')
        self.vid_extn = ('.mp4', '.avi', '.mkv', '.zip', '.rar')

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


def main():
    """
    Entry point for running the post scraper
    """
    scraper = PostScraper()


if __name__ == "__main__":
    main()
