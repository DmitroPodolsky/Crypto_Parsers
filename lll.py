from urllib.parse import urlparse, parse_qs

import requests

# The provided URL
url = 'https://lineascan.build/advanced-filter?fadd=0xaaa9ea898ae0b7d3805af555af3a2e3bdf06d22c&tadd=0xaaa9ea898ae0b7d3805af555af3a2e3bdf06d22c&mtd=0x379607f5%7eClaim%2c0x20b1cb6f%7eClaim+Rewards&tkn=0xaaaac83751090c6ea42379626435f805ddf54dc8&ps=100&p=2'

# Parse the URL
parsed_url = urlparse(url)

# Extract query parameters
query_params = parse_qs(parsed_url.query)

# Construct the token_params dictionary
token_params = {
    'tkn': query_params.get('tkn', [None])[0],
    'ps': query_params.get('ps', [None])[0],
    'tadd': query_params.get('tadd', [None])[0],
    'fadd': query_params.get('fadd', [None])[0],
    'mtd': query_params.get('mtd', [None])[0],
    'p': query_params.get('p', [None])[0]
}

# Print the token_params dictionary
print(token_params)

# Example of how you would use this in a requests call
# response = requests.get('https://lineascan.build/advanced-filter', params=token_params)

# # Print the response
# print(response.url)  # To verify the URL
# print(response.text)  # To see the response content
