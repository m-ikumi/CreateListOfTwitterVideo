# Introduction

Nice to meet you, everyone  
I'm IKUMI, a freelance engineer.  
I am Japanese and not good at English.  
All English sentences listed here are translated by "Google Translate".  
I'm sorry if there are notation or sentences that are hard to understand.  

みなさん、初めまして  
フリーランスエンジニアのIKUMIと申します。  
私は日本人で英語は得意ではありません。  
ここに記載してある英語の文章はすべて"Google翻訳"で翻訳したものです。  
分かりづらい表記や文章がありましたら申し訳ございません。  
# CreateListOfTwitterVideo

"CreateListOfTwitterVideo" is a program that searches for tweets with videos that match the specified conditions from Twitter posts, and sends the contents of the tweets to the email along with the URL of the videos.

"CreateListOfTwitterVideo"はTwitterの投稿から指定した条件に一致する動画付きのツイートを検索し、ツイートの内容を動画のURLと共にメールに送信するプログラムです。

# DEMO

Content of the sent email. 送信されるメールの内容
![demo](https://user-images.githubusercontent.com/60560534/73698325-2d24c280-4724-11ea-9ea8-e1fde1d4dad3.jpg)

Credit notation when sharing videos on Twitter. Twitterで動画を共有した際のクレジット表記
![demo2](https://user-images.githubusercontent.com/60560534/73699615-9bb74f80-4727-11ea-9494-d0cf54ecbfe1.jpg)


# Features

By using the URL of the video, you can easily share the video with your own account.  
You can share your videos in a legitimate way without downloading them, so you don't have to worry about violating your rights.  
The shared video will have a credit to identify who posted it.  
This credit is automatically added by the Twitter system, so you know that it was shared in a legitimate manner.

動画のURLを利用することにより、自分のアカウントで簡単に動画を共有することが出来ます。  
動画をダウンロードしないで正規の方法で共有することができるため、投稿者の権利を侵害する心配がありません。  
共有した動画のには誰の投稿かがわかるクレジットが付きます。  
このクレジットはTwitterのシステムが自動的に付加するものですので、正規の方法で共有されたことが分かります。

# Requirement

* Windows10
* Python3.8


* urllib3 1.25.8
* requests-oauthlib 1.3.0

# Installation

This program requires a Twitter developer API key.  
If you do not have one, register from the following address to get various keys.

本プログラムはTwitterデベロッパーAPIキーが必要です。  
持っていない場合は以下のアドレスから登録して各種キーを取得してください。

https://developer.twitter.com

This program uses Gmail to send emails.  
If you do not have one, prepare a Gmail account.

本プログラムはメールの送信にGmailを利用しています。  
持っていない場合はGmailアカウントを用意してください。

This program has been tested only on Windows 10 with Python 3.8 installed.  
I have not confirmed the operation on OS other than Windows, so I do not know if it works properly.  
If the library described in "Requirement" above is not installed in Python3.8, install it.

本プログラムはPython3.8がインストールされたWindows10でのみ動作確認しています。
Windows以外のOSでの動作確認はしていませんので正常に動作するか分かりません。
Python3.8に上記の"Requirement"に記載してあるライブラリがインストールされていない場合はインストールしてください。

If you are not sure whether it is installed, you can check it with the following command.

インストールされているか不明な場合は以下のコマンドで確認することが出来ます。
```bash
pip list
```
Each package can be installed with the following command.

それぞれのパッケージは以下のコマンドでインストールできます。

```bash
pip install urllib3
```
```bash
pip install requests-oauthlib
```

# Usage

1. Unzip the Zip file to any location.  
Zipファイルを任意の場所に解凍してください。
1. Create a shortcut of "CreateListOfTwitterVideo.bat" in the folder on the desktop.  
フォルダの中にある"CreateListOfTwitterVideo.bat"のショートカットをデスクトップに作成します。
1. Right-click the shortcut you created to open its properties.  
作成したショートカットを右クリックしてプロパティを開きます。
1. Edit the "Link" on the "Shortcut" tab as shown below.  
(The part before "CreateListOfTwitterVideo.bat" does not need to be edited. Leave a space, specify the parameters by enclosing them in double quotes in the order of Query, Result type, Count, target language.)  
In the following example, the query is "cute OR healed OR lovely OR pretty OR sweet OR ""feel better"" cat OR kitten filter:videos -filter:retweets", Result type is "3"(mixed), Count is "100", target language is "en"(English).  
Queries can contain up to 10 specifications. As you can see in the example below, if you want to search for words that contain the space "feel better", use two double quotes.  
Also, "filter: videos" targets only tweets with videos, and "-filter: retweets" specifies that retweets are not included in the search results.  
Please refer to the following pages for details on how to specify them.  
「ショートカット」タブの”リンク先”を下記の例のように編集します。  
 (CreateListOfTwitterVideo.bat"より前の部分は編集の必要はありません。スペースを1つ空けて、クエリ、検索対象、取得件数、対象の言語の順にダブルクォーテーションで括ってパラメータを指定します。)  
以下の例ではクエリに"cute OR healed OR lovely OR pretty OR sweet OR ""feel better"" cat OR kitten filter:videos -filter:retweets"、検索対象に"3"(mixed)、取得件数に"100"(100件)、対象言語に"en"(英語)を指定しています。  
クエリは最大10個の指定を含むことができます。下の例で分かる通り、"feel better"という空白を含むワードを検索対象としたい場合にはダブルクォーテーションを2個ずつ使用してください。  
また、"filter:videos"で動画付きのツイートのみを対象としていて、"-filter:retweets"はリツイートを検索結果に含まないことを指定しています。
これらの指定方法の詳細は以下のページに詳しく書いてありますので参考にしてください。  

    https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets


    ```text
    D:/**********/CreateListOfTwitterVideo.bat "cute OR healed OR lovely OR pretty OR sweet OR ""feel better"" cat OR kitten filter:videos -filter:retweets" "3" "100" "en"
    ```
1. After editing, click "Apply"-> "OK" to close the properties window.  
編集が終わったら"適用"->"OK"の順にクリックしてプロパティ・ウィンドウを閉じます。
1. Open "CreateListOfTwitterVideo.py" in the unzipped folder with a text editor.  
解凍したフォルダの中にある"CreateListOfTwitterVideo.py"をテキストエディタで開きます。  
      
      ※日本人の方は"CreateListOfTwitterVideo.py"を削除（若しくは名前を"CreateListOfTwitterVideo_backup.py"などに変更）したのち、ファイル名の先頭に"JP-"が付いた方を"JP-"を削除して使用するとプログラム内部のコメントも出力されるメールも日本語になります。
1. Enter your information in each item from the 64th line to the 76th line.  
    You will need your Gmaiil account and its password, the name of the sender of the email sent, the title of the email sent, the email address of the recipient, and the Twitter API key.  
The source address and destination address of the email can be the same.64行目から76行目までの各項目に自分の情報を入力します。  
Gmaiilアカウントとそのパスワード、送信されるメールの送信元の名前、送信されるメールのタイトル、送信先のメールアドレス、TwitterAPIのキーが必要です。  
メールの送信元アドレスと送信先アドレスは同一でも構いません。
1. When editing is completed, save it by overwriting.  
編集が完了したら上書きで保存します。
1. Double-click the shortcut you created on your desktop.  
デスクトップに作成したショートカットをダブルクリックします。
1. Two files, "list.lst" and "original.json", should have been created in the folder where the files were extracted.  
list.lst is the same as the content of the body sent by e-mail. The file original.json contains various information obtained from Twitter. This file is attached to the email as an attachment.  
If all settings are correct, an email will be sent to the email address specified as the sender.  
解凍先のフォルダに"list.lst"と"original.json"という２つのファイルが作成されているはずです。  
list.lstはメールで送信される本文の内容と同一です。また、original.jsonというファイルはTwitterから取得した各種情報が記載されたファイルです。このファイルはメールに添付ファイルとして付加されます。
全ての設定が問題なければ送信元に指定したメールアドレスにメールが送信されます。  
![demo3](https://user-images.githubusercontent.com/60560534/73703833-a4fae900-4734-11ea-9bc9-952fea3111be.jpg)

## How to share videos/動画の共有の方法

1. Double-click the URL of the video in the email to display it in the browser.  
メール内の動画のURLをダブルクリックしてブラウザで表示します。
1. When the video is displayed on Twitter, click the share button below the video.  
Twitterで動画が表示されたら動画の下にある共有ボタンをクリックします。
![how-to01](https://user-images.githubusercontent.com/60560534/73707231-4175b900-473e-11ea-9889-c37273afcfe0.jpg)
1. When the pull-down opens, click "Copy Tweet Link" at the bottom.  
プルダウンが開いたら一番下の「ツイートのリンクをコピー」をクリックします。
![how-to02](https://user-images.githubusercontent.com/60560534/73707233-4470a980-473e-11ea-87a5-58ad6cba1021.jpg)
1. Next, paste the copied URL into the new tweet field of your account.  
次に、自分のアカウントの新規ツイート欄にコピーしたURLを貼り付けます。
1. Delete the characters after "?" At the end of the pasted URL.  
貼り付けたURLの末尾の"?"以降を削除します。
![how-to04](https://user-images.githubusercontent.com/60560534/73707423-e1cbdd80-473e-11ea-88a3-62ec17454cd4.jpg)
1. Add "/video/ 1" to the end of the URL.  
URLの末尾に"/video/1"を付けます。
![how-to03](https://user-images.githubusercontent.com/60560534/73707235-46d30380-473e-11ea-9e35-52320a0b99ed.jpg)
1. If you want to add a comment or hashtag, enter it below the URL.  
コメントやハッシュタグを添えたい場合はURLの下に入力します。
1. After that, if you tweet as it is, it will be a shared tweet.  
あとはそのままツイートすれば共有ツイートとなります。

* If you copy the URL in the mail as it is, you do not need to click the share button or delete the end and add it, but in that case it is not recommended because you can not check what kind of video it is.  
※メール内のURLをそのままコピーすれば共有ボタンをクリックしたり、末尾を削除して付け加えたりする必要はありませんが、その場合はどんな動画なのか確認できませんのでおすすめしません。

# Note

* If "1" (recent) or "3" (mixed) is specified as the search target, the latest post will be included in the search target.  
The tweets resulting from the search may contain very sensitive content.  
Make sure to check the tweeted text before clicking on the video URL to open it. 

    検索対象に"1"(recent)または"3"(mixed)を指定した場合、最新の投稿が検索対象に含まれます。  
検索された結果のツイートは非常にセンシティブな内容が含まれている場合があります。  
動画のURLをクリックして開く前にツイートされた文章をよく確認するようにしてください。

# Author



* Author: IKUMI
* E-mail: info-21383789@heart-i.biz
* Site: https://heart-i.biz

# License

Copyright is not abandoned.  
Copyright is owned by IKUMI.  
However, modification and redistribution are free.  

著作権は放棄しておりません。  
著作権はIKUMIが保有しています。  
ただし、改変および再配布は自由です。