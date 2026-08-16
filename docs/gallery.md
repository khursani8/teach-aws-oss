---
layout: default
title: Model responses by service
prev: shipped
---

# Same question, four models, six services

Every example below is a real generation (greedy decoding) on an unseen eval question,
one per service. Judge verdicts from the full eval, not these single samples.

| Model | What to look for |
|---|---|
| teach-aws (H3) | reference-register, fact-complete |
| teach-aws D | same facts, rephrased |
| PixelSpaceAI 7B LoRA | fluent Malay, register-first |
| mesolitica 7B base | the starting point |


## s3

**Q:** Bagaimana saya boleh memastikan perlindungan maksimum untuk versi yang dipelihara?

<details><summary>reference</summary>

Keupayaan MFA Delete (Multi-Factor Authentication) Versioning boleh digunakan untuk menyediakan lapisan keselamatan tambahan. Secara lalai, semua permintaan ke bucket Amazon S3 anda memerlukan kelayakan akaun AWS anda. Jika anda mendayakan Versioning dengan MFA Delete pada bucket Amazon S3 anda, dua bentuk pengesahan diperlukan untuk memadamkan versi objek secara kekal: kelayakan akaun AWS anda dan kod enam digit yang sah serta nombor siri daripada peranti pengesahan yang berada dalam milikan fi

</details>

**teach-aws (H3):** Keupayaan MFA Delete (Multi-Factor Authentication) Versioning boleh digunakan untuk menyediakan lapisan keselamatan tambahan. Secara lalai, semua permintaan ke bucket Amazon S3 anda memerlukan kelayakan akaun AWS anda. Jika anda mendayakan Versioning dengan MFA Delete pada bucket Amazon S3 anda, dua bentuk pengesahan diperlukan untuk memadamkan versi objek secara kekal: kelayakan akaun AWS anda dan kod enam digit yang sah serta nombor siri daripada peranti pengesahan yang berada dalam milikan fizikal anda. Untuk mengetahui lebih lanjut tentang mendayakan Versioning dengan MFA Delete, termasuk 


**teach-aws (D, flexible):** Apabila anda memulakan versi baharu, anda boleh menetapkan sama ada versi utama atau minor sebagai versi yang akan dipelihara. Amazon API Gateway menyediakan versi baharu secara automatik untuk semua REST API anda apabila versi baharu didayakan. Amazon API Gateway kemudian menyediakan pengemaskinian untuk setiap sumber dalam REST API anda berdasarkan corak penggunaan. Sebagai contoh, jika anda mempunyai API carian dan pencarian yang menggunakan dua sumber, satu untuk setiap sumber, dan anda mendayakan versi baharu untuk carian, Amazon API Gateway akan menyediakan versi baharu untuk carian apab


**PixelSpaceAI 7B LoRA:** Untuk memastikan perlindungan maksimum, anda boleh menggunakan dasar bucket untuk menyekat akses kepada semua versi objek, termasuk yang dipelihara, dan menyediakan kebenaran yang lebih terperinci untuk akses kepada versi semasa sahaja. Anda juga boleh menggunakan dasar bucket untuk menetapkan dasar pengekalan yang memastikan semua versi objek dipelihara selama-lamanya.


<details><summary>mesolitica 7B base</summary>

Untuk memastikan perlindungan maksimum untuk versi yang disimpan, anda boleh mengikuti langkah-langkah berikut:

1. Gunakan sistem penyimpanan yang selamat dan boleh dipercayai, seperti penyimpanan awan atau perkhidmatan penyimpanan yang disediakan oleh pihak ketiga yang dipercayai.

2. Pastikan versi yang disimpan disimpan dalam format yang selamat dan tidak boleh diubah, seperti format fail yang tidak boleh diubah atau format fail yang disulitkan.

3. Lakukan pemeriksaan keselamatan berkala untuk memastikan versi yang disimpan tidak terdedah kepada ancaman keselamatan seperti serangan siber 

</details>


## lambda

**Q:** Apakah CloudWatch Live Tail dan bagaimana ia berfungsi dengan Lambda?

<details><summary>reference</summary>

CloudWatch Logs Live Tail ialah keupayaan penstriman log dan analitik interaktif yang menyediakan keterlihatan masa nyata ke dalam log, memudahkan pembangunan dan penyelesaian masalah fungsi Lambda. Ini membolehkan pembangun menguji dan mengesahkan perubahan kod atau konfigurasi dengan cepat dalam masa nyata, mempercepatkan kitaran tulis-uji-sebar (juga dikenali sebagai "gelung pembangunan dalaman") semasa membina aplikasi dengan Lambda. Pengalaman Live Tail juga membolehkan pengendali dan pasuk

</details>

