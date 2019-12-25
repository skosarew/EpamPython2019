# Find files with given sha256 hash

The utility takes the path to the directory and sha256 hash as an arguments.
It goes through all the files inside the directory and displays in stdout the
absolute path to the files whose hash is specified as an argument.

## Launcing

./get_files_from_hash.py path sha256

## Define:
1) which system call will be used most often (strace):
    
    The most used system call is `read`.
    
    The full information is in the sys_calls.txt.
    
        $ sudo strace -o sys_calls.txt -c ./get_files_from_hash.py path sha256
 
 2) which part of the code is the “hottest” (profiling):
   
    The most time consuming function is `built-in method _hashlib
    .openssl_sha256`. 
    
        $ python3 -m cProfile -o profiler_out.txt path sha256
   
    To read profiler_out.txt run following in the interpreter:
    
    ```python
    import pstats
    p = pstats.Stats("profiler_out.txt")
    p.strip_dirs().sort_stats('tottime').print_stats()
    ```
    
 3) which system call consumed the most time (strace + log analysis):
     
     System call `read` consumed the most time.
     
    