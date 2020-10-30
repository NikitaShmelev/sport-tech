# frozen_string_literal: true

require 'nokogiri'
require 'curb'
require 'csv'
require 'roo'


url = 'https://dominant.by/catalog/longboardandcruiser/longbordy-i-kruizery-v-sbore/'
page_document = Nokogiri::HTML.parse(Curl.get(url).body_str)
file = Roo::Spreadsheet.open('./test.xlsx')
# print(file.sheet(0).last_column)

# (0..file.sheet(0).last_column).each do |i|
#     print(file.sheet(0).column(i))
# end
test_data = file.sheet(0).column(2).last.to_s

links = page_document.search('div.item-title a').map { |link| "https://dominant.by#{link['href']}" }
# puts links.length
for link in links

    page_document = Nokogiri::HTML.parse(Curl.get(link).body_str)
    name = page_document.search("h1#pagetitle").xpath('text()')
    current_price = page_document.search('div[@class="price font-bold font_mxs"] span.values_wrapper').xpath('text()')

    if test_data != current_price
        sheet(0).set_value(1, 5, 'TEST', nil)
    end
    puts "\nName: #{name}"
    puts "\nLink: #{link}"
    puts "current_price: #{current_price}"
    
end 
file.close()
# CSV.open("dominant.csv", 'wb') do |csv|
#     csv << %w[Name Current_Price Image_url Discription Page_url]

# end
