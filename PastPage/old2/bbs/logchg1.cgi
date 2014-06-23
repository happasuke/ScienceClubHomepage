#!/usr/local/bin/perl

## light6chg.cgi (2002/09/20)
## (LightBoard v5.xx より、v6 へログ変換を行います)
## Copyright(C) Kent Web 2002
## webmaster@kent-web.com
## http://www.kent-web.com/
##
## [ 使い方 ]
## (1) light.cgi と同一ディレクトリに light6chg.cgi にテキストモード
##     で転送し、パーミッションを755に設定する。
## (2) ブラウザから light.cgi にアクセスし、「変換作業完了」の
##     メッセージが表示されれば完了。

# 旧ログ
$old = './minibbs0.dat';

# 新ログ
$new = './data0.cgi';

# 設定ファイル
$set = './light.dat';

# ---------- 作業開始 ----------

# ヘッダ出力
print "Content-type: text/html\n\n";
print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>変換ツール</title></head>
<body>
EOM

# ログ変換
open(IN,"$old") || &error("Open Error : $old");
@old = <IN>;
close(IN);

$top = shift(@old);

# 新ログへ書き込み
$no = 307;
$host ="";
$pw ="";
open(OUT,">$new") || &error("Write Error : $new");
foreach (@old) {
	($date,$nam,$eml,$com,$sub,$url) = split(/\,/);
	$com =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
		chop($hpage) if $hpage =~ /\n/;

#	($no,$date,$nam,$eml,$sub,$com,$url,$host,$pw) = split(/<>/);
#	if ($url) { $url = "http://$url"; }
	print OUT "$no<>$date<>$nam<>$eml<>$sub<>$com<>$url<>$host<>$pw<><>\n";
$no = $no -1;
}
close(OUT);

# 設定データ変換
#($head,$title,$t_col,$t_size,$t_face,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$namcol,$mail1,$mail2) = split(/<>/, $top);
#open(OUT,">$set") || &error("Write Error : $set");
#print OUT "$title<>$t_col<>24<>$t_face<>$t_img<>$bg<>$bc<>$tx<>$li<>$vl<>$al<>$home<>$max<>$subcol<>#800000<>10<>13<>$mail1<><>1<>0<>";
#close(OUT);

print <<"EOM";
変換作業完了3
</body>
</html>
EOM
exit;

# ERROR
sub error {
	print <<"EOM";
<h3>ERROR</h3>
$_[0]
</body>
</html>
EOM
	exit;
}

__END__

