# アキくんすきカウンター
twitterにてgithubへあげる予定はあるか、と何度かリプを貰いましたのでgithubの使い方の確認や技術向上の目的を兼ねてあげさせてもらいます。  
  
 アキくんのライブ中にチャットに投稿された「アキくんすき」をカウントするプログラムです。(そのほかのアキくんに関するワードにも対応しようと思ってます)  

# やってること
channel_idで指定されたチャンネルが生放送中か判別(放送中になるまで待機)  
	↓  
放送中になったらvideoIDを取得しそこからactiveLiveChatIdを取得しチャットのデータを取り出す  
	↓  
そのデータを使ってアキくんすきコメントを探してカウント  
  
  
毎回チャットのデータを取ってくるたびに放送中であるか判別してライブ終了と共にプログラムが終了します(そうなってるはず)  
aki-suki-counter.pyの他にcredentials_pathへ認証情報のファイルを用意してそのファイル名を入れてやる必要があります。

# 製作者
[@kitune_chan_250r](https://twitter.com/kitune_chan250r)  
プログラミング初心者です、コードに対するアドバイスがめちゃくちゃ欲しいです。  
アキくん好き(決め台詞)  

