this script uses randomized HTTP range requests to thwart elementary packet analysis. 
given a known static web resource that includes the base64 alphabet, this script could also be used to request specific byte offsets of the resource to construct shellcode (all in memory).

for an example of repurposing byte offsets, uncomment the few lines of code that creates "the string I requested".



Note: Bro reconstructs the requested file correctly.
