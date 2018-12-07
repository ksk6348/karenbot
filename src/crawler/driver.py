from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yaml
import time


class InstaCrawler:
    FULL_POST_SIZE = 14
    TEXT_PATH = '../../res/post.txt'

    def __init__(self, all_post_size=501):
        self.cache = []

        self.all_post_size = all_post_size

        with open('param.yml') as f:
            self.param_dict = yaml.load(f)

        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(self.param_dict['path'], options=options)
        self.driver.get(self.param_dict['url'])
        self.driver.implicitly_wait(5)

    def del_footer(self):
        del_button = self.driver.find_element_by_css_selector('#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.ctQZg > div > div > section > div > button')
        del_button.click()

    def each_post(self, col=3):
        while(len(self.cache) < self.all_post_size):
            self.scroll_to_bottom()
            time.sleep(5)
            all_post_div = self.driver.find_elements_by_css_selector('#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) > div > div')
            for div in all_post_div:
                for c in range(1, col):
                    post_img = div.find_element_by_css_selector('div:nth-child({}) > a > div.eLAPa > div.KL4Bh > img'.format(c))
                    txt = post_img.get_attribute('alt')
                    if txt not in self.cache:
                        self.cache.append(txt)
                        yield txt
                    else:
                        continue
            self.save()

    def save(self):
        with open(self.TEXT_PATH, 'a') as fw:
            for post in self.cache:
                fw.write(post)


    def scroll_to_bottom(self):
        root = self.driver.find_element_by_css_selector('#react-root > section')
        self.driver.execute_script('window.scrollTo(0, {})'.format(root.size['height']))


if __name__ == '__main__':
    c = InstaCrawler()
    c.del_footer()
    for t in c.each_post():
        print("===={}====".format(len(c.cache)))
        print(t)
    c.save()
