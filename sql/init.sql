
CREATE SCHEMA tdk;

CREATE TABLE tdk.input_logs (
    user_id INT NOT NULL,
    remote_ip VARCHAR,
	rfc_1413 VARCHAR,
    request_time TIMESTAMP WITH TIME ZONE NOT NULL,
    request_method VARCHAR NOT NULL,
    request_path VARCHAR NOT NULL,
    http_version VARCHAR NOT NULL,
    response_code INT NOT NULL,
    content_size INT NOT NULL,
    created_on TIMESTAMP DEFAULT current_timestamp
);

-- User count and total number of request
CREATE OR REPLACE VIEW tdk.user_result AS 
SELECT COUNT(DISTINCT user_id) AS distinct_users_count,    
    COUNT(*) AS requests,    
    COUNT(CASE WHEN response_code >= 200 AND response_code < 400 THEN 1 END) AS successfull_req_count,    
    COUNT(CASE WHEN response_code >= 400 AND response_code < 500 THEN 1 END) AS client_side_error,    
    COUNT(CASE WHEN response_code >= 500 THEN 1 END) AS server_side_error,    
    created_on::date as creation_date
FROM tdk.input_logs 
GROUP BY creation_date;

-- Requests made by each  user
CREATE VIEW tdk.user_successful_request_view AS 
SELECT user_id, COUNT(*) AS requests, 
       COUNT(CASE WHEN response_code >= 200 AND response_code < 400 THEN 1 END) AS successfull_req_count,
       current_timestamp AS created_at,
       current_timestamp AS update_at
FROM tdk.input_logs 
GROUP BY user_id;