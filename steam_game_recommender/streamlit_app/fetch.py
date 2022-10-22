from bs4 import BeautifulSoup
import requests


class FetchFromWeb:

    # scrap url and return html
    def game_image(self, game_href):
        """
        Parameters
        ----------
        url : str
            hyperlink for game page 
        Return
        ------
        image url : string
        """
        html = requests.get(game_href).text
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('img', {'class': 'game_header_image_full'})

        return image['src']

    def get_price(self, game_href):
        """
        Parameters
        ----------
        url : str
            hyperlink for game page 
        Return
        ------
        price : str
        discounted_price : str
            if there is a discount 
        discount_percent : str
            if there is a discount

        """
        html = requests.get(game_href).text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            price = soup.find('div', {'class': 'game_purchase_price price'}).text.replace(
                '\t', '').replace('\n', '').replace('\r', ' ')
        except:
            price = 'erawrrr'

        if price == 'erawrrr':
            try:
                price = soup.find('div', {'class': 'discount_original_price'}).text.replace(
                    '\t', '').replace('\n', '').replace('\r', ' ')
                discounted_price = soup.find('div', {'class': 'discount_final_price'}).text.replace(
                    '\t', '').replace('\n', '').replace('\r', ' ')
                discount_percent = soup.find('div', {'class': 'discount_pct'}).text.replace(
                    '\t', '').replace('\n', '').replace('\r', ' ')
            except:
                price = 'erawrrr'
                discounted_price = 'erawrrr'
                discount_percent = 'erawrrr'

            return [price, discounted_price, discount_percent]
        else:
            return [price]

    def get_tags(self, url):
        """
        Parameters
        ----------
        url : str
            hyperlink for game page 
        Return
        ------
        user tags : str

        """
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')

        try:
            # user added tags
            user_tags = soup.find_all('a', class_='app_tag')
            tags = []
            [[tags.append(i.strip()) for i in tag] for tag in user_tags]

        except:
            print('someshit went wrong')

        return tags

    def get_name(Self,url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('div', class_='apphub_AppName').text
        return title
