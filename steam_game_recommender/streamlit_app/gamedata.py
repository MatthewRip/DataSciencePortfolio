from bs4 import BeautifulSoup
import requests


class GameData:

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
            price = 'None'

        if price == 'None':
            try:
                price = soup.find('div', {'class': 'discount_original_price'}).text.replace(
                    '\t', '').replace('\n', '').replace('\r', ' ')
                discounted_price = soup.find('div', {'class': 'discount_final_price'}).text.replace(
                    '\t', '').replace('\n', '').replace('\r', ' ')
                discount_percent = soup.find('div', {'class': 'discount_pct'}).text.replace(
                    '\t', '').replace('\n', '').replace('\r', ' ')
            except:
                price = 'None'
                discounted_price = 'None'
                discount_percent = 'None'

            return [price, discounted_price, discount_percent]
        else:
            return [price]
