from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def amazonify(url, affiliate_tag):
    new_url = urlparse(url)

    if not new_url.netloc:
        return None

    if not "amazon.com" in new_url.netloc:
        return None

    query_dict = parse_qs(new_url[4])
    query_dict['tag'] = affiliate_tag
    new_url = (new_url.scheme, new_url.netloc, new_url.path,
               new_url.params, urlencode(query_dict, True), new_url.fragment)
    return urlunparse(new_url)


url = 'https://smile.amazon.com/Simple-Joys-Carters-Resistant-Pajamas/dp/B07CKZTX2B?ref_=Oct_DLandingS_D_2f67a6b4_60&tag=arttherapygui-20&smid=ATVPDKIKX0DER'
affiliate_tag = 'arttherapygui-20'
print(amazonify(url, affiliate_tag))
