# File-transfer-program
A file transfer program using TCP and UDP Layer 4 protocols talking across an unreliable channel. It covers socket programming. Python is used to implement it. Main objective is to transfer 10 large objects and 10 small objects. The large objects will be at least 1000 times larger than the small objects.
* TCP Part: A socket application using TCP that transfers objects. A “single persistent” TCP connection will be employed. 1 large object and 1 small object is transfered consecutively in the TCP implementation.
* UDP Part: A socket application using UDP. A reliable pipelined data transport protocol that overcomes the head-of-line blocking together with the application logic is implemented. Large objects are divided into small pieces, tag those pieces and convey tagged pieces in an interleaved fashion employing a mixture of pieces from large and small objects. Main objective is to perform better than TCP.
