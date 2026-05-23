# Deployment Streamlit

Gunakan file utama berikut saat deploy:

```text
transport_bi_system/app.py
```

Jangan pilih file di folder `pages/` sebagai entry point. Folder `pages/` hanya untuk halaman tambahan Streamlit multipage.

## Streamlit Community Cloud

1. Push project ini ke GitHub.
2. Buka Streamlit Community Cloud.
3. Pilih repository.
4. Isi `Main file path`:

```text
transport_bi_system/app.py
```

5. Deploy.

File deployment yang disiapkan:

- `requirements.txt` di root repo, mengarah ke dependency project.
- `runtime.txt` untuk memaksa Python 3.11.
- `packages.txt` untuk memasang Java runtime yang dibutuhkan PySpark.
- `transport_bi_system/.streamlit/config.toml` untuk mode headless.

## Login Default

```text
username: admin
password: admin123
```

Untuk deployment serius, ubah credential melalui Streamlit secrets atau environment variables.

## Masalah Umum

Jika deploy gagal karena `pyspark` atau Java:

- Pastikan `packages.txt` ada di root repository.
- Pastikan isinya `openjdk-17-jre-headless`.

Jika app tidak ditemukan:

- Pastikan main file path adalah `transport_bi_system/app.py`.
- Jangan gunakan `transport_bi_system/pages/1_Executive_Summary.py`.

Jika dependency tidak terbaca:

- Pastikan `requirements.txt` ada di root repository.
- Pastikan isinya:

```text
-r transport_bi_system/requirements.txt
```
