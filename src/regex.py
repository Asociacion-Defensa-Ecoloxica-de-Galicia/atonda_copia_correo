import re

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

#Date: Fri, 14 Feb 2020 09:56:35 +0100
