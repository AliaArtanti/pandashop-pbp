Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step.

Answer : 
> Membuat sebuah proyek Django baru. 
Pertama siapkan folder untuk proyek ini lalu buka folder tersebut di terminal. Selanjutnya buat virtual environment di folder tersebut dan download requirements.txt

> Membuat aplikasi dengan nama main pada proyek tersebut.
Install django di env dengan menjalankan perintah :
python -m pip install --upgrade pip  dan 
pip install django
Selanjutnya buat proyek pandashop (nama toko) dengan perintah : django-admin startproject pandashop .
Dan untuk membuat aplikasinya jalankan perintah : 
python manage.py startapp main

> Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
Di vscode buka file settings.py dalam folder pandashop, di bagian INSTALLED_APPS tambahkan 'main',

> Membuat model pada aplikasi main dengan nama Product dan memiliki atribut wajib
Buka file models.py di dalam folder main lalu buat class Product dan tambahkan atribut-atribut yang diperlukan beserta tipe datanya. 

> Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.
Membuat "template" dengan nama,npm dan kelas yang akan ditampilkan di main.html (web) nanti.

> Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py.
Buat file urls.py di folder main, lalu import fungsi view (show_main). Setelah itu tambahkan pemetaan path url ke list urlpatterns.

> Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
Push ke Github terlebih dahulu baru ke PWS dengan command git add . dan git commit - m "..." (menyimpan perubahan di lokal) dilanjut dengan perintah git push origin master untuk mengirim (commit) ke repository



Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.

Answer : Siklus request response django dimulai dari client yang mengirim request ke web server dan diteruskan ke WSGI yang menjadi penghubung antar server dan django. Request akan melewati middleware dan diarahkan ke urls.py agar permintaan dapat diproses, dan mengambil/menyimpan data melalui models.py (berhubungan dengan database). Setelah data diproses, view akan mengirim ke template html untuk dirender menjadi tampilan yang akan "dibungkus" oleh middleware response dan dikirim kembali ke browser sebagai halaman visual.
link canva bagan : https://www.canva.com/design/DAGygNWoaD0/nMVvas1K7AJXALUKVOPgTA/edit?utm_content=DAGygNWoaD0&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton



Jelaskan peran settings.py dalam proyek Django!

Answer : File settings.py berfungsi untuk mengontrol sebuah proyek (seperti pusat pengaturan). Di dalam file tersebut terdapat konfigurasi untuk komponen apa saja yang aktif di proyek seperti daftar aplikasi, middleware, database dan pengaturan untuk bahasa, timezone dll.



Bagaimana cara kerja migrasi database di Django?

Answer : Migrasi di django dilakukan untuk menerjemahkan perubahan pada model ke database. Perintah makemigrations yang dijalankan di terminal saat ada perubahan di models.py akan membuat file migrasi yang berisi instruksi perubahan. Setelah perintah migrate dijalankan baru intruksi tersebut dijalankan/dieksekusi oleh database. Proses ini mempermudah pengelolaan database sehingga lebih terkontrol dan versinya lebih mudah dilacak (tidak perlu menulis versinya secara manual).



Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

Answer : Dapat dikatakan django itu paket lengkap untuk pemula, karena :
- cara mengelola databasenya bisa dengan Python (ORM)  
- sudah banyak fitur bawaannya seperti sistem template, middleware (tidak perlu banyak memasang library tambahan) bahkan sistem keamanannya
- struktur MVT memudahkan dalam belajar



Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?

Answer : Instruksi sudah jelas dan mudah untuk dipahami.