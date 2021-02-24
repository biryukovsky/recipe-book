install psycopg2 for macos (tested on Big Sur Intel Macbook)

```bash
$ export PATH="/usr/local/opt/libpq/bin:$PATH"
$ export LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib"
$ pip --no-cache install psycopg2
```