import requests, csv, re
from bs4 import BeautifulSoup
from sys import argv

filename, url, mask = argv[1], 'https://weather.com/weather/monthly/l/{zip}', '^[a-zA-Z]+'
fieldnames = ['Full Address','D1D','D1H','D1L','D2D','D2H','D2L',
              'D3D','D3H','D3L','D4D','D4H','D4L',
              'D5D','D5H','D5L','D6D','D6H','D6L',
              'D7D','D7H','D7L','D8D','D8H','D8L',
              'D9D','D9H','D9L','D10D','D10H','D10L',
              'D11D','D11H','D11L','D12D','D12H','D12L',
              'D13D','D13H','D13L','D14D','D14H','D14L',
              'D15D','D15H','D15L','D16D','D16H','D16L',
              'D17D','D17H','D17L','D18D','D18H','D18L',
              'D19D','D19H','D19L','D20D','D20H','D20L',
              'D21D','D21H','D21L','D22D','D22H','D22L',
              'D23D','D23H','D23L','D24D','D24H','D24L',
              'D25D','D25H','D25L','D26D','D26H','D26L',
              'D27D','D27H','D27L','D28D','D28H','D28L',
              'D29D','D29H','D29L','D30D','D30H','D30L',
              'D31D','D31H','D31L','D32D','D32H','D32L',
              'D33D','D33H','D33L','D34D','D34H','D34L',
              'D35D','D35H','D35L']

with open("monthly_weather_{}.csv".format(filename[:-4]),"w", encoding='utf8') as output:
    writer = csv.DictWriter(output, fieldnames = fieldnames)
    writer.writeheader()
    with open(filename, "r", encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = []
            print("Entry: {}".format(row['Full Address']))
            r = requests.get(url.format(zip=row['Full Address'][-5:]))
            soup = BeautifulSoup(r.text, 'html.parser')
            for b in soup.findAll('button'):
                if str(b).find('tempLow') > 0 and b.find:      # find all the <Button>'s that have temperature information in them.
                    data.append(str(b)[str(b).index('data-id="calendar-')+18:str(b).index('data-id="calendar-')+23].replace('"','')) # date information
                    data.append(re.sub(mask,"",b.get_text()[-6:-1])[:re.sub(mask,"",b.get_text()[-6:-1]).index("°")]) # temp high
                    data.append(re.sub(mask,"",b.get_text()[-6:-1])[re.sub(mask,"",b.get_text()[-6:-1]).index("°") + 1:]) # temp low
            writer.writerow({'Full Address': row['Full Address'], 'D1D': data[0],'D1H':data[1], 'D1L': data[2], \
                'D2D': data[3],'D2H':data[4], 'D2L': data[5], 'D3D': data[6],'D3H':data[7], 'D3L': data[8], \
                'D4D': data[9],'D4H':data[10], 'D4L': data[11], 'D5D': data[12],'D5H':data[13], 'D5L': data[14], \
                'D6D': data[15],'D6H':data[16], 'D6L': data[17], 'D7D': data[18],'D7H':data[19], 'D7L': data[20], \
                'D8D': data[21],'D8H':data[22], 'D8L': data[23], 'D9D': data[24],'D9H':data[25], 'D9L': data[26], \
                'D10D': data[27],'D10H':data[28], 'D10L': data[29], 'D11D': data[30],'D11H':data[31], 'D11L': data[32], \
                'D12D': data[33],'D12H':data[34], 'D12L': data[35], 'D13D': data[36],'D13H':data[37], 'D13L': data[38], \
                'D14D': data[39],'D14H':data[40], 'D14L': data[41], 'D15D': data[42],'D15H':data[43], 'D15L': data[44], \
                'D16D': data[45],'D16H':data[46], 'D16L': data[47], 'D17D': data[48],'D17H':data[49], 'D17L': data[50], \
                'D18D': data[51],'D18H':data[52], 'D18L': data[53],'D19D': data[54],'D19H':data[55], 'D19L': data[56], \
                'D20D': data[57],'D20H':data[58], 'D20L': data[59], 'D21D': data[60],'D21H':data[61], 'D21L': data[62], \
                'D22D': data[63],'D23H':data[64], 'D23L': data[65], 'D24D': data[66],'D24H':data[67], 'D24L': data[68], \
                'D25D': data[69],'D25H':data[70], 'D25L': data[71], 'D26D': data[72],'D26H':data[73], 'D26L': data[74], \
                'D27D': data[75],'D27H':data[76], 'D27L': data[77], 'D28D': data[78],'D28H':data[79], 'D28L': data[80], \
                'D29D': data[81],'D29H':data[82], 'D29L': data[83], 'D30D': data[84],'D30H':data[85], 'D30L': data[86], \
                'D31D': data[87],'D31H':data[88], 'D31L': data[89], 'D32D': data[90],'D32H':data[91], 'D32L': data[92], \
                'D33D': data[93],'D33H':data[94], 'D33L': data[95], 'D34D': data[96],'D34H':data[97], 'D34L': data[98], \
                'D35D': data[99],'D35H': data[100], 'D35L': data[101] }) 