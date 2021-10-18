SELECT 
	cc.country,
	cc.currency,
	er.code, 
	er.rate as "rate-eur-base",
	-- SELECT rate FROM ex_rates WHERE code = 'USD'
	(er.rate / 1.160905) as "rate-usd-base", 
	-- SELECT rate FROM ex_rates WHERE code = 'GBP'
	(er.rate / 0.84295) as "rate-gbp-base", 
	er.date	
FROM ex_rates as er
JOIN currency_codes as cc on er.code = cc.code
WHERE er.date IN (SELECT max(ex_rates.date) as max_date 
                  FROM ex_rates)
ORDER BY cc.country
