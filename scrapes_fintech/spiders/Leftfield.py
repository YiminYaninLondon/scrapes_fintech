import scrapy
import pandas as pd
from decimal import Decimal, DecimalException
import math
from scrapes_fintech.scrapes_fintech.items import StableIndexPriceItem
import imaplib
import email
from io import BytesIO
from environs import Env
import re
from datetime import datetime

env = Env()
env.read_env('credentials.env')
EMAIL_USER = env('EMAIL_USER')
EMAIL_PASS = env('EMAIL_PASS')

SOURCE = 'Leftfield'
PATH_SEPARATOR = '\t'
DICT = {"Dec":"12",
        "Nov":"11",
        "Oct":"10",
        "Sep":"09",
        "Aug":"08",
        "Jul":"07",
        "Jun":"06",
        "May":"05",
        "Apr":"04",
        "Mar":"03",
        "Feb":"02",
        "Jan":"01"}

class LeftfieldSpider(scrapy.Spider):
    name = 'Leftfield'
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('inbox')
        typ, data = mail.search(None, '(HEADER FROM "chuck@leftfieldcr.com")')
        Leftfield_emails = data[0].decode('UTF-8').split()
        Leftfield_email = Leftfield_emails[-1]
        typ, message_parts = mail.fetch(Leftfield_email, '(RFC822)')
        raw_email_body = message_parts[0][1]
        email_body = email.message_from_bytes(raw_email_body)
        for email_part in email_body.walk():
            if email_part.get_content_maintype() == 'multipart':
                continue
            if email_part.get('Content-Disposition') is None:
                continue
            file_name = email_part.get_filename()
            if '.xlsx' in file_name:
                excel_file = (BytesIO(email_part.get_payload(decode=True)))
                scraped_Daily_df = pd.read_excel(excel_file, sheet_name="Daily Series", header=2)
                scraped_Weekly_df = pd.read_excel(excel_file, sheet_name="Weekly Series", header=2)
                for scraped_df in (scraped_Daily_df,scraped_Weekly_df ):
                    columns = []
                    for i in range(len(scraped_df.columns)):
                        series = (scraped_df[scraped_df.columns[i]])
                        series = '\t'.join(map(str, series[:3]))
                        columns.append(series)
                    scraped_df.columns = columns
                    scraped_df = scraped_df.iloc[3:]

                    scraped_df = scraped_df.rename(columns={'nan\tnan\tDate': 'Date'})
                    col_names = scraped_df.columns
                    for col_name in col_names:
                        if 'Date' not in col_name:
                            index_name = col_name
                            for index, row in scraped_df.iterrows():
                                date = row['Date']
                                price = row[col_name]
                                original_index_id = PATH_SEPARATOR.join([index_name])
                                if price != "NaT" and price != '0':
                                    try:
                                        price = Decimal(str(price).replace('*', '').strip())
                                        if not math.isnan(price):
                                            report_item = StableIndexPriceItem(
                                                source=SOURCE,
                                                source_url=f'Email: {file_name}',
                                                original_index_id=original_index_id,
                                                index_specification=original_index_id,
                                                published_date=date,
                                                price=price
                                                )
                                            yield report_item
                                    except DecimalException as ex:
                                        self.logger.error(f"Non decimal price of {price} "
                                                  f"found in {original_index_id}",
                                                  exc_info=ex)

