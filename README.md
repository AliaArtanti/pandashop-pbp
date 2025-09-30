TUGAS 2

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



===========================================================================
TUGAS 3


1. Jelaskan mengapa kita memerlukan data delivery dalam pemgimplementasian sebuah platform.

Answer : Data delivery merupakan cara terstruktur untuk menyalurkan data ke antar komponen (client, server dan layanan pihak ketiga) melalui interface yang konsisten, sehingga modul yang berbeda bisa tetap “berkomunikasi”  tanpa harus bergantung dengan implementasi internalnya. 
Beberapa manfaat dari penerapan data delivery adalah arsitektur yang lebih terukur (mudah ditambahkan instance), reliable, aman dan maintenance yang mudah. Selain itu data delivery juga memungkinkan untuk sinkronisasi dalam real time agar pengalaman pengguna konsisten walaupun di perangkat yang berbeda.


2. Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

Answer : Menurut saya lebih baik JSON karena biasanya lebih sesuai/cocok untuk aplikasi web atau mobile karena lebih mudah dibaca manusia, lebih ringkas, langsung nyambung dengan tipe data JavaScript serta cepat dikonversi ke bahasa komputer (diparse). 
Sementara XML lebih cocok untuk file yang jenis teksnya bercampur-campur (seperti publishing) dan mendukung skema yang besar. Di sisi lain XML cenderung terlalu banyak pengulangan kata, sehingga parsing lebih besar dan mengakibatkan sebagian besar pertukaran data lebih berfokus pada objek atau record. 

3. Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?

Answer : Ketika form terikat dengan request, pemanggilan is_valid() bertugas untuk menjalankan semua validasi(cek syarat, tipe data) lalu melakukan cleaning & normalisasi data. Jika memenuhi semua syarat maka akan return true tetapi jika tidak memenuhi maka akan mengisi form.errors. Langkah ini harus dilakukan agar hanya data yang benar yang dipakai untuk berbagai operasi sensitif, sehingga mencegah kerusakan data, type error dan potensi munculnya celah keamanan.


4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

Answer : csrf_token adalah semacam token rahasia per-request yang dimasukkan sebagai hidden field setiap ada permintaan yang mengubah sesuatu di website. Cara kerjanya adalah middleware django akan mencocokkan token di form dengan yang disimpan di sisi pengguna, sehingga hanya request yang berasal dari halaman aplikasi pengguna saja yang diterima.

Jika tidak menyertakan token, django secara default akan menolak request dengan HTTP 403 Forbidden. Jika protection dimatikan atau diabaikan maka aplikasi akan menjadi rentan terhadap cyber attack (Cross-Site Request Forgery), penyerang dapat “menitipkan” form dari situs lain agar saat korban ingin login, browser korban akan melakukan  aksi yang berbahaya seperti mengubah password atau transfer data tanpa sepengetahuan korban.


5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
Answer : 
> Pertama buat fungsi-fungsi baru di file views.py (add, delete, edit dan search produk). Setelah itu tambahkan juga fungsi JSON, XML dan yang pakai id.

> Selanjutnya tambahkan url dari semua fungsi yang tadi ditambahkan di views.py

> Lalu di folder templates edit file main.html, dan buat file-file baru yang mendukung semua fitur website yaitu product_form.html, product_detail.html dan product_list.html. 

> Buat kode untuk menampilkan semua fitur yang diinginkan serta melengkapi design atau ui dari website tersebut.

> Lakukan runserver lokal untuk memastikan bahwa semua fitur berjalan sesuai keinginan.

> Mengecek link url di Postman dan screenshot semuanya, hasil screenshot tsb diupload ke google drive dan linknya ditaruh di README.md

> Melakukan push ke Github terlebih dahulu baru ke PWS dengan command git add . dan git commit - m "..." (menyimpan perubahan di lokal) dilanjut dengan perintah git push origin master untuk mengirim (commit) ke repository


6. Apakah ada feedback untuk asdos di tutorial 2 yang sudah kalian kerjakan?

Answer : Tidak ada


7. Mengakses keempat URL di poin 2 menggunakan Postman, membuat screenshot dari hasil akses URL pada Postman, dan menambahkannya ke dalam README.md.

Answer : https://drive.google.com/drive/folders/1hbAbpzUaoX1nGJmczI1mgxrcHmzoEWd0



===========================================================================
TUGAS 4

1. Apa itu Django AuthenticationForm? Jelaskan juga kelebihan dan kekurangannya.

