# AliExpress product parser
#
# usage: scrapy runspider ali_spider.py -o prices.json --nolog
#
# title: response.css('h1.product-name::text').extract()
# price: response.xpath('//span[contains(@id, "j-sku-price")]//text()').extract()
# price_discount: response.xpath('//span[contains(@id, "j-sku-discount-price")]//text()').extract()
# url: response.url
# category: response.css('div.breadcrumb-layout b::text').extract()
# images: response.xpath('//ul[contains(@id, "j-image-thumb-list")]''//li//img//@src').extract()
#

import scrapy
import re, sys
import urllib.request
from termcolor import colored, cprint
from ali_my.items import ParserConfig, ScrapyAliexpressItem

config  = ParserConfig()
product = ScrapyAliexpressItem()

config['items_quantity']    = 5    # crawl n links, if 0 then all of them

config['create_images']     = 0    # image creation: 1 = On, 0 = Off
config['images_output_url'] = '/Users/therealman_/Desktop/processed' # output url


class AliExSpider(scrapy.Spider):
  name = "ali"

  def start_requests(self):
    urls = [
      'https://ru.aliexpress.com/item/EKEN-H9-H9R-FHD-4-25FPS-Wi-Fi-30/32839434363.html',
      'https://ru.aliexpress.com/item/Grip-Tripods-GoPro-3-Way-Monopod-Arm-Mount-Adjustable-stand-Bracket-Handheld-Self-pole-For-Gopro/32759409248.html',
      'https://ru.aliexpress.com/item/GoPro-Aluminum-Extendable-Pole-Stick-Telescopic-Handheld-Monopod-with-Mount-Adapter-for-GoPro-Hero-4-3/32572180595.html',
      'https://ru.aliexpress.com/item/Presell-Zhiyun-SMOOTH-Q-Handheld-3-Axis-Gimbal-Portable-Stabilizer-with-Selfie-Light-for-Smartphone-Vertical/32799665540.html',
      'https://ru.aliexpress.com/item/Gopro-Accessories-2014-High-Quality-Adjustable-Camera-Head-Strap-Mount-Belt-For-SJ4000-Gopro-Hero-Camera/2039268539.html',
      'https://ru.aliexpress.com/item/Chest-Body-Strap-For-all-Gopro-Hero4-3-3-2-SJ4000-SJ5000-the-same-as-original/32430746626.html',
      'https://ru.aliexpress.com/item/Gopro-Accessories-Set-GOPRO-Bobber-Floating-Handheld-Monopod-Gopro-Accessories-For-HERO-4-3-3-2/32377424804.html',
      'https://ru.aliexpress.com/item/2015-New-Black-Shockproof-Portable-Bag-Case-For-GoPro-HD-Hero-3-3-2-1-Camera/32810322822.html',
      'https://ru.aliexpress.com/item/Portable-Shockproof-Camera-Protective-Case-Zip-Bag-for-GoPro-Hero-3-3-hero-4/32812631677.html',
      'https://ru.aliexpress.com/item/Waterproof-Shockproof-EVA-Storage-Carry-Hard-Bag-Case-Protective-Box-for-GoPro-HERO-1-2-3/32825354064.html',
      'https://ru.aliexpress.com/item/Brand-New-360-Degree-Rotation-Glove-style-Wrist-Hand-Band-Mount-Strap-For-GoPro-Hero-4/32825694833.html',
      'https://ru.aliexpress.com/item/Adjustable-45cm-19-joint-Jaws-Flex-Clamp-Mount-Neck-for-Gopro-Hero-4-3-2-1/32739852197.html',
      'https://ru.aliexpress.com/item/Jaws-Flex-Clamp-Mount-8-joint-Adjustable-Goose-Neck-for-Gopro-Hero-4-hero-3/32806852454.html',
      'https://ru.aliexpress.com/item/Black-Color-Bike-Bicycle-Motorcycle-Handlebar-Handle-Clamp-Bar-Mount-Camera-Mount-Tripod-Adapter-For-Gopro/32672154000.html',
      'https://ru.aliexpress.com/item/New-2015-Universal-Mini-Suction-Cup-Mount-Tripod-Holder-for-Car-GPS-DV-DVR-Camera-car/32657194669.html',
      'https://ru.aliexpress.com/item/Senior-360-Degree-Rotary-Backpack-Hat-Clip-Travel-Quick-Clamp-Clip-Mount-Adapter-Mini-Tripod-For/32716157591.html',
      'https://ru.aliexpress.com/item/2-In-One-Mini-Flexible-Octopus-Tripod-adapter-Bracket-Holders-Stand-for-Gopro-Hero-3-3/32668223768.html',
      'https://ru.aliexpress.com/item/92A-Sliding-Braking-wheel-8-Pcs-Lot-Original-ATS-Inline-Skates-Wheel-For-Slide-Braking/32525940239.html',
      'https://ru.aliexpress.com/item/City-Monkey-All-around-85A-FSK-Slalom-Braking-Skating-Wheel-Multi-purpose-Inline-Roller-Skates-All/32440547591.html',
      'https://ru.aliexpress.com/item/Free-Shipping-Flash-Roller-Wheels-LED-Light-Sliding-Skate-Wheels-90A-72-76-80-8-pieces/32509825685.html',
      'https://ru.aliexpress.com/item/8PCS-set-SEBA-TWINCAM-ILQ-11-Skating-Bearings-Deep-Groove-608ZZ-8X22X7mm-Chrome-Steel-Nylon-Bracket/32508187210.html',
      'https://ru.aliexpress.com/item/MagiDeal-Roller-Skate-Wheels-Accessories-Center-Bearing-Bushing-Spacer-8PCS/32600039744.html',
      'https://ru.aliexpress.com/item/8Pcs-Roller-Skates-Parts-Axle-Male-And-Female-Screws-For-Child-Kid-Or-Adult-Free-Skating/32820490178.html',
      'https://ru.aliexpress.com/item/Roller-skating-t-shirt-seba-men-women-100-cotton-short-sleeve-o-neck-t-shirts-plus/32828619742.html',
      'https://ru.aliexpress.com/item/CIP-100-Cotton-SEBA-New-Arrivals-Brand-Clothing-T-Shirt-Men-2017-Hip-Hop-Male-T/32825893780.html',
      'https://ru.aliexpress.com/item/5-4cm-New-3D-Roller-Skates-Keychain-Roller-Shoes-Key-Chains-Key-Holder-Cover-Women-Handbag/32848981200.html',
      'https://ru.aliexpress.com/item/Roller-Skates-Skating-Shoes-Pendant-Stainless-Steel-Silver-Tone-Skate-Heart-Tattoo-Wheel-Necklace-Best-Gift/32815653977.html',
      'https://ru.aliexpress.com/item/-/1000005171567.html',
      'https://ru.aliexpress.com/item/Skating-Wristband-for-Inline-Roller-Skates-Player-Soft-Silicone-Wrist-Band-with-10-colors-for-SEBA/32690967761.html',
      'https://ru.aliexpress.com/item/20pcs-Football-Training-Equipment-Stadium-Marking-Agility-training-Marker-Skating-Marking-Cones-Freestyle-Slalom-Skate-Pile/32818500586.html',
      'https://ru.aliexpress.com/item/Skates-Hook-Good-Quality-Nylon-Inline-Roller-Skates-Handle-Buckle-Hook-For-SEBA-Powerslide-Rollerblade/32533051921.html',
      'https://ru.aliexpress.com/item/Multifunctional-Roller-Skates-Shoes-Handle-Buckle-Metal-Hook-Hasps-for-Inline-Slalom-Skating-Shoes/32602211669.html',
      'https://ru.aliexpress.com/item/Frame-Protective-Cover-Waterproof-Dust-proof-Roller-Skates-Skating-Shoes-Bag-Random-Color-1pair-2Pcs/32717086382.html',
      'https://ru.aliexpress.com/item/Red-Blue-Yellow-Pink-Green-DIY-CUFF-Decorate-Suit-Kits-for-SEBA-HV-including-Braking-Block/32691120837.html',
      'https://ru.aliexpress.com/item/Original-SEBA-Skating-shoes-shoe-lace-for-HV-HL-HVG-T-KSJ-IGOR-WFSC-TRIX-Rollerblade/32440599891.html',
      'https://ru.aliexpress.com/item/Hot-Sale-Fashion-Polyester-Paisley-Reflective-Shoelaces-Ronds-Visible-Safety-Cordon-Shoe-Lace-17-Colors-120cm/32781046244.html',
    ]

    if config['items_quantity'] == 0:
      config['items_quantity'] = len(urls)

    # cprint(config['items_quantity'], 'green')

    for i in range(0, config['items_quantity']):
      pass
      yield scrapy.Request(url=urls[i], callback=self.parse)


  def parse(self, response):

    # parsing prices
    product['price_regular']     = response\
      .xpath('//span[contains(@id, "j-sku-price")]//text()')\
      .extract()
    
    product['price_low']  = response\
      .xpath('//span[contains(@itemprop, "lowPrice")]//text()')\
      .extract()

    product['price_discount'] = response\
      .xpath('//span[contains(@id, "j-sku-discount-price")]//text()')\
      .extract()
    
    # if there is a price interval "$100-$200" then use low price
    if product['price_low']: product['price_regular'] = product['price_low']

    # if there is a discount then use it
    if product['price_discount']: product['price_regular'] = product['price_discount']

    # strip ['...'] and space
    product['price_regular'] = str(product['price_regular'])\
      .replace(u'\\xa0', '')\
      .replace("['", "")\
      .replace("']", "")\
      .replace(",", ".")

    # if there is a price interval "$100-$200" then use only min value
    product['price_regular'] = re.sub("'.*","", product['price_regular'])

    # round price 123.60 to 124
    product['price_regular'] = round(int(float(product['price_regular'])))

    # debug
    cprint(product['price_regular'], 'green')
    
    # product id extract 1439489881 from link http://ali.../1439489881.html
    product['id'] = re.search("\/\d.*[^.html]", response.url).group(0)[1:]

    # product link
    product['url'] = response.url
    product['url_affilate'] = ''

    # parse images
    if config['create_images'] == 1:
      product['images_url'] = response.xpath('//ul[contains(@id, "j-image-thumb-list")]''//li//img//@src').extract()
      s = 0
      # image save
      for image in product['images_url']:
        urllib.request.urlretrieve(image[:-10], config['images_output_url'] + '/' + product['id'] + '-' + str(s) + '.jpg')
        s += 1

    # output data to JSON stream
    yield {
      'price': product['price_regular'],
      'image': product['id'],
    }