# Kriptanalisis Cipher Abjad-Tunggal — Kelompok 9

Repositori ini berisi solusi **Soal B** tugas mata kuliah Kriptografi: melakukan kriptanalisis terhadap ciphertext berbahasa Inggris yang dienkripsi menggunakan **cipher substitusi abjad-tunggal** (*monoalphabetic substitution cipher*).

**Repositori:** https://github.com/rxl2-wqwq/cyptanalysis

---

## 1. Identitas Tugas

| Item | Keterangan |
|---|---|
| Mata kuliah | Kriptografi |
| Kelompok | 9 |
| Bagian tugas | B — Kriptanalisis Cipher Abjad-Tunggal |
| Berkas yang dianalisis | `cipher1.txt` |
| Bahasa pemrograman | Python 3 |
| Metode | Analisis frekuensi + analisis pola kata + metode terkaan (konteks bahasa Inggris) |
| Tool bantu | Program `cryptanalysis.py` (dirancang sendiri) |

---

## 2. Latar Belakang

Pada cipher substitusi abjad-tunggal, setiap huruf plaintext digantikan oleh satu huruf ciphertext yang tetap sepanjang pesan. Jika huruf `e` dipetakan menjadi `z`, maka **setiap** `e` dalam plaintext selalu menjadi `z` dalam ciphertext.

Ruang kunci cipher ini sangat besar, sebanyak `26!` atau sekitar:

```
403.291.461.126.605.635.584.000.000
```

Angka tersebut jauh melebihi ruang kunci DES (2^56). Meskipun demikian, cipher ini tetap dapat dipecahkan karena satu kelemahan fundamental: **struktur statistik bahasa plaintext tidak ikut tersembunyi**. Huruf yang sering muncul pada plaintext menghasilkan huruf ciphertext yang juga sering muncul; pola pengulangan huruf dalam kata, panjang kata, bigram, dan trigram juga tetap dipertahankan.

Inilah yang menjadi fokus tugas ini: menunjukkan bahwa besar ruang kunci tidak menjamin keamanan, dan membuktikannya dengan memecahkan `cipher1.txt` menggunakan analisis frekuensi, pola kata, dan konteks bahasa Inggris.

---

## 3. Struktur Repositori

```
cyptanalysis/
├─ cipher1.txt          # ciphertext yang diberikan untuk Kelompok 9
├─ cryptanalysis.py     # program alat bantu kriptanalisis
└─ README.md            # dokumentasi ini
```

---

## 4. Cara Menjalankan Program

### 4.1 Prasyarat

- Python 3.8 atau lebih baru
- Tidak ada dependensi eksternal — program hanya menggunakan pustaka standar Python (`collections`, `pathlib`, `re`, `sys`)

### 4.2 Menjalankan

Pastikan `cipher1.txt` berada di folder yang sama dengan `cryptanalysis.py`, lalu jalankan dari terminal:

```bash
cd cyptanalysis
python cryptanalysis.py
```

Jika ciphertext berada di lokasi lain, nama file dapat diberikan sebagai argumen:

```bash
python cryptanalysis.py /path/ke/cipher1.txt
```

### 4.3 Output Program

Program menampilkan tiga bagian:

**a. Frekuensi huruf** — jumlah kemunculan tiap huruf, diurutkan dari terbanyak:

```
=== FREKUENSI HURUF ===
g: 249
u: 187
m: 135
a: 117
x: 112
...
```

**b. Kata yang sering muncul beserta pola hurufnya** — huruf yang sama dalam satu kata diberi nomor pola yang sama:

```
=== KATA YANG SERING MUNCUL ===
usg       38 kali | pola (0, 1, 2)
zm        18 kali | pola (0, 1)
x         17 kali | pola (0,)
qguuga    14 kali | pola (0, 1, 2, 2, 1, 3)
mjymuzujuzkd  6 kali | pola (0, 1, 2, 0, 3, 4, 3, 1, 3, 4, 5, 6)
...
```

**c. Hasil dekripsi sementara** — huruf yang sudah memiliki mapping diterjemahkan; huruf yang belum diketahui ditampilkan sebagai `_`:

```
=== HASIL DEKRIPSI SEMENTARA ===
substitution ciphers
in simple substitution ciphers, a particular letter or symbol is substituted
for each letter. the letters are substituted in their normal order, usually with
...
```

---

## 5. Alur Kerja Pengguna

Program ini adalah **alat bantu**, bukan pemecah otomatis. Penentuan mapping tetap dilakukan oleh pengguna melalui siklus kerja berikut:

