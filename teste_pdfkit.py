import pdfkit

html_content = """\
<html>
                <head>
                <meta charset="UTF-8">
                </head>
                <body>
                <h4>Table: Top 10 Banking Players in Brazil</h4>
<table>
<thead>
<tr>
<th><strong>Rank</strong></th>
<th><strong>Bank Name</strong></th>
<th><strong>Detailed Profile</strong></th>
<th><strong>Relevant Context Information</strong></th>
<th><strong>Estimates of Volumes</strong></th>
<th><strong>Estimates of Revenue</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td><strong>Itaú Unibanco</strong></td>
<td>Itaú Unibanco is the largest bank in Brazil and Latin America, resulting from the merger of Banco Itaú and Unibanco in 2008. It offers a wide range of financial services including retail, wholesale, and investment banking. It is a leader in digital banking, with a significant number of online and mobile banking users[1][3][5].</td>
<td>Key brands include Itaú, Unibanco, and Itaú BBA. It has been a pioneer in sustainability, being the first Brazilian company listed in the Dow Jones Sustainability Index. Recent strategic moves include expanding digital services and investment in fintech[2][5].</td>
<td>Total assets: $439.50 billion (2023)[3]</td>
<td>Net income: Not specified, but it is one of the top profit generators in the region[5].</td>
</tr>
<tr>
<td>2</td>
<td><strong>Banco do Brasil</strong></td>
<td>Banco do Brasil is the second-largest bank in Brazil and is majority-owned by the Brazilian government. It provides a broad spectrum of financial services, including retail, commercial, and investment banking. The bank has a significant presence in the country's agricultural sector and public sector financing[1][3][5].</td>
<td>Key brands include Banco do Brasil and BB Seguros. Recent initiatives include expansion into digital banking and participation in green finance through the Green Protocol[2][5].</td>
<td>Total assets: $379.78 billion (2023)[3]</td>
<td>Net income: Not specified, but it is among the top banks in terms of profitability[5].</td>
</tr>
<tr>
<td>3</td>
<td><strong>Banco Bradesco</strong></td>
<td>Banco Bradesco is one of the largest private banks in Brazil, offering retail, commercial, and investment banking services. It has a strong presence in the insurance market through its subsidiary Bradesco Seguros. The bank is known for its extensive branch network and digital banking services[1][3][5].</td>
<td>Key brands include Bradesco and Bradesco Seguros. Recent moves include investments in fintech and digital transformation. However, it faced a drop in proceeds in recent years[5].</td>
<td>Total assets: $340.41 billion (2023)[3]</td>
<td>Net income: Approximately $4.5 billion (though this figure can vary)[5].</td>
</tr>
<tr>
<td>4</td>
<td><strong>Caixa Econômica Federal</strong></td>
<td>Caixa Econômica Federal is a state-owned bank and one of the largest financial institutions in Brazil. It specializes in housing finance, savings accounts, and social security payments. The bank is also involved in various social and economic development programs[1][3][5].</td>
<td>Key brands include Caixa and Caixa Seguros. It has been involved in several green finance initiatives and is part of the Green Protocol[2][5].</td>
<td>Total assets: $300.63 billion (2023)[3]</td>
<td>Net income: Not specified, but it is a significant player in the public sector[5].</td>
</tr>
<tr>
<td>5</td>
<td><strong>Banco Santander (Brasil)</strong></td>
<td>Banco Santander (Brasil) is the Brazilian subsidiary of the Spanish bank Santander Group. It offers a range of financial services, including retail, commercial, and investment banking. The bank has a strong presence in the corporate segment and is involved in various sustainability initiatives[1][3][5].</td>
<td>Key brands include Santander and Santander Brasil. Recent moves include digital transformation and expansion in SME lending. However, it faced some drops in proceeds recently[5].</td>
<td>Total assets: $186.41 billion (2023)[3]</td>
<td>Net income: Not specified, but it is among the top profit generators in the region[5].</td>
</tr>
<tr>
<td>6</td>
<td><strong>BTG Pactual</strong></td>
<td>BTG Pactual is a major investment bank and wealth management firm in Brazil. It has a strong presence in investment banking, asset management, and corporate lending. The bank has seen significant growth in recent years, especially in its corporate and SME lending divisions[1][5].</td>
<td>Key brands include BTG Pactual and BTG Asset Management. Recent moves include a 25% YoY increase in profitability and leadership in M&amp;A deals and equity capital markets in Brazil[5].</td>
<td>Total assets: $85.24 billion (2023)[3]</td>
<td>Net income: Approximately $2.8 billion, with a 61% growth compared to the previous period[5].</td>
</tr>
<tr>
<td>7</td>
<td><strong>Banco Safra</strong></td>
<td>Banco Safra is a private bank in Brazil, known for its strong presence in the corporate and investment banking sectors. It offers a range of financial services, including treasury, trade finance, and wealth management. The bank has a significant presence in the international market[3][5].</td>
<td>Key brands include Banco Safra and Safra Bank. Recent strategic moves include expansion in international banking and investment in digital technologies[5].</td>
<td>Total assets: $50.76 billion (2023)[3]</td>
<td>Net income: Not specified, but it is a key player in the corporate segment[5].</td>
</tr>
<tr>
<td>8</td>
<td><strong>Banco Votorantim</strong></td>
<td>Banco Votorantim is a private bank in Brazil, part of the Votorantim Group. It offers retail, commercial, and investment banking services. The bank is known for its strong presence in the agricultural sector and corporate lending[3][5].</td>
<td>Key brands include Banco Votorantim and Votorantim Asset Management. It has been involved in various sustainability initiatives and green finance projects[2][5].</td>
<td>Total assets: $23.03 billion (2023)[3]</td>
<td>Net income: Not specified, but it is a significant player in the agricultural sector[5].</td>
</tr>
<tr>
<td>9</td>
<td><strong>Banrisul</strong></td>
<td>Banrisul is a regional bank in Brazil, primarily operating in the southern states. It offers a range of financial services, including retail, commercial, and investment banking. The bank is known for its strong presence in the SME segment and agricultural financing[3][5].</td>
<td>Key brands include Banrisul and Banrisul Asset Management. Recent moves include expansion in digital banking and participation in regional economic development programs[5].</td>
<td>Total assets: $21.50 billion (2023)[3]</td>
<td>Net income: Not specified, but it is a key player in regional banking[5].</td>
</tr>
<tr>
<td>10</td>
<td><strong>Banco do Nordeste (BNB)</strong></td>
<td>Banco do Nordeste (BNB) is a regional development bank in Brazil, focusing on the northeastern states. It provides financial services to support economic development in the region, including agricultural financing and SME lending. The bank is involved in various sustainability initiatives[2][3][5].</td>
<td>Key brands include BNB and BNB Seguros. Recent initiatives include participation in green finance projects and social development programs[2][5].</td>
<td>Total assets: Not specified among the top 10, but significant in regional terms</td>
<td>Net income: Not specified, but it is a crucial player in regional economic development[5].</td>
</tr>
</tbody>
</table>
<h3>References:</h3>
<ul>
<li>[1] https://www.spglobal.com/market-intelligence/en/news-insights/research/latin-americas-30-largest-banks-by-assets-2024</li>
<li>[2] https://www.giz.de/en/downloads/the-green-finance-market-emerging-in-brazil-oct-2020-final.pdf</li>
<li>[3] https://en.wikipedia.org/wiki/List_of_largest_banks_in_Latin_America</li>
<li>[5] https://www.gfmag.com/award/award-winners/worlds-best-banks-2024-latin-america/</li>
</ul>
                </body>
                </html>
"""

options = {
    'encoding': 'UTF-8',
}

pdfkit.from_string(html_content, 'test_string.pdf')
