# srad_journal_crawler
Download srad.jp user's all journal (Nikki) into local folder.

 This program is available on Windows environment only.

 usage: srad_journal_crawler.py <user_handle_name>

 then, make folder <id>_<handle>, and start download.
 First, program downloads journal's index, and the next dowloads each contents of the journal.
 The file type is *.html, that is be browsable with web browser.
 
 (2024-2-15) ver 0.2 : 最新の10件をダウンロードできないバグを修正。

 (2024-2-16) make_journal_index.py を追加。ダウンロードが完了したフォルダ内のファイルをサーチして 各日記記事への index_local.htmlを作成します。
 
 (2024-2-20) srad_journal_crawler.py に、 friends のページをダウンロードする機能を追加。   
            日記本体がダウンロード済みならば、再ダウンロードせずに friendsページのみをダウンロードします。   
