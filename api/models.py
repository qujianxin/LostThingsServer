#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import date

from django.db import models


def user_image_path(instance, filename):
    return os.path.join('./img/user_portrait/', str(instance.phone_number) + '.png')


def message_image_path(instance, filename):
    today = date.today()
    return os.path.join('./img/messages/',
                        str(today.year) + '-' + str(today.month) + '-' + str(today.day) + '/' + instance.what + '.png')


def news_image_path(instance, filename):
    today = date.today()
    return os.path.join('./img/news/', str(today.year) + '-' + str(today.month) + '-' + str(
        today.day) + '/' + str(instance.commit_person_id) + '.png')


def ambassador_image_path(instance, filename):
    return os.path.join('./img/ambassador/', filename)


class Words(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    content = models.TextField()
    to_person = models.ForeignKey('Person', related_name='words', null=True, blank=True)
    from_person = models.ForeignKey('Person', related_name='words_sended', null=True, blank=True)
    if_read = models.BooleanField(default=False)

    def __unicode__(self):
        return self.content


# 个人
class Person(models.Model):
    token = models.CharField(max_length=8, blank=True, default="")  # token验证 (允许为空)
    created = models.DateField(auto_now_add=True)  # 创建时间
    phone_number = models.CharField(max_length=11, unique=True, primary_key=True)  # 电话号码 (限制长度)
    password = models.CharField(max_length=50)  # 密码
    name = models.CharField(max_length=50)  # 昵称 (唯一)
    portrait = models.ImageField(null=True, blank=True,
                                 upload_to=user_image_path)  # 头像
    location = models.TextField()

    def __unicode__(self):
        return self.name


# 评论
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    commit_person = models.ForeignKey(Person, related_name="comments", blank=True, null=True)  # 评论人
    content = models.TextField()  # 内容
    message = models.ForeignKey('Message', null=True)
    news = models.ForeignKey('News', null=True)
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    to_person = models.ForeignKey(Person, related_name="replies")

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ("created",)


# 信息
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    what = models.CharField(max_length=4)  # 什么信息
    title = models.TextField()  # 信息标题
    time = models.DateTimeField()  # 丢失时间
    latlng = models.CharField(max_length=50)  # 经纬度
    kind = models.CharField(max_length=10)  # 丢失物品种类
    information = models.TextField()  # 丢失简介
    image1 = models.ImageField(upload_to=message_image_path, blank=True, null=True)
    image2 = models.ImageField(upload_to=message_image_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=message_image_path, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    contact_phone = models.CharField(max_length=11)  # 联系电话
    commit_person = models.ForeignKey(Person, related_name="messages", null=True, blank=True)  # 提交信息人
    comments_number = models.IntegerField(default=0)  # 评论数
    share_number = models.IntegerField(default=0)  # 分享数
    reading_number = models.IntegerField(default=0)  # 阅读量
    location = models.CharField(max_length=100)
    commit_location = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("-created",)


# 发现
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    information = models.TextField()
    image1 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    image2 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=news_image_path, blank=True, null=True)
    commit_person = models.ForeignKey(Person, related_name='news', null=True, blank=True)  # 提交信息人
    comments_number = models.IntegerField(default=0)  # 评论数
    following_number = models.IntegerField(default=0)  # 关注数
    followers = models.ManyToManyField(Person, related_name='following')
    share_number = models.IntegerField(default=0)  # 分享数
    reading_number = models.IntegerField(default=0)  # 阅读量
    created = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ("-created",)


class SystemMsg(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        ordering = ("-created",)

    def __unicode__(self):
        return self.content


class Feedback(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # 创建时间
    contact = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.content


class CampusAmbassador(models.Model):
    name = models.TextField()
    school = models.TextField()
    grade = models.TextField()
    slogan = models.TextField()
    resume = models.TextField()
    experience = models.TextField()

    def __unicode__(self):
        return self.name


# for statistics

class OpenAppRecord(models.Model):
    date = models.DateField(auto_now_add=True)
    people = models.ManyToManyField(to=Person)
    times = models.IntegerField(default=0)
    regist_times = models.IntegerField(default=0)

    class Meta:
        ordering = ("-date",)


class RecordWatcher(models.Model):
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
