SELECT
    s.name AS "State",
    s.code AS "ST",
	d.id AS "Drug ID",
    d.name AS "Product",
	COALESCE(
        string_agg(DISTINCT ct.name, ', ' ORDER BY ct.name),
        ''
    ) AS "Coverage Tag",
	c.name AS "Class",
	c.id AS "Class ID"
    
FROM state_coverages AS sc
JOIN states AS s
  ON s.id = sc.state_id
JOIN drugs AS d
  ON d.id = sc.drug_id
LEFT JOIN state_coverage_coverage_tags AS scct
  ON scct.state_coverage_id = sc.id
LEFT JOIN coverage_tags AS ct
  ON ct.id = scct.coverage_tag_id
JOIN classifications as c
  ON d.classification_id = c.id

GROUP BY
    sc.id,         -- keep rows distinct per state_coverage
    s.name,
    s.code,
    d.name,
	d.id,
	c.name,
	c.id
ORDER BY
    s.name;