**teach-aws (H3):** CloudWatch Logs Live Tail ialah keupayaan penstriman log dan analitik interaktif yang menyediakan keterlihatan masa nyata ke dalam log, memudahkan pembangunan dan penyelesaian masalah fungsi Lambda. Ini membolehkan pembangun menguji dan mengesahkan perubahan kod atau konfigurasi dengan cepat dalam masa nyata, mempercepatkan kitaran tulis-uji-sebar (juga dikenali sebagai "gelung pembangunan dalaman") semasa membina aplikasi dengan Lambda. Pengalaman Live Tail juga membolehkan pengendali dan pasukan DevOps mengesan dan menyahpepijat kegagalan dan ralat kritikal dalam kod fungsi Lambda dengan leb


**teach-aws (D, flexible):** CloudWatch Live Tail ialah keupayaan analitik interaktif baharu yang memberikan anda paparan masa nyata bagi metrik dan peristiwa yang penting untuk aplikasi anda. Live Tail untuk AWS Lambda memberikan anda paparan masa nyata tentang prestasi, kesihatan, dan penggunaan (termasuk panggilan yang disekat) untuk fungsi Lambda anda. Live Tail membolehkan pembangun dan pengendali dengan cepat mengesan isu kritikal dengan segera dan menyelesaikan masalah dengan lebih cepat, mengurangkan Mean Time to Recovery (MTTR) semasa memberi tumpuan kepada pemulihan aplikasi.


**PixelSpaceAI 7B LoRA:** CloudWatch Live Tail ialah ciri yang membolehkan anda melihat output sebenar daripada fungsi Lambda atau proses tanpa pelayan tanpa perlu menunggu log disimpan. Ia memaparkan output log dalam masa nyata dalam konsol CloudWatch. Anda boleh melihat output sebenar fungsi Lambda, termasuk ralat dan mesej stdout/stderr, dalam konsol CloudWatch tanpa perlu menunggu log disimpan. Ini berguna untuk debug dan memahami apa yang berlaku semasa pelaksanaan.


<details><summary>mesolitica 7B base</summary>

CloudWatch Live Tail adalah ciri yang membolehkan anda melihat log dalam masa nyata dari pelbagai sumber, termasuk AWS Lambda. Ia membolehkan anda memantau dan memeriksa log dengan mudah tanpa perlu menunggu log dikumpulkan dan disimpan dalam CloudWatch Logs.

Dalam konteks AWS Lambda, CloudWatch Live Tail boleh digunakan untuk memantau log yang dihasilkan oleh fungsi Lambda anda. Ini membolehkan anda memeriksa log dengan cepat dan tepat untuk menyelesaikan masalah atau memantau prestasi fungsi Lambda anda.

Untuk menggunakan CloudWatch Live Tail dengan Lambda, anda perlu mengaktifkan ciri ini

</details>


## cloudfront

**Q:** Bagaimanakah saya boleh melindungi aplikasi web saya yang dihantar melalui CloudFront daripada serangan DDoS?

<details><summary>reference</summary>

Sebagai pelanggan AWS, anda mendapat AWS Shield Standard tanpa kos tambahan. AWS Shield ialah perkhidmatan terurus yang menyediakan perlindungan terhadap serangan DDoS untuk aplikasi web yang berjalan di AWS. AWS Shield Standard menyediakan perlindungan untuk semua pelanggan AWS terhadap serangan Infrastruktur (lapisan 3 dan 4) yang biasa dan paling kerap berlaku seperti SYN/UDP Floods, Reflection attacks, dan lain-lain untuk menyokong ketersediaan tinggi aplikasi anda di AWS. Lampirkan AWS WAF 

</details>

**teach-aws (H3):** Sebagai pelanggan AWS, anda mendapat AWS Shield Standard tanpa kos tambahan. AWS Shield ialah perkhidmatan terurus yang menyediakan perlindungan terhadap serangan DDoS untuk aplikasi web yang berjalan di AWS. AWS Shield Standard menyediakan perlindungan untuk semua pelanggan AWS terhadap serangan Infrastruktur (lapisan 3 dan 4) yang biasa dan paling kerap berlaku seperti SYN/UDP Floods, Reflection attacks, dan lain-lain untuk menyokong ketersediaan tinggi aplikasi anda di AWS. Lampirkan AWS WAF pada pengedaran CloudFront anda dan dayakan AntiDDoS AMR, ciri yang disasarkan khusus untuk mitigasi


**teach-aws (D, flexible):** Untuk melindungi daripada serangan DDoS, anda boleh menggunakan kombinasi AWS Shield (piawai disertakan percuma, Advanced untuk perlindungan lanjutan) dan AWS WAF untuk menyekat trafik berbahaya. Anda juga boleh menggunakan Amazon CloudFront yang disepadukan dengan AWS Shield untuk memastikan sumber anda di hadapan tidak terjejas. Untuk DDoS yang canggih, anda boleh menggunakan gabungan CloudFront, WAF, dan Shield untuk membentuk pertahanan berlapis.


