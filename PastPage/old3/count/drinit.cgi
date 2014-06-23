#┌─────────────────────────────────
#│ DreamCounter v3.41
#│ drinit.cgi - 2008/03/05
#│ Copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'DreamCounter v3.41';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# [タグの書き方の例] (*** はログファイル名)
#
#  ・カウンタ <img src="http://～～/count/dream.cgi?id=***">
#  ・時刻表示 <img src="http://～～/count/dream.cgi?mode=time">
#  ・カレンダ <img src="http://～～/count/dream.cgi?mode=date">
#  ・ファイルの更新時間
#             <img src="http://～～/count/dream.cgi?file=/home/～/index.html">
#             [注意] --> /home/～/index.htmlの部分はフルパスを指定
#
#  * 応用例 (ID名を index と仮定)
#    1.画像を変更するとき：(以下はgif2ディレクトリの画像指定例)
#      <img src="http://～～/count/dream.cgi?id=index&gif=2">
#    2.数字をランダムに表示するとき：
#      <img src="http://～～/count/dream.cgi?mode=rand">
#    3.カウンタ桁数を７桁にするとき：
#      <img src="http://～～/count/dream.cgi?id=index&fig=7">
#
#  * チェックモード (mode=check という引数をつけて呼び出す）
#    http://～～/dream.cgi?mode=check
#
# [ ディレクトリ構成例 (かっこ内はパーミッション) ]
#
#  public_html / index.html(ここにカウンタ等を表示)
#       |
#       +-- count / dream.cgi  [755]
#             |     gifcat.pl  [644]
#             |     drinit.cgi [644]
#             |     drmgr.cgi  [755]
#             |
#             +-- data [777] / index.dat [666]
#             |                xxxxx.dat [666}
#             |                   :
#             |                   :
#             |
#             +-- gif1 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#             |
#             +-- gif2 / 0.gif .. 9.gif, a.gif, p.gif, c.gif, d.gif
#                  :

#-------------------------------------------------
#  ■基本設定
#-------------------------------------------------

# 管理パスワード（英数字で指定）
$pass = 'ayashi';

# IPアドレスのチェック (0=no 1=yes) 
#   → yesの場合連続したIPアドレスはカウントアップしない
$ip_chk = 1;

# ログの自動生成 (0=no 1=yes)
$id_creat = 0;

# ログを置くサーバディレクトリ
#   → 現行ディレクトリであればこのままでよい
#   → 最後は必ず / で閉じる
#   → フルパスなら / から始める（http://からではない）
$datadir = './data/';

# 他サイトからアクセスを排除
#   → 排除する   : dream.cgiを設置するURLを http://から記述
#   → 排除しない : 何も記述しない（このまま）
#   注：ただし「排除する」とした場合、設置するサーバや利用者のブラウザ
#       によっては自サイトからでもアクセスを排除する場合があります。
$base_url = "";

# 画像のあるデフォルト（初期値）のディレクトリ指定
#   → フルパスなら / から始める（http://からではない）
#   → 最後は必ず / で閉じる
$gifdir = './gif1/';

# 桁数指定の最大値（セキュリティ対策）
#   → これを超える桁数は指定しても無視されます。
$maxfig = 12;

# 画像連結ライブラリ【サーバパス】
$gifcat = './lib/gifcat.pl';

# 本体CGI【URLパス】
$dreamcgi = './dream.cgi';

# 管理CGI【URLパス】
$drmgrcgi = './drmgr.cgi';

#-------------------------------------------------
#  ■設定完了
#-------------------------------------------------

#-------------------------------------------------
#  フォームデコード
#-------------------------------------------------
sub parse_form {
	$postflag = 0;
	local($buf);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$postflag = 1;
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$buf = $ENV{'QUERY_STRING'};
	}
	undef(%in);
	foreach ( split(/&/, $buf) ) {
		local($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;

		$in{$key} = $val;
	}
	$mode = $in{'mode'};
	if ($buf) { return 1; } else { return 0; }
}

#-------------------------------------------------
#  HTMLヘッダー
#-------------------------------------------------
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>夢カウンタ</title></head>
<body>
EOM
}

#-------------------------------------------------
#  データディレクトリ検索
#-------------------------------------------------
sub datadir {
	my @dir;

	## データディレクトリ読込
	# (1) opendir関数
	if (opendir(DIR,"$datadir")) {
		@dir = readdir(DIR);
		closedir(DIR);

	# (2) chdir関数
	} else {
		my $dir = $ENV{'SCRIPT_FILENAME'};
		$dir =~ s/[^\\\/]*$//;

		chdir($datadir) || &error("Dir Error : $datadir");
		@dir = <*>;
		if ($dir[0] eq '') {
			my $ls = `ls`;
			@dir = split(/\s+/, $ls);

		}
		chdir($dir);
	}
	# ログチェック
	my @file;
	foreach (@dir) {
		if (/.+\.dat$/) { push(@file,$_); }
	}
	return @file;
}


1;

