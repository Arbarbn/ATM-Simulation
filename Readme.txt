By : Ariq (13216072) -> features.py, Khudzaifah (13216073)-> Client.py, Arba (13216079) -> cobaweb.py
Penjelasan penggunaan simulasi ATM :
1. Pada server digunakan folder server dan client digunakan folder client
2. Pada server perlu dilakukan pembuatan project terlebih dahulu yang 
berisikan file pada folder Server. 
Server
a. File utama yang digunakan yaitu cobaweb.py
b. File MySQL yang perlu dibuat berada pada file database_awal.sql
c. File IDCard_Pass.txt merupakan ringkasan user untuk Client dan Server
d. File Certificate.pem dan key.pem dibuat dengan OpenSSL direncanakan digunakan 
untuk membuat https tetapi masih terdapat kendala
e. File features.py merupakan fungsi-fungsi yang dijalankan file cobaweb.py untuk
mendukung bagian Back-end
f. Folder templates merupakan file html untuk mendukung tampilan web server
g. Untuk menjalankan file cobaweb.py harus terlebih dahulu mengatur venv dan interpreter
Python 3.7 serta mendownload library yang digunakan
h. Jika sudah dipenuhi pada g. kita dapat menjalankan file cobaweb.py
Client
a. Berisikan file Client.py untuk menjalankan GUI Client 
b. Untuk menjalankan, bisa digunakan cmd dengan cara menuju file Client.py disimpan 
kemudian pastikan sudah terinstall Python 3.7 dan jalankan di CMD dengan cara :
python Client.py
c. Tunggu hingga GUI keluar
d. Jika sudah keluar, GUI dapat dijalankan

