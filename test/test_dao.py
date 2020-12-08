def test_adding_new_users_correctly(init_sqlite3_db, init_users_db_table,
                                    init_sqlite3_db_connection, return_new_users_correctly):
    # Retrieve the connection and the cursor to the "users.db" table
    dao_handler = init_sqlite3_db_connection

    # Add users to "users" table in the SQLite database
    for index, user in enumerate(return_new_users_correctly):
        # Add a user and retrieve him/her ID
        user_id = dao_handler.add_row_into_table(object=user, table_name='users')
        assert (user_id == index + 1)
