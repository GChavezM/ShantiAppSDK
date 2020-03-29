from config import initialize_app
# import offices
import users
# import util

if __name__ == "__main__":
    print('Start')
    app = initialize_app()
    apy_key = app.options.get('apiKey')
    # print(users.get_users('admin_users', 'Trav'))
    # print(users.get_user_by_id('5xdCOp495zgw0exFEczPzP3Va8u1'))
    # key, data = users.get_user_by_name('Trav Fa Sofia')
    # print(key)
    # print(data)
