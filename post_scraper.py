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


def main():
    """
    Entry point for running the post scraper
    """
    scraper = PostScraper()


if __name__ == "__main__":
    main()
