Franken*
========
These scripts take advantage of HTTP's Range header. This header allows the pausing and resuming of downloads and uploads by browsers. Here we use it to obscure communications for thwarting traffic analysis.


frankendropper
--------------
This script will request a resource from a web server in randomly ordered chunks. First a HEAD request is made to locate the size of the resource (this could also be replaced with a GET request for the first byte). Then a series of GET requests for randomly ordered chunks of the resource are issued. The script then reconstructs the source and prints it to screen. 


frankenexfiller
---------------
This script does the opposite of frankendropper. Using PUT requests in conjunction with Content-Range headers this script opens a file, reads random chunks of the file, and PUTs them to a server.
Note: The server you configure this script to use must also be configured to support this functionality


Note: Bro reconstructs the requested file correctly.
