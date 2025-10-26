import re
from email import utils, message_from_file
from typing import Optional

email_from = re.compile('From: .*<(.*)>')
email_to = re.compile('To: .*<(.*)>')
email_subject = re.compile('Subject: (.*)')
email_date = re.compile('Date: (.*)')
email_id = re.compile('Message-ID:(?: |\n)*<(.*)>')
date_year = re.compile('^Date:.* ([0-9]{4}) ')
date_month = re.compile('^Date:.* ([A-Za-z]{3}) ')
date_day = re.compile('^Date: .*, ([0-9]{2}) ')
date_hour = re.compile('^Date: .* ([0-9]{2}):')
date_minuts = re.compile('^Date: .*:([0-9]{2}):')
date_seconds = re.compile('^Date: .*:([0-9]{2}) ')
date_zone = re.compile('^Date: .*( [+-]?[0-9]{4})$')

def find_first(regex: re.Pattern[str], string: str) -> Optional[str]:
    results = regex.findall(string)
    return None if len(results) == 0 else results[0]

def find_datetime(regex, content) -> Optional[str]:
    datetime_string = find_first(regex, content)
    if datetime_string == None: return None 
    return utils.parsedate_to_datetime(datetime_string).isoformat()
