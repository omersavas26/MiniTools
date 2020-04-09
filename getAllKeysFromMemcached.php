<?php

function getMemcachedKeys($host = '127.0.0.1', $port = 11211)
{
    $mem = @fsockopen($host, $port);
    if ($mem === FALSE) return -1;

    $r = @fwrite($mem, 'stats items' . chr(10));
    if ($r === FALSE) return -2;

    $slabs = [];
    while (($l = @fgets($mem, 1024)) !== FALSE) 
    {
        $l = trim($l);
        if ($l == 'END') break;

        $m = array();
        $r = preg_match('/^STAT\sitems\:(\d+)\:/', $l, $m);
        if ($r != 1) return -3;
        
        if(!in_array($m[1], $slabs)) array_push ($slabs, $m[1]);
    }

    $keys = [];
    foreach($slabs as $slab)
    {
        $r = @fwrite($mem, 'lru_crawler metadump '.$slab . chr(10));
        while (($l = @fgets($mem, 1024)) !== FALSE) 
        {
            $l = trim($l);
            if ($l == 'END') break;
            
            $key = explode(' ', $l);
            $key = $key[0];
            $key = substr($key, 4);
            $key = urldecode($key);
            array_push($keys, $key);
        }
     
    }
    
    @fclose($mem);
    unset($mem);

    return $keys;
}

?>