# Django Blog 實作
## 簡介
一個以 Django 為基礎開發的部落格系統，實作完整的用戶管理與文章 CRUD 功能。
本專案旨在熟悉 Django 框架的 MVC 架構、資料庫操作與前後端整合流程。

## 專案目標

- 練習 Django ORM 與資料庫整合
- 強化後端 CRUD 開發流程
- 掌握基本前後端整合與部署步驟

## 技術概要

- 後端框架：Django
- 資料庫：MySQL（原 SQLite 改為 MySQL，以模擬真實部署環境）
- 前端技術：Bootstrap 5、Django Template Language
- 部署平台：[PythonAnywhere](https://oove.pythonanywhere.com/)

## 主要功能

* 使用者註冊、登入、刪除帳號
* 文章新增、編輯、刪除、瀏覽
* 使用 Django Admin 後台進行資料管理
* 基於 Template Language 的頁面渲染與動態內容顯示
  
## 內容說明
 專案內容說明
 Posts 模組 (package)
 1. models.py
定義三個資料表：IpAddress、Post、Comment，並使用 django.contrib.auth.models.User 作為用戶資料表。
  - Post 模型
+ 貼文基本欄位：title、poster、image、context、post_time、slug、classification
  -其中 poster 與 User 為多對一關係。
+ IP 相關欄位：posterip 與 viewersip
+ 方法：get_viewersip_count()
  -回傳觀看過該貼文的唯一 IP 數量，用於統計瀏覽人次。

- IpAddress 模型

與 posterip 為一對一關係

與 viewersip 為多對多關係

- Comment 模型

與 Post、User 皆為多對一關係

2. forms.py

定義四個表單類別，用於處理不同功能的輸入資料。

CustomUserCreationForm

處理使用者註冊，繼承自 UserCreationForm

透過繼承與 metaclass，額外加入 Email 欄位（原始 UserCreationForm 無此欄位）

PostCreationForm / PostUpdateForm

分別用於新增與更新貼文

均繼承自 forms.ModelForm，並以 metaclass 與 Post 模型連結

CommentCreationForm

用於新增留言

同樣繼承自 forms.ModelForm 並與 Comment 模型連結

3. urls.py

定義網站主要的 URL 結構，對應到各個 views.py 中的邏輯。

路徑	說明
accounts/	使用者登入、登出、密碼變更與重設（不含註冊）
register/	使用者註冊
createposts/	建立貼文
blog/{User ID}	使用者個人部落格頁面，可進一步操作貼文 CRUD
        
   
     
       
       


