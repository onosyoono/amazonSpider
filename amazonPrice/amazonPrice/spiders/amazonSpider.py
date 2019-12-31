import scrapy

class amazonSpider(scrapy.Spider):
	name = 'amazon'
	search_item_raw = input("Enter your search Keyword")
	max_page = int(input("Enter max number of pages you want to Scrape"))
	search_item = search_item_raw
	page_no = 2
	#https://www.amazon.in/s?k=laptop+mouse&ref=nb_sb_noss_2
	text_link = ''
	search_item = search_item.split(' ')
	for i in search_item:
		text_link += i+'+'
	text_link = text_link[:-1]
	link = 'https://www.amazon.in/s?k='+text_link+'&ref=nb_sb_noss_2'
	
	start_urls=[
	link
	]
	def parse(self, response):
		#searched_keyword = search_item_raw
		# item_name              .a-color-base.a-text-normal       .s-line-clamp-4
		# item_prime_i_guess   .sb_25yic0YU
		# item_current_price_2   .a-price-whole 
		# #search > div.s-desktop-width-max.s-desktop-content.sg-row > div.sg-col-20-of-24.sg-col-28-of-32.sg-col-16-of-20.sg-col.s-right-column.sg-col-32-of-36.sg-col-8-of-12.sg-col-12-of-16.sg-col-24-of-28 > div > span:nth-child(5) > div.s-result-list.s-search-results.sg-row > div:nth-child(1) > div > span > div > div > div > div
		item = response.css("div.a-section.a-spacing-medium")
		check = str(response.css(".a-size-medium:nth-child(1)::text"))
		check = check[check.find('data=')+5:]
		if check.find('No results for') != -1:
			amazonSpider.max_page = amazonSpider.page_no
		final_text = ""
		for i in item:
			item_name = i.css(".a-color-base.a-text-normal::text").extract()
			item_price = i.css(".a-price-whole::text").extract()
			item_prime_int = i.css(".a-icon-medium")
			item_prime = "Prime"
			if len(item_prime_int) == 0:
				item_prime = "Not "+item_prime
			if len(item_price) == 0:
				item_price = i.css(".a-color-price::text").extract()
			print(f'NAME: {item_name} #@for@# {item_price} #@Prime@# {item_prime}')
			final_text += f'NAME: {item_name} #@for@# {item_price} #@Prime@# {item_prime}'
		#yield {
		#'final_text' : final_text
		#}
		next_page = 'https://www.amazon.in/s?k='+amazonSpider.text_link+'&page='+str(amazonSpider.page_no)+'&qid=1577643536&ref=sr_pg_2'
		amazonSpider.page_no += 1
		if amazonSpider.page_no < amazonSpider.max_page:
			yield response.follow(next_page, callback=self.parse)
		