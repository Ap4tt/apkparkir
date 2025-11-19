import datetime
import time
import os

# ====== SISTEM LOGIN ======
password = "123456"
percobaan = 0

while True:
    pw = input("\nMasukkan Password Untuk Masuk Ke Program : ")
    if pw == password:
        print("Login Berhasil!")
        break
    else:
        percobaan += 1
        print("Password Salah!")
        if percobaan == 5:
            print("Terlalu Banyak Percobaan Gagal. Aplikasi Ditutup.")
            exit()
            
# ====== DATA DASAR ======
slotMOBIL = [f"MBL-{i + 1:02d}" for i in range(10)]
slotMOTOR = [f"MTR-{i + 1:02d}" for i in range(15)]
slotTRUK = [f"TRU-{i + 1:02d}" for i in range(5)]
slotBUS = [f"BUS-{i + 1:02d}" for i in range(5)]

TARIF = {"Mobil": 3000, 
         "Motor": 2000, 
         "Truk" : 5000,
         "Bus" : 7000}

member = ["B1945JKW", 
          "B2025GBR", 
          "B1998PBW"]

slot = {s: None for s in slotMOBIL + slotMOTOR + slotTRUK + slotBUS}

data = {}

# ====== PROGRAM UTAMA ======
while True:
    print("""
==== SISTEM PARKIR ====
1. Tap In
2. Tap Out
3. Cek Durasi
4. Lihat Slot
5. Keluar""")
    pilihan = input("Pilih Menu (1/2/3/4/5) : ").strip()

    # ------------------ TAP IN ------------------
    if pilihan == "1":
        plat = input("\nMasukkan Plat Nomor : ").upper().strip().replace(" ","")

        if plat in data:
            print("\n==============================")
            print("\033[1;31mPlat Nomor Ini Sudah Di Dalam!\033[0m")
            print("==============================\n")
            continue
        else:
            print("""
Jenis Kendaraan : 
1. Mobil
2. Motor
3. Truk
4. Bus""")

        while True:
            jenis = input("Pilih Jenis Kendaraan (1/2/3/4): ").strip()
            if jenis == "1":
                jenis = "Mobil"
                kode = "MBL"
                break
            elif jenis == "2":
                jenis = "Motor"
                kode = "MTR"
                break
            elif jenis == "3":
                jenis = "Truk"
                kode = "TRU"
                break
            elif jenis == "4":
                jenis = "Bus"
                kode = "BUS"
                break
            else:
                print("\n=====================================================")
                print("\033[1;31mPilihan Tidak Valid. Silahkan Masukkan Pilihan 1 - 4!\033[0m")
                print("=====================================================\n")
                continue

        slotKOSONG = None
        for s in slot:
            if s.startswith(kode) and slot[s] is None:
                slotKOSONG = s
                break

        if slotKOSONG is None:
            print("\n===========")
            print("\033[1;31mSlot Penuh!\033[0m")
            print("===========")
        else:
            waktuMASUK = datetime.datetime.now()
            slot[slotKOSONG] = plat
            data[plat] = {
            "in": waktuMASUK,
            "jenis": jenis,
            "slot": slotKOSONG
            }
            if plat in member:
                status = "MEMBER"
            else:
                status = "REGULAR"
                
            print("\n======== TAP IN ========")
            print(f"Plat        : {plat}")
            print(f"Jenis       : {jenis}")
            print(f"Slot        : {slotKOSONG}")
            print(f"Waktu Masuk : {waktuMASUK.strftime('%H:%M:%S')}")
            print(f"Status      : {status}")
            print("========================")
                
    # ------------------ TAP OUT ------------------
    elif pilihan == "2":
        plat = input("\nMasukkan Plat Nomor : ").upper().strip().replace(" ","")

        if plat not in data:
            print("\n===============================")
            print("\033[1;31mData Kendaraan Tidak Ditemukan!\033[0m")
            print("===============================")
            continue
        else:
            waktuKELUAR = datetime.datetime.now()
            waktuMASUK = data[plat]["in"]
            jenis = data[plat]["jenis"]
            slotPARKIR = data[plat]["slot"]

            selisih = waktuKELUAR - waktuMASUK
            durasiDETIK = selisih.total_seconds()
            durasiJAM = int(durasiDETIK // 3600)
            sisaMENIT = int((durasiDETIK % 3600) // 60)

            jamPARKIR = durasiJAM + (1 if sisaMENIT > 0 else 0)
            if jamPARKIR == 0:
                jamPARKIR = 1

            tarifPER_JAM = TARIF[jenis]
            total = tarifPER_JAM * jamPARKIR

            if plat in member:
                total = total - (total * 20 / 100)

            print("\n======== TAP OUT ========")
            print(f"Plat        : {plat}")
            print(f"Jenis       : {jenis}")
            print(f"Slot        : {slotPARKIR}")
            print(f"Durasi      : {durasiJAM} Jam {sisaMENIT} Menit")
            print(f"Total Bayar : Rp.{total:,.0f}")
            print("=========================")
            
        print("\n===================")
        print("Metode Pembayaran :")
        print("===================")
        print("1. Cash")
        print("2. QR")

        while True:
            metode = input("Pilih metode (1/2): ").strip()

            if metode == "1":
                while True:
                    uang = int(input("\nMasukkan Jumlah Uang Tunai : "))
                    
                    if uang < total:
                        print("==============================================")
                        print("\033[1;31mUang Kurang! Harap Masukkan Jumlah Yang Cukup.\033[0m")
                        print("==============================================")
                        continue
                    else:
                        kembalian = uang - total
                        print("\n=========================")
                        print("\033[1;32m{:^25}\033[0m".format("Pembayaran Berhasil!"))
                        print("=========================")
                        print(f"Total Bayar  : Rp.{total:,.0f}")
                        print(f"Uang Dibayar : Rp.{uang:,.0f}")
                        print(f"Kembalian    : Rp.{kembalian:,.0f}")
                        print("=========================")
                        break
                break

            elif metode == "2":
                time.sleep(2)
                print("\n==============================")
                print("\033[1;32m{:^30}\033[0m".format("Pembayaran QRIS Berhasil!"))
                print("==============================")
                break

            else:
                print("\n===================================================")
                print("\033[1;31mPilihan Tidak Valid! Silakan pilih 1 (Cash) atau 2 (QR).\033[0m")
                print("===================================================")

            slot[slotPARKIR] = None
            del data[plat]

    # ------------------ CEK DURASI ------------------
    elif pilihan == "3":
        plat = input("\nMasukkan Plat Nomor : ").upper().strip().replace(" ","")

        if plat not in data:
            print("\n==========================")
            print("\033[1;31mKendaraan Tidak Ditemukan!\033[0m")
            print("==========================")
        else:
            waktuMASUK = data[plat]["in"]
            try:
                while True:
                    waktuSEKARANG = datetime.datetime.now()
                    selisih = waktuSEKARANG - waktuMASUK
                    h, sisa = divmod(selisih.seconds, 3600)
                    m, d = divmod(sisa, 60)
                    os.system("cls" if os.name == "nt" else "clear")
                  
                    print(f"======== {plat} ========")
                    print(f"Waktu Masuk     : {waktuMASUK.strftime('%H:%M:%S')}")
                    print(f"Waktu Sekarang  : {waktuSEKARANG.strftime('%H:%M:%S')}")
                    print(f"Durasi Parkir   : {h} Jam {m} Menit {d} Detik")
                    print("\nCTRL + C Untuk Keluar")
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n")


    # ------------------ LIHAT SLOT ------------------
    elif pilihan == "4":
        while True:
            print("""
========= LIHAT SLOT PARKIR =========
Pilih Jenis Slot Yang Ingin Dilihat :
1. Mobil
2. Motor
3. Truk
4. Bus
5. Semua""")

            pilihanSLOT = input("Masukkan Pilihan (1/2/3/4/5) : ")

            slotMAP = {
                "1" : "MBL",
                "2" : "MTR",
                "3" : "TRU",
                "4" : "BUS",
                "5" : None
            }

            if pilihanSLOT not in slotMAP:
                print("\n=====================================================")
                print("\033[1;31mPilihan Tidak Valid. Silahkan Masukkan Pilihan 1 - 5!\033[0m")
                print("=====================================================")
                continue
            else:
                prefix = slotMAP[pilihanSLOT]
                print("\n======= STATUS SLOT PARKIR =======")
                for s, p in slot.items():
                    if prefix is None or s.startswith(prefix):
                        status = ("\033[1;31mKosong\033[0m" if p is None else f"\033[1;32m{p}\033[0m")
                        print(f"{s} : {status}")
                print()
                break

    # ------------------ KELUAR ------------------
    elif pilihan == "5":
        print("\n===================================")
        print("\033[1;34mTerima Kasih! Hati - Hati Di Jalan!\033[0m")
        print("===================================")
        break

    else:
        print("\n=====================================================")
        print("\033[1;31mPilihan Tidak Valid. Silahkan Masukkan Pilihan 1 - 5!\033[0m")

        print("=====================================================")
