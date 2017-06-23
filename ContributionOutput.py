#!/usr/bin/python3
#!python3
#encoding:utf-8
import sys
import os.path
import subprocess
import configparser
import argparse
import web.service.github.api.v3.AuthenticationsCreator
import web.service.github.api.v3.Client
import database.src.Database
import cui.uploader.Main
import web.log.Log
import database.src.contributions.Main
import database.src.contributions.SvgCreator
import setting.Setting

class ContributionOutput:
    def __init__(self):
        pass

    def Run(self):
        parser = argparse.ArgumentParser(
            description='GitHub Contribution Get.',
        )
        parser.add_argument('-u', '--usernames', action='append')
        parser.add_argument('-o', '--output-dir')
        self.__args = parser.parse_args()

        self.__setting = setting.Setting.Setting(os.path.abspath(os.path.dirname(__file__)))
        path_dir_db = self.__setting.DbPath
#        web.log.Log.Log().Logger.debug(path_dir_db)
        
        self.__db = database.src.Database.Database(os.path.abspath(os.path.dirname(__file__)))
        self.__db.Initialize()
        
        if None is self.__args.usernames:
            self.__args.usernames = []
            for record in self.__db.Accounts['Accounts'].find():
                self.__args.usernames.append(record['Username'])
        else:
            for username in self.__args.usernames:
                if None is self.__db.Accounts['Accounts'].find_one(Username=username):
                    web.log.Log.Log().Logger.warning('指定したユーザ {0} はDBに存在しません。UserRegister.pyで登録してください。'.format(args.username))
                    return
        
        print(self.__args.usernames)
        m = database.src.contributions.Main.Main(path_dir_db)
        for username in self.__args.usernames: m.Run(username)
        s = database.src.contributions.SvgCreator.SvgCreator(path_dir_db, self.__args.usernames)
        s.Create(is_overwrite=True)


if __name__ == '__main__':
    main = ContributionOutput()
    main.Run()
