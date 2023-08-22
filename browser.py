from selenium import webdriver
import time

class Browser:
    """
        A class representing a browser

        Attributes:
            name_browser (str): Name of the browser to open (e.g., "Chrome", "Edge", "Firefox").
            profile_path (str, optional): Path to the browser profile.
                If provided, the browser will open with the specified profile.
                If None, the browser will open in guest mode.

        Note:
            Supported browser names: "Chrome", "Edge", "Firefox".
            To find the profile path, go to "chrome://version" for Chrome and "about:profiles" for Firefox.

            
    """

    def __init__(self, name_browser: str):
        self.name_browser = name_browser
        self.driver = None


    def create_profile(self, num, profile_path):
        for i in range(1, num + 1):
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={profile_path}")
            options.add_argument(f"--profile-directory=Profile {i}")
            
            self.driver = webdriver.Chrome(options=options)
            time.sleep(2)

            self.driver.quit()


    def open(self, profile= "Default", profile_path = None):
        options = webdriver.ChromeOptions()
        if profile_path:
            options.add_argument(f"user-data-dir={profile_path}")
            options.add_argument(f"--profile-directory={profile}")
            
        options.add_argument("--start-maximized")
        options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=options)


    def access_website(self, url= None):
        self.driver.get(url)

    def click(self):
        self.driver.find_element()

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    profile_path = "C:\\Users\\mitin\\AppData\\Local\\Google\\Chrome\\User Data"
    A1 = Browser("Chrome")
    A1.open(profile= "TEST", profile_path= profile_path)
    A1.access_website("https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn")

