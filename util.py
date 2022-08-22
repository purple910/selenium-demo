"""
    @Time           : 2022/8/18 10:53
    @Author         : fate
    @Description    : 工具类
    @File           : util.py
"""
import os

import dotenv


def load_env_variable(key, default_value=None, none_allowed=False):
    v = os.getenv(key, default=default_value)
    if v is None and not none_allowed:
        raise RuntimeError(f"{key} returned {v} but this is not allowed!")
    return v


def get_twitter_email(env):
    return get(env, "TWITTER_EMAIL")


def get_twitter_password(env):
    return get(env, "TWITTER_PASSWORD")


def get_twitter_username(env):
    return get(env, "TWITTER_USERNAME")


def get_facebook_password(env):
    return get(env, "FACEBOOK_PASSWORD")


def get_facebook_username(env):
    return get(env, "FACEBOOK_USERNAME")


def get(env, key):
    dotenv.load_dotenv(env, verbose=True)
    return load_env_variable(key, none_allowed=True)
