<?php
/* from http://groups.google.com/group/twitter-development-talk/browse_thread/thread/1df7a2d9898d93e4 */
     $page_num = 1;
     $txtString = "";
     while ($page_num <= 10 )
     {
       $host = "http://search.twitter.com/search.atom?q=from%3Axxxx1965&page=$page_num&rpp=100";
         $result = file_get_contents($host);
         $xml = new SimpleXMLElement($result);
         foreach ($xml->entry as $entry)
         {
          echo $entry->title . "\n";
         }
       $page_num++;
     }
?> 

