from ticket import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

#hydra -l test -P 10-million-password-list-top-1000000.txt 127.0.0.1:5000 http-get /login
#hydra -l nik -P 10-million-password-list-top-1000000.txt -s 40434 141.87.61.62 http-post-form "/login:Username=^USER^&Password=^PASS^:Username or Password wrong"