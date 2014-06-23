#!/usr/local/bin/perl

# 外部ファイル取り込み
require './jcode.pl';
require './init.pl';

#&decode;
#&setfile;
&viewlog;

#------------#
#  記事表示  #
#------------#
sub viewlog {
	&header;
	print <<"EOM";
掲示板変更しました．<BR>
i_light.cgi → i_dlight.cgi<BR>

</body>
</html>
EOM
	exit;
}

__END__
