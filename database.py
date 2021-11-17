import sqlite3


class dbworker:
    def __init__(self, database_file):
        """ Констуктор """
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        """ Проверка есть ли юзер в бд """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `telegram_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def get_account(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `telegram_id` = ?', (user_id,)).fetchall()
            return result

    def get_all_users(self):
        """ Проверка есть ли юзер в бд """
        with self.connection:
            result = self.cursor.execute('SELECT `telegram_id` FROM `users`').fetchall()
            return result

    def add_user(self, telegram_username, telegram_id):
        """Добавляем нового юзера"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`telegram_username`, `telegram_id`) VALUES(?,?)",
                                       (telegram_username, telegram_id))

    def edit_sex(self, sex, telegram_id):
        """ Изменения пола """
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `sex` = ? WHERE `telegram_id` = ?',
                                (sex, telegram_id))  # True - мужчина, False - женщина

    def search(self, sex):
        """ Поиск """
        with self.connection:
            search = self.cursor.execute('SELECT `telegram_id` FROM `queue` WHERE `sex` = ?', (str(sex),)).fetchone()

            return search

    def search_random(self):
        """ Поиск """
        with self.connection:
            search = self.cursor.execute('SELECT `telegram_id` FROM `random_queue`').fetchone()

            return search

    def estimation(self, telegram_id, coin):
        with self.connection:
            self.cursor.execute('UPDATE `wallets_users` SET `money` = ? WHERE `telegram_id` = ?', (coin, telegram_id))

    def last_update(self, last, telegram_id):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `last_dialogue` = ? WHERE `telegram_id` = ?', (last, telegram_id))

    def get_last(self, telegram_id):
        with self.connection:
            result = self.cursor.execute("SELECT `last_dialogue` FROM `users` WHERE `telegram_id` = ?",
                                         (telegram_id,)).fetchall()
            return result

    def get_sex_user(self, telegram_id):
        """ Получить информацию о поле юзера по его айдишнику """
        with self.connection:
            result = self.cursor.execute('SELECT `sex` FROM `users` WHERE `telegram_id` = ?', (telegram_id,)).fetchone()
            return result

    def add_to_queue(self, telegram_id, sex):
        """ Добавление в очередь """
        with self.connection:
            self.cursor.execute("INSERT INTO `queue` (`telegram_id`, `sex`) VALUES(?,?)", (telegram_id, sex))

    def add_to_random_queue(self, telegram_id, sex):
        """ Добавление в очередь """
        with self.connection:
            self.cursor.execute("INSERT INTO `random_queue` (`telegram_id`, `sex`) VALUES(?,?)", (telegram_id, sex))

    def delete_from_queue(self, telegram_id):
        """ Функция удаляет из очереди """
        with self.connection:
            self.cursor.execute('DELETE FROM `queue` WHERE `telegram_id` = ?', (telegram_id,))

    def delete_from_random_queue(self, telegram_id):
        """ Функция удаляет из очереди """
        with self.connection:
            self.cursor.execute('DELETE FROM `random_queue` WHERE `telegram_id` = ?', (telegram_id,))

    def update_connect_with(self, connect_with, telegram_id):
        """ Обновление с кем общается пользователь """
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `connect_with` = ? WHERE `telegram_id` = ?',
                                (connect_with, telegram_id))

    def select_connect_with(self, telegram_id):
        """ Функция для получения айдишника с кем общается человек """
        with self.connection:
            return self.cursor.execute('SELECT `connect_with` FROM `users` WHERE `telegram_id` = ?',
                                       (telegram_id,)).fetchone()

    def select_connect_with_self(self, telegram_id):
        """ Функция для получения айдишника по айдишнику с кем общается человек """
        with self.connection:
            return self.cursor.execute('SELECT `telegram_id` FROM `users` WHERE `connect_with` = ?',
                                       (telegram_id,)).fetchone()

    def delete_block_user(self, connect_with, telegram_id, connect):
        with self.connection:
            self.cursor.execute('DELETE FROM `users` WHERE `telegram_id` = ?', (connect_with,))
            self.cursor.execute('UPDATE `users` SET `connect_with` = ? WHERE `telegram_id` = ?',
                                (connect, telegram_id))

    def log_msg(self, telegram_id, msg):
        """ Функция которая логирует все сообщения юзеров друг другу """
        with self.connection:
            self.cursor.execute('INSERT INTO `all_messages` (`sender`,`message`) VALUES (?,?)', (telegram_id, msg))

    def add_vk(self, telegram_id, msg):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `vk` = ? WHERE `telegram_id` = ?', (msg, telegram_id))

    def get_vk(self, telegram_id):
        with self.connection:
            return self.cursor.execute('SELECT `vk` FROM `users` WHERE `telegram_id` = ?', (telegram_id,)).fetchone()

    def add_insta(self, telegram_id, msg):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `inst` = ? WHERE `telegram_id` = ?', (msg, telegram_id))

    def get_insta(self, telegram_id):
        with self.connection:
            return self.cursor.execute('SELECT `inst` FROM `users` WHERE `telegram_id` = ?', (telegram_id,)).fetchone()

    def add_city(self, telegram_id, msg):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `city` = ? WHERE `telegram_id` = ?', (msg, telegram_id))

    def add_nickname(self, telegram_id, msg):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `nickname` = ? WHERE `telegram_id` = ?', (msg, telegram_id))

    def add_media(self, telegram_id, msg):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `media` = ? WHERE `telegram_id` = ?', (msg, telegram_id))

    def get_media(self, telegram_id):
        with self.connection:
            return self.cursor.execute('SELECT `media` FROM `users` WHERE `telegram_id` = ?', (telegram_id,)).fetchone()

    def add_admin(self, telegram_id):
        with self.connection:
            self.cursor.execute('INSERT INTO `admins` (`telegram_id`) VALUES (?)', (telegram_id,))

    def del_admin(self, telegram_id):
        with self.connection:
            self.cursor.execute('DELETE FROM `admins` WHERE `telegram_id` = ?', (telegram_id,))

    def all_admin_exists(self):
        with self.connection:
            return self.cursor.execute('SELECT `telegram_id` FROM `admins`').fetchall()

    def admin_exists(self, telegram_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `admins` WHERE `telegram_id` = ?', (telegram_id,)).fetchall()
            return bool(len(result))

    def blocked_user(self, telegram_id):
        with self.connection:
            self.cursor.execute('INSERT INTO `blocked` (`telegram_id`) VALUES (?)', (telegram_id,))

    def add_subscribtion(self, telegram_id, from_date, by_date, payment, type_sub, number_pay):
        with self.connection:
            self.cursor.execute('INSERT INTO `subscribtion` '
                                '(`id_user`,`from`,`by`,`id_payment`,`type_subscribtion`, `number_pay`) '
                                'VALUES (?,?,?,?,?,?)',
                                (telegram_id, from_date, by_date, payment, type_sub, number_pay))

    def del_subscribtion(self, telegram_id):
        with self.connection:
            self.cursor.execute('DELETE FROM `subscribtion` WHERE `id_user` = ?', (telegram_id,))

    def subscribtion_exists(self, telegram_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscribtion` WHERE `id_user` = ?', (telegram_id,)).fetchall()
            return bool(len(result))

    def by_subscribtion(self, telegram_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `subscribtion` WHERE `id_user` = ?', (telegram_id,)).fetchall()

    def unblocked_user(self, telegram_id):
        with self.connection:
            self.cursor.execute('DELETE FROM `blocked` WHERE `telegram_id` = ?', (telegram_id,))

    def blocked_exists(self, telegram_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `blocked` WHERE `telegram_id` = ?', (telegram_id,)).fetchall()
            return bool(len(result))

    def queue_exists(self, telegram_id):
        """ Функция возвращает есть ли пользователь в очереди """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `queue` WHERE `telegram_id` = ?', (telegram_id,)).fetchall()
            return bool(len(result))

    def queue_random_exists(self, telegram_id):
        """ Функция возвращает есть ли пользователь в очереди """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `random_queue` WHERE `telegram_id` = ?',
                                         (telegram_id,)).fetchall()
            return bool(len(result))

    def count_user(self):
        """вывод количества юзеров"""
        with self.connection:
            result = self.cursor.execute('SELECT COUNT(*) FROM `users`').fetchone()
            return result[0]

    def confirm(self, confirm, telegram_id):
        with self.connection:
            self.cursor.execute('UPDATE `users` SET `confirm` = ? WHERE `telegram_id` = ?', (confirm, telegram_id))

    def top_rating(self):
        """вывод топа по рейтингу"""
        with self.connection:
            return self.cursor.execute('SELECT `telegram_id` FROM `users` ORDER BY `all_msg` DESC LIMIT 5').fetchall()

    def get_name_user(self, telegram_id):
        """ Получить информацию о поле юзера по его айдишнику """
        with self.connection:
            result = self.cursor.execute('SELECT `telegram_username` FROM `users` WHERE `telegram_id` = ?',
                                         (telegram_id,)).fetchone()
            return result[0]

    def get_count_all_msg(self, telegram_id):
        """вывод количества сообщений у юзера"""
        with self.connection:
            result = self.cursor.execute('SELECT `all_msg` FROM `users` WHERE `telegram_id` = ?',
                                         (telegram_id,)).fetchone()
            return result[0]