```
1. Baca frekuensi huruf & kata yang sering muncul dari output program
        │
        ▼
2. Bandingkan pola kata ciphertext dengan kata bahasa Inggris
   (mis. pola (0,1,2,0,3,4,3,1,3,4,5,6) → "substitution")
        │
        ▼
3. Tambahkan pasangan huruf baru ke dictionary MAPPING di cryptanalysis.py
        │
        ▼
4. Jalankan ulang program → periksa hasil dekripsi sementara
        │
        ├── hasil masih ada "_" atau kalimat aneh ──► kembali ke langkah 1
        │
        └── seluruh teks terbaca sebagai bahasa Inggris yang masuk akal ──► selesai
```

Setiap iterasi menambah beberapa pasangan huruf; hasil dekripsi yang semakin terbaca menjadi konfirmasi bahwa mapping yang baru benar.

---

## 6. Metode Pemecahan Ciphertext

### Tahap 1 — Identifikasi jenis cipher

Ciri yang diamati pada `cipher1.txt`:

- spasi dan tanda baca tetap utuh (tidak dienkripsi);
- huruf yang sama selalu menghasilkan huruf ciphertext yang sama di seluruh teks;
- frekuensi huruf tidak merata (tidak acak);
- panjang kata dan pola huruf berulang dipertahankan.

Berdasarkan ciri tersebut, ciphertext diidentifikasi sebagai **cipher substitusi abjad-tunggal**.

### Tahap 2 — Mencari kata dengan pola khas

Kata pertama ciphertext:

```
mjymuzujuzkd
```

Pola hurufnya: `(0,1,2,0,3,4,3,1,3,4,5,6)` — huruf ke-1 dan ke-4 sama, huruf ke-6, ke-8, dan ke-10 sama, dst. Satu-satunya kata bahasa Inggris umum yang cocok adalah:

```
substitution
```

Dari pasangan ini diperoleh mapping awal:

| Cipher | Plaintext |
|---|---|
| m | s |
| j | u |
| y | b |
| u | t |
| z | i |
| k | o |
| d | n |

### Tahap 3 — Memperluas mapping dari kata lain

Kata berikutnya `wznsgam` dapat diterjemahkan dengan mapping awal menjadi `_i_ _ _ _rs` → terbaca sebagai **ciphers**, sehingga diperoleh:

| w | n | s | g | a |
|---|---|---|---|---|
| c | p | h | e | r |

Kata pendek memberikan konfirmasi cepat:

| Ciphertext | Pola | Plaintext | Alasan |
|---|---|---|---|
| `zd` | 2 huruf | `in` | preposisi paling umum |
| `x` | 1 huruf | `a` | satu-satunya kata 1 huruf bahasa Inggris |
| `usg` | 3 huruf, paling sering (38×) | `the` | kata tersering bahasa Inggris |
| `xdi` | 3 huruf | `and` | konjungsi umum |
| `kc` / `uk` / `ye` | 2 huruf | `of` / `to` / `by` | preposisi umum |

### Tahap 4 — Validasi melalui konteks kalimat

Setiap dugaan mapping diuji dengan membaca hasil dekripsi sementara. Contoh hasil yang mengonfirmasi kebenaran mapping:

```
in simple substitution ciphers, a particular letter or symbol is substituted
for each letter. the letters are substituted in their normal order, usually with
normal word divisions.
```

Kalimat tersebut masuk akal, koheren, dan sesuai topik kriptografi. Jika suatu mapping salah, hasilnya langsung terlihat sebagai kata yang tidak bermakna (misalnya `recognihed` sebelum huruf `z → z` dan `z → x` dikoreksi).

### Tahap 5 — Menutup huruf yang tersisa

Huruf yang belum termapping diidentifikasi dari kata yang masih mengandung `_`, lalu ditekan dari konteksnya. Contoh:

| Konteks | Ciphertext | Plaintext | Kesimpulan |
|---|---|---|---|
| `mebykq` (≈ mem_ry) | `b` | `m` | memory |
| `caghjgdwzgm` (≈ _requencies) | `c`, `h` | `f`, `q` | frequencies |
| `pgerkai` (≈ _ey_ord) | `p` | `k` | keyword |
| `fjqzjm` (≈ _ulius) | `f` | `j` | Julius Caesar |
| `gvxbnqg` (≈ e_a_ple) | `v` | `x` | example |

Setelah seluruh 26 huruf termapping, dekripsi menghasilkan plaintext penuh tanpa satu pun `_`.

---

## 7. Mapping Lengkap yang Ditemukan

Tabel substitusi hasil kriptanalisis (cipher → plaintext):

```
Cipher : a b c d e f g h i j k l m n o p q r s t u v w x y z
Plain  : r m ? n y j e q v u o ? s p ? k l h w t g c i a b x
```

Dalam bentuk pasangan:

```
m → s      w → c      b → m      i → d      r → w
j → u      n → p      c → f      l → z      t → g
y → b      s → h      e → y      o → v      v → x
u → t      g → e      f → j      p → k
z → i      a → r      h → q
k → o      x → a
d → n      q → l
```

