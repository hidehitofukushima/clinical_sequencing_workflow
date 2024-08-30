
from bs4 import BeautifulSoup
import requests
import csv

# HTMLページを取得します。
url = "http://www.jshem.or.jp/modules/genomgl/?ao%5B1%5D=0&sf%5B1%5D=2%2C3%2C4%2C6%2C7%2C9%2C11%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21&ss%5B1%5D=0&sq%5B1%5D=germ"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# テーブルを見つけます。
table = soup.find('table')

# TSVファイルを開きます。
with open('/Users/fukushimahideto/Desktop/clinical_sequencing_workflow/new_annotation_list/jsh_germline.tsv', 'w', newline='') as f_output:
    tsv_output = csv.writer(f_output, delimiter='\t')

    # 各行を処理します。
    for row in table.findAll('tr'):
        cols = row.findAll('td')
        if cols:
            cols = [ele.text.strip() for ele in cols]
            tsv_output.writerow(cols)
