#!/usr/local/bin/perl

# �O���t�@�C����荞��
require './jcode.pl';
require './init.pl';

#&decode;
#&setfile;
&viewlog;

#------------#
#  �L���\��  #
#------------#
sub viewlog {
	&header;
	print <<"EOM";
�f���ύX���܂����D<BR>
i_light.cgi �� i_dlight.cgi<BR>

</body>
</html>
EOM
	exit;
}

__END__
