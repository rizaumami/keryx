# Keryx

Repo ini merupakan salinan `Keryx` v0.92.4 yang dapat ditemukan di laman proyek aslinya di [https://launchpad.net/keryx](https://launchpad.net/keryx).

README asli bisa dilihat di [doc/README](doc/READM).


## What

`Keryx` adalah alat bantu bagi pengguna Debian, Ubuntu, dan turunannya, yang memiliki keterbatasan sambungan internet untuk mengunduh dan atau memutakhirkan sistem operasinya.

## Who

`Keryx` tidak hanya berguna bagi para fakir *bandwidth*, namun juga bagi mereka memiliki koneksi internet namun karena satu dan lain sebab komputernya tida mampu tersambung ke internet.

## Why

Sistem operasi selalu berkembang, baik untuk penambahan kegunaan maupun penambalan kelemahan. Jadi sistem operasi wajib untuk selalu update.

Kadang pula, aplikasi yang terpasang dalam sistem operasi tidak memenuhi kebutuhan pengguna. Jadi si pengguna butuh memasang aplikasi penunjang keperluannya.

Dua hal tidak atas tidak menjadi masalah jika komputer tersambung internet. Jika komputer tidak dapat tersambung internet, `Keryx` dapat membantu.

## When

`Keryx` bisa digunakan kapan saja. Walau tujuannya menolong kita yang kesulitan sambungan internet, `Keryx` bisa pula kita gunakan ketika sedang memiliki sambungan internet, misalnya menolong mereka yang komputernya tidak terhubung internet.

## Where

`Keryx` dapat dijalankan di GNU/Linux, Windows dan Mac, dengan syarat *dependencies*-nya terpenuhi. Lihat bagian **How** berikut.

## How

Lihat tutorial asli di [doc/Tutorial.html](doc/Tutorial.html) atau terjemahan di [Tutorial.md](Tutorial.md)

Berikut rincian prasyarat yang diperlukan agar `Keryx` dapat bekerja dengan benar.

#### Windows

Tidak ada.

Klik ganda untuk menjalankan `win32/keryx.exe` dalam Windows.

#### Linux

Pasang paket berikut:

* `Python`
* `wxPython`

Pengguna Ubuntu perlu untuk memasang paket berikut agar `wxPython` terpasang sempurna:

* `libwxbase2.8-0`
* `libwxgtk2.8-0`
* `python-wxversion`
* `python-wxgtk2.8`

`wxPython` hanya diperlukan untuk menggunakan antarmuka grafis `Keryx`. Pembuatan *Project* dapat dilakukan menggunakan baris perintah. Lihat **USAGE** untuk keterangan lebih lanjut.

### Panduan pemasangan

Uraikan berkas `Keryx` (umumnya di perangkat usb).

### Penggunaan

`Keryx` berdasarkan konsep `projects`. Tiap *project* menyimpan rekam jejak versi perangkat lunak yang terpasang pada komputer. Pertama memulai, Anda mesti membuat sebuah berkas *project* pada komputer (offline).

Jika dalam komputer (*offline*) tidak terdapat `wxPython` namun terpasang `Python`, Anda dapat tetpa membuat `projects` menggunakan baris perintah pada `terminal`:

```sh
python keryx.py --create <project name> <plugin name>
```

dan `Keryx` akan membuat sebuah `project` dalam map `projects`. Hal ini akan membantu mereka yang memasang Ubuntu *server* dan tidak umunya belum terpasang `wxPython`. Untuk sementara, hanya Debian yang tersedia bagi `<plugin name>`.

Ketika selesai membuat `project` ini, pastikan untuk menyalin map `Keryx` ini ke perangkat usb yang akan Anda gunakan untuk menjalankan `Keryx` dalam komputer yang memiliki sambungan internet.

`Keryx` dapat dijalankan pada **SEMUA** komputer yang terpasang `Python` dan `wxPython`, artinya komputer Windows, Mac dan Linux. Menjalankan `Keryx` dalam komputer Windows adalah dengan menjalankan berkas `keryx.exe`. Jika Anda menjalankan `Keryx` menggunakan `Python`, `cd` ke dalam direktori `source` dan jalankan `python keryx.py`. Beberapa `Desktop Environments` mampu menjalankan aplikasi `python` cukup dengan mengklik ganda berkas `python`-nya.

Setelah Anda membuaka `Keryx` pada komputer yang memiliki sambungan internet, mengunduh paket semudah membuka `project` Anda dan memilih paket untuk diunduh.
`Keryx` akan secara otomatis memilih paket yang menjadi ketergantungan (*dependencies*) dan memastikan semua yang diperlukan terunduh. Setiap paket yang telh diunduh akan disimpan pada map `project` dalam direktori `packages`.

Setelah selesai, kembali ke komputer (*offline*) dan pasang paket seperti biasa.

### Thanks

#### Kontributor Project/Profil

* [@ariesm](http://telegram.me/ariesm) : [elementaryos-freya-64bit](https://github.com/rizaumami/keryx/blob/master/projects/elementaryos-freya-64bit.7z), [ubuntu-14.10-64bit](https://github.com/rizaumami/keryx/blob/master/projects/ubuntu-14.10-64bit.7z), [lxle-14.04.2-64bit](https://github.com/rizaumami/keryx/blob/master/projects/lxle-14.04.2-64bit.7z), [xubuntu-14.04.2-64bit](https://github.com/rizaumami/keryx/blob/master/projects/xubuntu-14.04.2-64bit.7z)
* [@mas_aiz](http://telegram.me/mas_aiz) : [linuxmint-17-kde-64bit](https://github.com/rizaumami/keryx/blob/master/projects/linuxmint-17-kde-64bit.7z)
* [@isnusindang](http://telegram.me/isnusindang) : [elementaryos-freya-32bit](https://github.com/rizaumami/keryx/blob/master/projects/elementaryos-freya-32bit.7z), [kubuntu-15.04-32bit](https://github.com/rizaumami/keryx/blob/master/projects/kubuntu-15.04-32bit.7z), [ubuntu-14.10-32bit](https://github.com/rizaumami/keryx/blob/master/projects/ubuntu-14.10-32bit.7z)

### Catatan tambahan

Parameter baris perintah:

```sh
-h or --help                            Menampilkan pesan ini
-v or --version                         Menampilkan versi Keryx
--create <nama project> <nama plugin>   Membuat project baru dalam direktori
                                        dengan <nama project> dan jenis project
                                        <nama plugin>
--config <berkas>                       Gunakan <berkas> sebagai configuration file
```

Karena sifat `py2exe`, keterangan yang tampil pada `console` **TIDAK** ditampilkan.
Sementara parameter baris perintah akan tetap bekerja dengan benar, tidak ada indikasi yang tampil pada `console`. Informasi akan tetap dituliskan pada berkas `log` untuk telaah lanjutan.
