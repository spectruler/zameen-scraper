# -*- coding: utf-8 -*
from scrapy import Spider
from scrapy.http import Request

class ZameenSpider(Spider):
    name = 'zameen'
    allowed_domains = ['zameen.com']
    start_urls = ['http://zameen.com/Homes/Karachi_DHA_Defence-213-1.html']

    def parse(self, response):
        articles = response.xpath('//li[@role="article"]')
        relative_next_page_url =  response.xpath('//a[@title="Next"]/@href').extract_first() 
        absolute_next_page_url = response.urljoin(relative_next_page_url)
        #iterate over articles 
        for article in articles:
            relative_prop_url =  article.xpath('.//div/a/@href').extract_first()  
            absolute_prop_url = response.urljoin(relative_prop_url)
            yield Request(absolute_prop_url, callback=self.parse_page,meta={'URL':absolute_prop_url})
        yield Request(absolute_next_page_url,callback=self.parse)        

    def parse_page(self,response):
        page_URL = response.meta['URL']

        #details 
        Id = response.xpath('//*[@class="c5051fb4"]/text()').extract()[-1]
        Id = [int(s) for s in Id.split() if s.isdigit()]  # only string number
        Id = Id[0]
        Zone = response.xpath('//*[@class="c5051fb4"]/text()').extract()[-2]
        Type = response.xpath(
            '//*[@aria-label="Property detail type"]/span[2]/text()'
            ).extract_first()
        Price =  response.xpath(
            '//*[@aria-label="Property detail price"]/span[2]/div/text()'
            ).extract()[-1]
        Location = response.xpath('//*[@class="b72558b0"]/div/text()').extract_first()
        Baths = response.xpath(
            '//*[@aria-label="Property detail baths"]/span[2]/text()'
            ).extract_first()
        Area = response.xpath(
            '//*[@aria-label="Property detail area"]/span[2]/span/text()'
            ).extract_first()
        Purpose = response.xpath(
            '//*[@aria-label="Property detail purpose"]/span[2]/text()'
            ).extract_first()
        Bedrooms = response.xpath(
            '//*[@aria-label="Property detail beds"]/span[2]/text()'
            ).extract_first()
        Added = response.xpath(
            '//*[@aria-label="Property creation date"]/span[2]/text()'
            ).extract_first()

        Amenities =  response.xpath('//div/ul[@class="e475b606"]')


        # parse amenities
        hasFlooring = 1 if len(Amenities.xpath('.//li/span[text()="Flooring"]')) >=1 else 0
        hasElectricityBackup = 1 if len(Amenities.xpath('.//li/span[text()="Electricity Backup"]')) >=1 else 0
        hasLift  = 1 if len(Amenities.xpath('.//li/span[text()="Elevators"]')) >=1 else 0
        hasGarden = 1 if len(Amenities.xpath('.//li/span[text()="Lawn or Garden"]')) >=1 else 0
        hasParking = 1 if len(Amenities.xpath('.//li/span[text()="Parking Spaces"]')) >=1 else 0
        hasSwimmingPool = 1 if len(Amenities.xpath('.//li/span[text()="Swimming Pool"]')) >=1 else 0
        hasJacuzzi = 1 if len(Amenities.xpath('.//li/span[text()="Jacuzzi"]')) >=1 else 0
        hasMaintenanceStaff = 1 if len(Amenities.xpath('.//li/span[text()="Maintenance Staff"]')) >=1 else 0
        hasSecurityStaff = 1 if len(Amenities.xpath('.//li/span[text()="Security Staff"]')) >=1 else 0
        
        yield   {"Id": Id,'Zone':Zone,"Type":Type,"Location":Location,
        "Baths":Baths,"Area":Area,"Purpose":Purpose,"Bedrooms":Bedrooms,
        "Added":Added,"Price":Price,
        'hasFlooring': hasFlooring,
        'hasElectricityBackup': hasElectricityBackup,
        'hasLift': hasLift,
        'hasGarden': hasGarden,
        'hasParking': hasParking,
        'hasSwimmingPool': hasSwimmingPool,
        'hasJacuzzi': hasJacuzzi,
        'hasMaintenanceStaff': hasMaintenanceStaff,
        'hasSecurityStaff': hasSecurityStaff,'URL':page_URL}

