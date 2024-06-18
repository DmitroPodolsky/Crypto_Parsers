from bs4 import BeautifulSoup


def get_addresses(soup: BeautifulSoup) -> None:
    """Get addresses from the soup object."""
    a_tag = soup.find('td', class_="advFilterFromAddress").find('a', {'data-highlight-target': True})
    from_token_address = a_tag['data-highlight-target']
    a_tag = soup.find('td', class_="advFilterToAddress").find('a', {'data-highlight-target': True})
    to_token_address = a_tag['data-highlight-target']
    
    return from_token_address, to_token_address