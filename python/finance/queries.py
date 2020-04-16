USER_CASH_QUERY = """
    SELECT cash FROM users
    WHERE id = :user_id
"""

USER_STOCKS_QUERY = """
    SELECT symbol, company_name, SUM(shares) AS total_shares, price, SUM(total) AS total_price
    FROM contracts
    WHERE user_id = :user_id
    GROUP BY symbol
    HAVING total_shares > 0
"""

USER_STOCK_QUERY = """
    SELECT SUM(shares) AS total_shares, SUM(total) AS total_price, company_name FROM contracts
    WHERE user_id = :user_id AND symbol = :symbol
"""

CONTRACT_CREATE_QUERY = """
    INSERT INTO contracts (
        user_id,
        company_name,
        price,
        symbol,
        shares,
        total
    ) VALUES (
        :user_id,
        :company_name,
        :price,
        :symbol,
        :shares,
        :total
    )
"""

USER_UPDATE_CASH_QUERY = """
    UPDATE users
    SET cash = :cash_after_contract
    WHERE id = :user_id
"""

USER_CONTRACTS_QUERY = """
    SELECT * FROM contracts
    WHERE user_id = :user_id
    ORDER BY created_at DESC
"""

USER_QUERY = """
    SELECT * FROM users
    WHERE username = :username
"""

USER_CREATE_QUERY = """
    INSERT INTO users (username, hash)
    VALUES (:username, :password)
"""

SYMBOLS_QUERY = """
    SELECT symbol, SUM(shares) AS total_shares FROM contracts
    WHERE user_id = :user_id
    GROUP BY symbol
    HAVING total_shares > 0
"""
