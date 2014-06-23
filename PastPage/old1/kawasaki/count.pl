#!/usr/local/bin/perl
$cnt_file="index.cnt"; 
$lock_file="index.lock";

       if ( -f $lock_file ) {
        open( IN, "$lock_file" );
        $cnt = <IN>;
       close( IN );
        $cnt ++;
} else {
        if ( -f $cnt_file ) {
                open( IN, "$cnt_file" );
                $cnt = <IN>;
                close( IN );
                $cnt ++;
        } else {$cnt=1;}

       open(OUT,">$lock_file");
       print OUT "$cnt";
       close(OUT);

       open(IN,"$lock_file");
       $cnt = <IN>;
       close( IN );
}
        open( OUT, "> $cnt_file" );
        printf OUT "%d", $cnt;
        close( OUT );
      
$_=$cnt;
while(s/^.//){
print "<IMG SRC=\"./cntimg/$&.gif\">";
}
unlink("$lock_file");
## printf "%d", $cnt;



