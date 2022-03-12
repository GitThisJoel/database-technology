-- (c)
SELECT  personnummer, kommunnamn
FROM    patient
JOIN    vårdakt 
USING   (personnummer)
JOIN    journalannteckning
USING   (personnummer)
JOIN    kommun
USING   (kommunnamn)
WHERE   journalannteckning.text LIKE "%inbillningssjuk%" AND 
        kommun.regionnamn LIKE "%Skåne%"
GROUP BY personnummer -- inga dubbletter! 