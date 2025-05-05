# StackSync Python Executor

This project provides a secure Python code execution API that accepts user-submitted Python code, runs it inside a sandboxed environment, and returns the output as JSON.

### 1. Test the API 

```
curl -X POST https://py-executor-cgjeeobbqq-uc.a.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main(): return {\"hello\":\"Akshay\"}"}'

```

```
curl -X POST https://py-executor-cgjeeobbqq-uc.a.run.app/execute \
  -H "Content-Type: application/json" \
  -d $'{"script": "import numpy as np\\ndef main():\\n    arr = np.arange(5)\\n    return {\\"array\\": arr.tolist()}"}'
```

### 2 Run Locally with Docker

```
docker build -t python-executor .
docker run -p 8080:8080 python-executor
```

Google Cloud run API URL: https://py-executor-cgjeeobbqq-uc.a.run.app/execute


### Website
I build a web to use this api : https://python-executor-4dcbb4.netlify.app/

here are some of the code examples can copy, paste into editor for test:

```
import numpy as np
def main():
    arr = np.array([1, 2, 3, 4, 5])
    print("hello akshay")
    return {"array": arr.tolist(), "mean": float(np.mean(arr))}
```

```
import pandas as pd
def main():
    print("Creating pandas DataFrame")
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    print(f"DataFrame:\n{df}")
    print(f"Columns: {df.columns.tolist()}")
    return {"dataframe": df.to_dict(), "columns": df.columns.tolist()}
```


```
import numpy as np
import pandas as pd
def main():
    print("Generating random numpy array")
    data = np.random.rand(3, 2)
    print(f"Random data:\n{data}")
    print("Creating pandas DataFrame")
    df = pd.DataFrame(data, columns=['X', 'Y'])
    print(f"DataFrame:\n{df}")
    total_sum = float(df.sum().sum())
    print(f"Sum of all values: {total_sum}")
    return {"random_data": df.to_dict(), "sum": total_sum}
```