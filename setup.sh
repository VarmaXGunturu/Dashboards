mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme]
primaryColor="#172a3a"
backgroundColor="#172a3a"
secondaryBackgroundColor="#2bb3a0"
textColor="#ffffff"
font="monospace"
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
<<<<<<< HEAD
" >> ~/.streamlit/config.toml
=======
" > ~/.streamlit/config.toml

>>>>>>> 7bf894c (added theme)
