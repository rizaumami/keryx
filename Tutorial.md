# Tutrial Keryx

### Mendapatkan Keryx

Unduh `Keryx` dengan melakukan:

```sh
git clone https://github.com/rizaumami/keryx.git
```

atau dengan mengunduh `https://github.com/rizaumami/keryx/archive/master.zip`.

Simpan dan uraikan ke dalam USB *flash disk*.

### Menjalankan Keryx

#### Dalam Linux

Jalankan berkas `source/keryx.py`.

#### Dalam Windows

Jalankan berkas `win32/keryx.exe`.

### Membuat Project (di komputer offline)

Di awal membuka `Keryx`, masukkan nama *project* Anda, atau biarkan sesuai *default* dan klik tombol `New Project`.

![Membuat project](https://github.com/rizaumami/keryx/blob/master/doc/Tutorial_Files/Create_Project.png)

Ketika ditanya apakah Anda ingin mengunduh daftar paket terkini, pilih `No`, kemudian tutup `Keryx`.

### Membuka Project (di komputer online)

Jalankan `Keryx` dan pilih *project* Abda dari menu *drop-down* paling bawah. Kemudian klik `Open Project`.

![Membuat project](https://github.com/rizaumami/keryx/blob/master/doc/Tutorial_Files/Open_Project.png)

Jika Anda ingin memiliki daftar paket terkini sesuai di *mirror/repo*, pilih `Yes` ketika ditanya apakah akan mengunduh daftar paket terkini (disarankan).

### Memasang Paket (di komputer offline)

Buka `project` Anda dan pilih `Install Packages` dari menu `Project`. Periksa semua paket yang ingin Anda pasang dan klik `Continue`.

Sebuah `terminal` akan menampilkan laju pemasangan paket. Setelah pemasangan selesai, tekan **ENTER**.

Agar `Keryx` Menyadari bahwa Anda telah memiliki paket baru terpasang di komputer, Anda harus memutakhirkan **project status** (`Project` > `Update Status`).
