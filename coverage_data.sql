SELECT
    sc.id AS "id",
    s.code AS "ST",
    d.name AS "Product",
    sc.pdl_status AS "PDL Status",
    sc.pdl_status_date as "PDL Status Date",
	c.name AS "Class",
    COALESCE(
        string_agg(DISTINCT ct.name, ', ' ORDER BY ct.name),
        ''
    ) AS "Coverage Tag(s)"
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
	c.name
ORDER BY
    s.name;