**PixelSpaceAI 7B LoRA:** CloudFront menyediakan perlindungan terbina dalam terhadap serangan DDoS. CloudFront menggunakan pengesahan berasaskan IP dan algoritma penapisan berat untuk mengurangkan trafik yang berpotensi berbahaya. CloudFront juga menyediakan perlindungan DDoS lanjutan yang boleh anda gunakan untuk melindungi aplikasi web anda dengan lebih lanjut. Perlindungan DDoS lanjutan CloudFront boleh anda gunakan untuk melindungi aplikasi web anda dengan lebih lanjut. Perlindungan DDoS lanjutan CloudFront boleh anda gunakan untuk melindungi aplikasi web anda dengan lebih lanjut.


<details><summary>mesolitica 7B base</summary>

Untuk melindungi aplikasi web anda yang dihantar melalui CloudFront daripada serangan DDoS, anda boleh mengambil beberapa langkah berikut:

1. **Gunakan CloudFront Web Application Firewall (WAF)**: CloudFront menyediakan WAF yang boleh mengesan dan menghalang serangan DDoS. anda boleh mengaktifkan WAF untuk menguruskan serangan yang mencurigakan.

2. **Gunakan CloudFront Distribution**: Pastikan anda menggunakan CloudFront Distribution yang mempunyai ciri-ciri keselamatan yang diperlukan seperti pengesahan pengguna, pengesahan kandungan, dan pengesahan sumber.

3. **Gunakan AWS Shield**: AWS S

</details>


## vpc

**Q:** Bagaimanakah saya menetapkan alamat IP peribadi kepada instans Amazon EC2 dalam VPC?

<details><summary>reference</summary>

Apabila anda melancarkan instans Amazon EC2 dalam subnet yang bukan IPv6-only, anda boleh secara pilihan menentukan alamat IPv4 peribadi utama untuk instans tersebut. Jika anda tidak menentukan alamat IPv4 peribadi utama, AWS secara automatik menetapkannya daripada julat alamat IPv4 yang anda tetapkan kepada subnet tersebut. Anda boleh menetapkan alamat IPv4 peribadi sekunder semasa melancarkan instans, semasa mencipta Elastic Network Interface, atau pada bila-bila masa selepas instans dilancark

</details>

**teach-aws (H3):** Apabila anda melancarkan instans Amazon EC2 dalam subnet yang bukan IPv6-only, anda boleh secara pilihan menentukan alamat IPv4 peribadi utama untuk instans tersebut. Jika anda tidak menentukan alamat IPv4 peribadi utama, AWS secara automatik menetapkannya daripada julat alamat IPv4 yang anda tetapkan kepada subnet tersebut. Anda boleh menetapkan alamat IPv4 peribadi sekunder semasa melancarkan instans, semasa mencipta Elastic Network Interface, atau pada bila-bila masa selepas instans dilancarkan atau antara muka dicipta. Sekiranya anda melancarkan instans Amazon EC2 dalam subnet IPv6-only, A


**teach-aws (D, flexible):** Apabila anda melancarkan instans Amazon EC2 dalam subnet yang bukan IPv6-only, anda boleh secara pilihan menentukan alamat IPv4 peribadi utama untuk instans tersebut. Jika anda tidak menentukan alamat IPv4 peribadi utama, AWS secara automatik menetapkannya daripada julat alamat IPv4 yang anda tetapkan kepada subnet tersebut. Anda boleh menetapkan alamat IPv4 peribadi sekunder semasa melancarkan instans, semasa mencipta Elastic Network Interface, atau pada bila-bila masa selepas instans dilancarkan atau antara muka dicipta. Sekiranya anda melancarkan instans Amazon EC2 dalam subnet IPv6-only, A


**PixelSpaceAI 7B LoRA:** Anda boleh menetapkan alamat IP peribadi kepada instans Amazon EC2 dalam VPC dengan memilih alamat IP semasa memulakan instans tersebut. Anda juga boleh menetapkan alamat IP peribadi kepada instans sedia ada dalam VPC dengan memanggil API ModifyInstanceAttribute atau menggunakan AWS Management Console.


<details><summary>mesolitica 7B base</summary>

Untuk menetapkan alamat IP peribadi kepada instans Amazon EC2 dalam VPC, anda perlu mengikuti langkah-langkah berikut:

1. **Cipta VPC dan Subnet**: Pertama, anda perlu mencipta VPC dan subnet yang sesuai untuk instans EC2 anda. Pastikan subnet tersebut mempunyai alamat IP yang anda inginkan.

2. **Cipta Instans EC2**: Selepas itu, cipta instans EC2 anda dalam VPC yang telah dicipta. Pilih jenis instans yang sesuai dan pilih konfigurasi yang membolehkan anda menetapkan alamat IP peribadi.

