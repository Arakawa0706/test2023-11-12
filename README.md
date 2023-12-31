# test2023-11-12
test2023-11-12



# サーバー故障検出プログラム ドキュメント

## 概要
このプログラムは、サーバーログから故障期間を検出し、検出された情報を表示するためのものです。

実行環境
Python 3.11.4

インストール：

% git clone https://github.com/Arakawa0706/test2023-11-12


監視ログファイル：logfile.txt
------------------------------------------------
＜確認日時＞,＜サーバアドレス＞,＜応答結果＞
-------------------------------------------------
確認日時は、YYYYMMDDhhmmssの形式。ただし、年＝YYYY（4桁の数字）、月＝MM（2桁の数字。以下同様）、日＝DD、時＝hh、分＝mm、秒＝ssである。
サーバアドレスは、ネットワークプレフィックス長付きのIPv4アドレスである。
応答結果には、pingの応答時間がミリ秒単位で記載される。ただし、タイムアウトした場合は"-"(ハイフン記号)となる。

設定ファイル　　：config.yaml

------------------------------------------------------------------------------------------------------------
setumon1.py
監視ログファイルを読み込み、故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラム。
pingがタイムアウトした場合(-)を故障とみなし、最初にタイムアウトしたときから、次にpingの応答が返るまでを故障期間とする。

実行結果例
% python setumon1.py
Server 10.20.30.1/16 is down from 2020-10-19 13:33:24 to 2020-10-19 13:33:25


------------------------------------------------------------------------------------------------------------
setumo2.py
ネットワークの状態によっては、一時的にpingがタイムアウトしても、一定期間するとpingの応答が復活することがあるため、
そのような場合はサーバの故障とみなさないようにしたもの。
N回以上連続してタイムアウトした場合にのみ故障とみなすように、なっている。
Nはconfig.yamlで設定する。

実行結果例
% python setumon2.py
Server 10.20.30.1/16 is down from 2020-10-19 13:31:26 to 2020-10-19 13:31:30


------------------------------------------------------------------------------------------------------------
setumo3.py
サーバが返すpingの応答時間が長くなる場合、サーバが過負荷状態になっていると考えられる。
直近m回の平均応答時間がtミリ秒を超えた場合は、サーバが過負荷状態になっているとし各サーバの過負荷状態となっている期間を出力できるようになっている。
m、tはconfig.yamlで設定する。

実行結果例
% python setumon3.py
Server 10.20.30.2/16 is down from 2020-10-19 13:31:25 to 2020-10-19 13:31:30
Server 10.20.30.1/16 is down from 2020-10-19 13:31:26 to 2020-10-19 13:31:30


------------------------------------------------------------------------------------------------------------
setumo4.py
ネットワーク経路にあるスイッチに障害が発生した場合、そのスイッチの配下にあるサーバの応答がすべてタイムアウトすると想定される。
あるサブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）している場合は、そのサブネット（のスイッチ）の故障とみなし
、各サブネット毎にネットワークの故障期間を出力できるようになっている。

実行結果例
 % python setumon4.py
Subnet 10.20.30 is down:
From 2020-10-19 13:31:25 to 2020-10-19 13:31:30
From 2020-10-19 13:31:26 to 2020-10-19 13:31:30


