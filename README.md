# log_converter

チャットサービスのログを変換します。

現在はLINE→Slackに対応しています。

## 注意事項
* LINEのエクスポートは存在しないはずの改行が追加されることがあります。
* SlackにCSVでインポートする際、ユーザー名がアルファベットでない場合、そのユーザーのメッセージが暗黙に無視されます。
