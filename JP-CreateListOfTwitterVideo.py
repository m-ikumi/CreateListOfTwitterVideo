#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
#
# プログラム名：CreateListOfTwitterVideo.py
#
# 機能
#	Twitterを検索して動画のリストを作成する
#
# 引数
#   (1)検索クエリ【必須】：検索したい語句、アカウント、ハッシュタグなど
#   (2)検索対象：[1]recent:最新のツイート [2]popular:人気のあるツイート [3]mixed:recentとpopularどちらも含む
#                初期値：3
#   (3)取得件数：100以下の整数値
#                初期値：15
#   (4)対象言語：何語のツイートを検索対象とするか（例 日本語=ja 英語=en フランス語=fr …
#                初期値：ja（日本語）
#
#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

#-------------------------------------------------
# 独自エラー用クラス定義
#-------------------------------------------------
class MyError(Exception):
	# Not_args：コマンドライン引数が無効です。
	pass

#-------------------------------------------------
# 関数名：sendmail
# 機  能：メールを送信する
# 引  数：
#   (1)送信元メールアドレス
#   (1)送信先メールアドレス
#   (1)メール本文
#-------------------------------------------------
def sendmail(from_addr, to_addrs, body_txt):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg['From'] = '{} <{}>'.format(Header(gmail_account_nm).encode(), gmail_account)
    msg['To'] = mail_to

    body = MIMEText(body_txt)
    msg.attach(body)

    #添付ファイルのMIMEタイプとファイル名を指定する
    attachment = MIMEBase(mine['type'], mine['subtype'], name = attach_file['name'])

    file = open(attach_file['path'], encoding = 'utf-8')
    attachment.set_payload(file.read())
    file.close()
    encoders.encode_base64(attachment)
    msg.attach(attachment)
    attachment.add_header('Content-Dispositon', 'attachment', filename = attach_file['name'])

    # Gmailに接続
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context())
    server.login(gmail_account, gmail_password)

    # メールの送信
    server.sendmail(from_addr, to_addrs, msg.as_string())

#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
# メイン処理
#/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
# gmailアカウント情報
gmail_account = '**********@gmail.com'   # Googleアカウント（メールアドレス）
gmail_password = '**********'            # Googleパスワード
gmail_account_nm = '**********'          # 送信元として表示される名前
subject = '**********'                   # 送信するメールのタイトル

# メールの送信先
mail_to = '**********@*****.com'         # メールの送信先アドレス

# Twetter認証キーの設定
consumer_key        = '********************'
consumer_secret     = '********************'
access_token        = '********************'
access_token_secret = '********************'

import os
import sys
import io
import shutil
import glob
import unicodedata
import datetime
import requests
from urllib.error import HTTPError
from urllib.error import URLError

# mail送信関連パッケージのロード
import smtplib, ssl
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# twitter関連パッケージのロード
import json
from requests_oauthlib import OAuth1Session

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

# コマンドライン引数
args = sys.argv

# コマンドライン引数のチェック
if not args[1]: # 検索クエリ
    raise MyError('Not_args')
else:
    q = args[1]
if not args[2]: # 検索対象
    rt = "mixed"
elif args[2] == "1":
    rt = "recent"
elif args[2] == "2":
    rt = "popular"
else:
    rt = "mixed"
if not args[3]: # 取得件数
    ct = 15
elif int(args[3]) >= 1 and int(args[3]) <= 100:
    ct = int(args[3])
else:
    ct = 15
if not args[4]: # 対象言語
    lg = "ja"
else:
    lg = args[4]

# ファイルの保存パス
path = os.path.join(os.path.abspath(os.path.dirname(__file__)))

# 共通メールデータ(MIME)の作成
mine = {'type':'application', 'subtype':'json'}
attach_file = {'name': 'original.json', 'path': path + '/original.json'}

# TwetterOAuth認証
twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)

# search/tweets API
url_search = 'https://api.twitter.com/1.1/search/tweets.json'

# 検索パラメータ
params = {'q': q, 'result_type': rt, 'count': ct, 'lang': lg}

try:
    # search/tweet API実行
    res = twitter.get(url_search, params = params)

    # レスポンスを確認
    if res.status_code == 200: # 正常
        # 実行結果読み込み(json)
        tweet = json.loads(res.text)

        # 現在日時を取得
        dt_now = datetime.datetime.now()

        # jsonダンプ出力
        with open(path + '/original.json', mode='w', encoding='utf-8') as f:
            json.dump(tweet, f, ensure_ascii=False, indent=4, separators=(',', ': '))
        # リストファイル出力
        with open(path + '/list.lst', mode='w', encoding='utf-8') as f:

            f.write(dt_now.strftime('%Y/%m/%d %H:%M:%S') + ' にチェック\n')
            f.write('検索クエリ:' +  params['q'] + '\n')
            f.write('検索対象:' +  params['result_type'] + '\n')
            f.write('取得件数:' +  str(params['count']) + '\n')
            f.write('対象言語:' +  params['lang'] + '\n')

            # ツイート単位にループ
            for post in tweet['statuses']:
                i_cnt = 0

                # エンティティ単位にループ
                for ent in post['entities']:
                    if 'media' in ent: # メディアがある場合だけ処理する
                        url = ''
                        # メディア単位にループ
                        for media in post['extended_entities']['media']:
                            # urlがあり、尚且つ動画のみ対象
                            if media['expanded_url'] != '' and media['type'] == 'video':
                                # 各種情報を書き込み
                                f.write('*************************************************\n')
                                f.write('ユーザ名：' + post['user']['name'] + '\n')
                                f.write('ツイート：' + post['text'] + '\n')
                                f.write('投稿日時：' + post['created_at'] + '\n')
                                f.write('いいね数：' + '{:,}'.format(post['favorite_count']) + '\n')
                                f.write('URL：' + media['expanded_url'] + '\n')
                                break
        file = open(path + '/list.lst', mode='r', encoding='utf-8')
        mail_body = file.read()
        file.close()

        # メール送信
        sendmail(gmail_account, mail_to, mail_body)

except MyError as e:
    tb = sys.exc_info()[2]
    if str(e.with_traceback(tb)) == 'Not_args':
        mail_body = '■■■■■ エラー発生 ■■■■■\n【コマンドライン引数が無効です。】'
        sendmail(gmail_account, mail_to, mail_body)

except Exception as e:
    import traceback
    mail_body = '■■■■■ エラー発生 ■■■■■\n【原因不明のエラーが発生しました。】\n'
    mail_body += traceback.print_exc()
    sendmail(gmail_account, mail_to, mail_body)
