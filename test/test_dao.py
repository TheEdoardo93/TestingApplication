def test_adding_new_users_correctly(init_sqlite3_db, init_users_db_table,
                                    init_sqlite3_db_connection, return_new_users_correctly):
    # Retrieve the connection and the cursor to the "users.db" table
    dao_handler = init_sqlite3_db_connection

    # Add users to "users" table in the SQLite database
    for index, user in enumerate(return_new_users_correctly):
        dao_handler.add_row_into_table(object=user, table_name='users')

        # Count how many users are there in the "users.db" table
        count_rows_sql_statement = 'SELECT COUNT(*) FROM users;'
        dao_handler._cursor.execute(count_rows_sql_statement)
        n_rows = dao_handler._cursor.fetchone()[0]
        print('n_rows: {}'.format(n_rows))
        assert (n_rows == index + 1)
