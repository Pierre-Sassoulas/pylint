from geoip2.database import Reader
reader = Reader('/var/lib/GeoIP/GeoLite2-City.mmdb')
response = reader.city('8.8.8.8')
country = response.country
print(type(country), country.iso_code)
