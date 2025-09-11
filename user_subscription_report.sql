select u.id,
       c.name as client_name,
       u.name,
       u.email,
       u.is_active,
       CASE WHEN cpf_bid_analysis.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Bid Analyses",
       CASE WHEN cpf_calendar.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Calendar",
       CASE WHEN cpf_notifications.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Daily Alerts",
       CASE WHEN cpf_drug_info.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Drug Information",
       CASE WHEN cpf_market_reports.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Market Reports",
       CASE WHEN cpf_state_reports_premium.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "State Reports (Premium)",
       CASE WHEN cpf_state_reports.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "State Reports (Standard)",
       CASE WHEN cpf_calendar_mobile.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Calendar (Mobile)",
       CASE WHEN cpf_market_share_mobile.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Market Share (Mobile)",
       CASE WHEN cpf_notifications_mobile.client_id IS NOT NULL THEN TRUE ELSE FALSE END AS "Notifications (Mobile)"
from users u
    join clients c on u.client_id = c.id
    LEFT JOIN client_premium_features cpf_bid_analysis on c.id = cpf_bid_analysis.client_id AND cpf_bid_analysis.premium_feature_id = 1
    LEFT JOIN client_premium_features cpf_calendar on c.id = cpf_calendar.client_id AND cpf_calendar.premium_feature_id = 2
    LEFT JOIN client_premium_features cpf_drug_info on c.id = cpf_drug_info.client_id AND cpf_drug_info.premium_feature_id = 3
    LEFT JOIN client_premium_features cpf_notifications on c.id = cpf_notifications.client_id AND cpf_notifications.premium_feature_id = 5
    LEFT JOIN client_premium_features cpf_state_reports on c.id = cpf_state_reports.client_id AND cpf_state_reports.premium_feature_id = 6
    LEFT JOIN client_premium_features cpf_state_reports_premium on c.id = cpf_state_reports_premium.client_id AND cpf_state_reports_premium.premium_feature_id = 7
    LEFT JOIN client_premium_features cpf_calendar_mobile on c.id = cpf_calendar_mobile.client_id AND cpf_calendar_mobile.premium_feature_id = 8
    LEFT JOIN client_premium_features cpf_notifications_mobile on c.id = cpf_notifications_mobile.client_id AND cpf_notifications_mobile.premium_feature_id = 9
    LEFT JOIN client_premium_features cpf_market_share_mobile on c.id = cpf_market_share_mobile.client_id AND cpf_market_share_mobile.premium_feature_id = 10
    LEFT JOIN client_premium_features cpf_market_reports on c.id = cpf_market_reports.client_id AND cpf_market_reports.premium_feature_id = 11
order by c.name;