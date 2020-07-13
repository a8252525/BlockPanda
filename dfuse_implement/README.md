# BlockPanda with dfuse

## build docker 

```shell=
cd [to docker folder]

docker build -t eos_lab:dfuse .
```  

```shell=
docker run -d -it -p 8180:8080/tcp -p 8181:8081/tcp -p 18080:18080/tcp --name eos eos_lab:dfuse
```

code-server will launch at port 18080.

Go to http://localhost:18080
