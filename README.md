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
1. Posts package
   * models.py: 定義了IpAddress、Post、Comment 三個資料表，並使用 django.contrib.auth.models 模組內的 User Model 來創建用戶資料表。
     - Post 內有兩種類型的欄位跟一個方法:
       + 貼文基本欄位(title、poster、image、context、post_time、slug、classification)，其中 poster 跟 User為多對一關係。
       + 與IP相關的欄位(posterip跟viewersip)。
       + get_viewersip_count 方法回傳有看過這個帖子的人的總數(利用IP判斷)。
         
     - IpAddress 與 posterip 為一對一關係、另與 viewersip 有多對多關係。
     - Comment 跟 Post 與 User 為多對一關係。
       
   * form.py: 定義四個表單類別，分別處理用戶創建、貼文創建、貼文更新以及留言創建等功能。
     - CustomUserCreationForm:處理用戶創建，繼承django.contrib.auth.forms 中的 UserCreationForm，並且額外加上 Email 欄位(原本 UserCreationForm 並沒有這個欄位)，最後利用元類(metaclass)的方式與 User 串聯。
     - PostCreationForm & PostUpdateForm:處理貼文創建與更新，均繼承自 forms.ModelForm 並利用元類(metaclass)與 Post 串聯。
     - CommentCreationForm:處理留言創建，繼承自 forms.ModelForm 並利用元類(metaclass)與 Comment 串聯。
       
   * urls.py: 定義了主要會使用到的網址，並與Views.py內所定義的處理邏輯相聯繫。
     - accounts/ : 與用戶相關的登錄、登出、密碼更改和密碼重置等操作的網址(不包含註冊)。
     - register/ : 用戶註冊時的網址。
     - createposts/ : 創建貼文時的網址。
     - blog/{User ID} : 以用戶Id為查詢參數之一，並附有數個子路徑可以連到貼文、更新刪除貼文或使用者的部落格。
       
   *  Views.py: 定義了數個函數處理請求
      + 檢視相關的頁面:
        - index: 首頁，會將五個瀏覽數最大的貼文顯示在首頁中。
        - classlist: 分類顯示頁，可依照所選的分類來檢視相關分類的文章，並使用 Django paginator 實現分頁閱讀功能。
      + 與用戶相關的頁面:
        - register: 處理註冊邏輯。
        - userblog: 使用 user id 查找該用戶跟他發過的貼文(依時間近排到遠)
      + 與貼文相關的頁面:
        - createpost: 處理創建貼文的邏輯，並使用 IpWare 抓取發文者IP。
        - postdetail: 使用 user id 跟 slug 查找相關貼文以及跟該貼文下的留言
          另外，當該網址使用POST method時會處理留言提交，
          並且會透過IP數據處理觀看數

        - updatepost & deletepost: 處理文章更新與刪除邏輯
         
2. 顯示頁面
   建立Base.html當作基本外型架構，並使用 Bootstrap5 所提供的 Navigation_bar.html 來當作導覽列。

   並依照需求建立用戶註冊、登入刪除，文章CRUD操作等頁面。
         
        
   
     
       
       


