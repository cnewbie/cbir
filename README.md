#Tutorial

requirements:

  - python 3.4+ 
  - numpy   
  - scipy   
  - opencv3+ with contrib module (SIFT,SURF,ORB)  
  - scikit-image (uniform lbp)deprecated 
  - scikit-learn    
  - h5py    
  - tornado (web)   
  
dataset:
    put in static with test and train folder then run index.py 
```python
    cd apps
    python3 index.py 0 -m sift_vlad
```

web demo:
   ```python
        python3 services.py
   ```
   then open the url http://127.0.0.1:8888 in web browser