---

## 8. Hasil Dekripsi

Bagian awal plaintext hasil dekripsi:

```
substitution ciphers

in simple substitution ciphers, a particular letter or symbol is substituted
for each letter. the letters are substituted in their normal order, usually with
normal word divisions. such ciphers are recognized by the occurrence of a set of
normal letter frequencies attached to the wrong letters. they are solved by using
frequency analysis and by noting the characteristics of particular letters,
such as the tendency to form doubles, common word prefixes and suffixes,
common first and last letters in words, and common combinations, such as qu,
th, er, and re.
```

Bagian lanjutan membahas Caesar cipher:

```
a substitution cipher is performed by reordering the letters in the alphabet.
for example, a cipher devised long ago by julius caesar shifts all the letters
in the alphabet by three places. ...
```

Serta penutup tentang polyalphabetic cipher:

```
in multiple-substitution (polyalphabetic) ciphers, a keyword or number is
employed. the first message letter might be enciphered by adding to it the
numerical value of the first letter of the keyword; ...
```

Plaintext membahas: pengertian cipher substitusi, kelemahannya terhadap analisis frekuensi, Caesar cipher dan lookup table, serta multiple-substitution (polyalphabetic) cipher dengan keyword.

---

## 9. Fitur Program `cryptanalysis.py`

| Fitur | Fungsi |
|---|---|
| Pembacaan file | Membaca ciphertext dari `cipher1.txt` (atau argumen path) |
| Analisis frekuensi | Menghitung & mengurutkan kemunculan tiap huruf (`collections.Counter`) |
| Analisis kata | Mencari kata yang paling sering muncul (20 teratas) |
| Analisis pola | Menampilkan pola pengulangan huruf tiap kata — kunci untuk mencocokkan dengan kata bahasa Inggris |
| Dekripsi bertahap | Menerapkan dictionary `MAPPING` (cipher → plaintext); huruf yang belum diketahui ditampilkan `_` |
| Dukungan argumen | Path file ciphertext dapat dilewatkan lewat command line |

Semua fungsionalitas menggunakan **pustaka standar Python** — tidak ada dependensi eksternal.

---

## 10. Keterbatasan Program (bukan bug)

1. **Mapping dimasukkan manual.** Program tidak menemukan kunci secara otomatis; pasangan huruf hasil analisis pengguna ditulis ke dictionary `MAPPING`. Ini sesuai ketentuan soal yang memperbolehkan metode statistik dan terkaan.
2. **Belum ada pemecah otomatis.** Teknik seperti simulated annealing, hill climbing, dictionary scoring, atau analisis n-gram belum digunakan.
3. **Asumsi satu kunci untuk seluruh teks.** Ketentuan soal menyebut setiap paragraf mungkin memakai kunci berbeda, namun pengamatan terhadap `cipher1.txt` menunjukkan mapping **konsisten di seluruh paragraf** (diverifikasi: setiap paragraf didekripsi tanpa `_` menggunakan satu tabel). Hal ini didokumentasikan sebagai temuan observasi.
4. **Hanya untuk alfabet A–Z.** Angka, tanda baca, dan spasi diteruskan apa adanya — sesuai ketentuan enkripsi pada soal.

---

## 11. Kesimpulan

`cipher1.txt` berhasil didekripsi sepenuhnya. Pemecahan tidak dilakukan dengan brute force terhadap `26!` kemungkinan kunci, melainkan dengan memanfaatkan kelemahan mendasar cipher substitusi abjad-tunggal: **statistik bahasa tidak ikut terenkripsi**.

Tiga senjata yang digunakan:

1. **Analisis frekuensi** — huruf ciphertext tersering dicocokkan dengan huruf bahasa Inggris tersering.
2. **Analisis pola kata** — pengulangan huruf dalam kata dicocokkan dengan kata bahasa Inggris (mis. `mjymuzujuzkd` ↔ `substitution`).
3. **Metode terkaan berbasis konteks** — kalimat hasil dekripsi sementara dibaca; mapping yang menghasilkan bahasa Inggris koheren dipertahankan.

Ketiganya dipadukan melalui siklus iteratif: duga → terapkan mapping → baca hasil → perbaiki. Program `cryptanalysis.py` mempercepat setiap iterasi dengan menyajikan statistik dan hasil dekripsi secara instan.

Temuan penting yang didokumentasikan: meskipun ruang kunci `26!` jauh melebihi 2^56 (DES), cipher ini tumbang dalam hitungan menit. **Besar ruang kunci bukan jaminan keamanan; yang menentukan adalah apakah struktur statistik plaintext berhasil disembunyikan.**

---

## 12. Lisensi & Kontribusi

Dibuat oleh **Kelompok 9** untuk tugas UTS Kriptografi.

Repositori: https://github.com/rxl2-wqwq/cyptanalysis
