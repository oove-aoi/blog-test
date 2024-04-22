# Django Blog 實作
## 簡介

本專題使用 Django 實作一個部落格。

## 技術概要

- 前端部分主要搭配 Bootstrap5 與 Django template language。
- 後端部分則使用 Django 與 Python，並使用 MySQL 取代原有的 SQLite。

## 部署

本專案部署到 [PythonAnywhere](http://oove.pythonanywhere.com/) 上。

## 主要功能

* 用戶創建、登入、刪除
* 文章的CRUD操作
  
## 內容說明
1. Posts
   * models.py: 定義了IpAddress、Post、Comment 三個資料表，並使用 django 內建的 User Model 來管理用戶
     - Post 內有兩種類型的欄位跟一個方法
       + 帖子基本欄位(title、poster、image、context、post_time、slug、classification)，其中 poster 跟 User為多對一關係
       + 與IP相關的欄位(posterip跟viewersip)
       + get_viewersip_count 方法回傳有看過這個帖子的人的總數(利用IP判斷)
         
     - IpAddress 與 posterip 為一對一關係、另與 viewersip 有多對多關係
     - Comment 跟 Post 與 User 為多對一關係
       
