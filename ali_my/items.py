# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserConfig(scrapy.Item):
  items_quantity = scrapy.Field()
  create_images = scrapy.Field()
  images_output_url = scrapy.Field()

class ScrapyAliexpressItem(scrapy.Item):
  id = scrapy.Field()
  title = scrapy.Field()
  category = scrapy.Field()
  price_regular = scrapy.Field()
  price_low = scrapy.Field()
  price_discount = scrapy.Field()
  options1 = scrapy.Field()
  options2 = scrapy.Field()
  item_specifics = scrapy.Field()
  packaging_details = scrapy.Field()
  images_url = scrapy.Field()
  url = scrapy.Field()
  url_affilate = scrapy.Field()