Answer : Sebuah form bawaan dari Django yang berfungsi untuk memverifikasi user (umumnya dengan username dan password) saat login. Kelebihan dari form ini salah satunya adalah mendukung validasi otomatis, selain itu lebih mudah dan aman untuk digunakan karena sudah terintegrasi dengan sistem authentication Django. Namun form ini memiliki kekurangan yaitu, informasi yang diperlukan untuk login sangat dasar sehingga menjadi kurang fleksibel jika memerlukan info tambahan untuk login (seperti email atau OTP) sehingga memerlukan kustomisasi.



2. Apa perbedaan antara autentikasi dan otorisasi? Bagaimana Django mengimplementasikan kedua konsep tersebut?

Answer : Autentikasi adalah proses memverifikasi identitas user. Di Django autentikasi diterapkan melalui sistem login dan middleware user authentication. Otorisasi adalah proses yang menentukan apa saja yang boleh dilakukan user setelah proses login/autentikasi. Dalam penerapannya menggunakan permissions,groups,decorator (@login_required atau @permission_required)


3. Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?

Answer : Cookies menyimpan data langsung di browser client sehingga lebih ringan bagi server dan data lebih tahan lama, tapi kekurangan dari cookies adalah kurang secure/aman karena rentan dimanipulasi atau dicuri. Sementara session hanya menyimpan data user di server dengan hanya menyimpan session ID di sisi client sehingga lebih fleksibel dan aman, tapi kekurangannya butuh storage lebih di server.


4. Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal tersebut?

Answer : Secara default penggunaan cookies berisiko terhadap kejahatan siber seperti pencurian data atau man in the middle. Untuk menangani hal ini django menyediakan fitur keamanan seperti http only, secure (mengirim cookies hanya lewat https) dan CSRF protection untuk mencegah serangan. Dengan modifikasi konfigurasi yang tepat, risiko penggunaan cookies dapat diminimalisir.


5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

Answer : 
> Tambahkan relasi antara owner dan products di models.py kemudian makemigrations dan migrate

> Selanjutnya implementasi alur untuk autentikasi, membuat option register, login dan logout. Tambahkan juga url routingnya.

> Set cookie(last_login) untuk melihat data last login dan menghapus saat logout(response.delete_cookie("last_login")).

> Buat portal keamanan untuk halaman utama web beserta fitur-fiturnya dengan menambahkan @login_required(harus login terlebih dahulu baru bisa akses)

> Tambahkan kode agar user hanya bisa melihat data sendiri dan produk-produknya, dan saat menyimpan product pastikan kolom owner otomastis diisi oleh user yang sedang login agar product terhubung ke user

> Lalu edit main.html agar menampilkan username dari user yang sedang login dan cookie last loginnya.

> Test server di lokal dengan buat 2 akun dan masing-masing diisi dengan 3 dummy product dan cek apakah setiap produk sesuai dengan ownernya (user yang sedang login).


=============================================================================================================
Tugas 5 

Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!

Answer : Jika ada beberapa CSS selector maka browser akan menentukan urutan prioritasnya melalui specificity (semakin spesifik selector, semakin tinggi prioritasnya). Untuk tingkat prioritas tertinggi dimiliki oleh inline style, dibawahnya ada selector ID, lalu class/pseudo-class/attribute dan di urutan paling rendah ada element. Kalau tingkat specificity nya sama, yang akan ditulis adalah yang terakhir digunakan.



Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design, serta jelaskan mengapa!

Answer : Responsive design penting karena akan memengaruhi pengalaman user, dengan menyesuaikan tampilan web di berbagai layar seperti desktop/mobile. Contoh aplikasi yang belum menerapkan responsive design adalah instagram, instagram kalau dibuka di layar yang cukup lebar seperti laptop/tablet(horizontal) tampilannya akan vertikal persis seperti di mobile dan di sisi kanan dan kiri nya akan ada space hitam. Aplikasi yang sudah menerapkan responsive design adalah google docs, ketika dibuka di mobile pun tampilannya tetap rapih (tidak ada fitur yang tertumpuk)



Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!

Answer : Margin, border dan padding adalah konsep-konsep box model di CSS. Masing-masing memiliki fungsi sebagai berikut :
Margin berfungsi untuk memberi jarak antar elemen
Border memberikan garis pembatas di sekeliling elemen
Padding memberi jarak antara konten dengan batas elemen


Jelaskan konsep flex box dan grid layout beserta kegunaannya!

Answer : Flex box dan grid layout adalah sistem tata letak di CSS. Flex box digunakan untuk mengatur elemen 1 dimensi seperti baris atau kolom agar menjadi lebih fleksibel dan desainnya lebih responsif. Sementara grid layout digunakan untuk mengatur tata letak elemen 2 dimensi (baris dan kolom), cocok untuk desain halaman yang lebih kompleks.


Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!

Answer : 