3. **Konfigurasi Alamat IP Peribadi**: Pada langkah ini, anda perlu menetapkan alamat IP peribadi untuk i

</details>


## rds

**Q:** Bagaimanakah saya mengintegrasikan Enhanced Monitoring dengan alat yang saya gunakan pada masa ini?

<details><summary>reference</summary>

Amazon RDS Enhanced Monitoring menyediakan satu set metrik yang dibentuk sebagai muatan JSON yang dihantar ke akaun CloudWatch Logs anda. Muatan JSON dihantar pada granulariti yang terakhir dikonfigurasikan untuk instance Amazon RDS. Terdapat dua cara anda boleh menggunakan metrik melalui papan pemuka atau aplikasi pihak ketiga. Alat pemantauan boleh menggunakan Langganan CloudWatch Logs untuk menyediakan suapan hampir masa nyata untuk metrik. Sebagai alternatif, anda boleh menggunakan penapis d

</details>

**teach-aws (H3):** Enhanced Monitoring menyediakan satu set metrik yang dibentuk sebagai muatan JSON yang dihantar ke akaun CloudWatch Logs anda. Muatan JSON dihantar pada granulariti yang terakhir dikonfigurasikan untuk instance Amazon RDS. Terdapat dua cara anda boleh menggunakan metrik melalui papan pemuka atau aplikasi pihak ketiga. Alat pemantauan boleh menggunakan Langganan CloudWatch Logs untuk menyediakan suapan hampir masa nyata untuk metrik. Sebagai alternatif, anda boleh menggunakan penapis dalam CloudWatch Logs untuk memindahkan metrik ke CloudWatch dan mengintegrasikan aplikasi anda dengan CloudWatc


**teach-aws (D, flexible):** Amazon RDS Enhanced Monitoring menyediakan satu set metrik yang dipisahkan secara logik merangkumi: CPU, memori, sistem fail, dan I/O cakera; rangkaian; dan metrik berkaitan dengan instance Amazon RDS. Setiap metrik mempunyai granulariti yang berbeza – granulariti 1 saat secara lalai, atau pilihan untuk menggunakan granulariti tinggi sehingga 10 saat. Metrik ini dihantar ke Amazon CloudWatch, yang membolehkan anda menggunakan alat CloudWatch dengan mudah untuk memahami kesihatan instance Amazon RDS anda. Alat pemantauan boleh memanfaatkan CloudWatch Metrics untuk mencipta papan pemuka, pengger


**PixelSpaceAI 7B LoRA:** Anda boleh mengintegrasikan Enhanced Monitoring dengan alat yang anda gunakan pada masa ini dengan memasukkan metrik yang dijana oleh Enhanced Monitoring ke dalam alat tersebut. Metrik yang dijana oleh Enhanced Monitoring tersedia dalam format OpenMetrics dan boleh diimport ke dalam mana-mana alat yang menyokong OpenMetrics.


<details><summary>mesolitica 7B base</summary>

Untuk mengintegrasikan Enhanced Monitoring dengan alat yang anda gunakan pada masa ini, anda perlu mengikuti langkah-langkah berikut:

1. **Pilih Alat Sumber**: Pastikan alat yang anda gunakan pada masa ini mempunyai sokongan untuk integrasi dengan Enhanced Monitoring. Ini biasanya dilakukan melalui API atau SDK yang disediakan oleh Enhanced Monitoring.

2. **Baca Dokumentasi**: Baca dokumentasi yang disediakan oleh Enhanced Monitoring untuk memahami bagaimana integrasi dengan alat anda boleh dilakukan. Dokumentasi ini biasanya akan memberikan panduan langkah demi langkah tentang bagaimana unt

</details>


## dynamodb

**Q:** Adakah point-in-time recovery tersedia pada global tables DynamoDB?

<details><summary>reference</summary>

Ya, anda boleh mendayakan point-in-time recovery pada setiap replika global table DynamoDB.

</details>

**teach-aws (H3):** Ya, anda boleh mendayakan point-in-time recovery pada setiap replika global table DynamoDB.


**teach-aws (D, flexible):** Ya, anda boleh mendayakan point-in-time recovery pada setiap replika global table DynamoDB.


**PixelSpaceAI 7B LoRA:** Ya. Global tables DynamoDB menyokong point-in-time recovery pada semua replika global. Point-in-time recovery tersedia pada replika global yang dicipta selepas 31 Januari 2023.


<details><summary>mesolitica 7B base</summary>

Ya, point-in-time recovery (PITR) tersedia untuk global tables DynamoDB. Dengan menggunakan PITR, anda boleh memulihkan data dari sebarang titik masa dalam masa 31 hari terakhir. Ini membolehkan anda memulihkan data ke keadaan sebelum perubahan atau kegagalan yang tidak diingini.

</details>
