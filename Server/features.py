from flask_mysqldb import MySQLdb
from flask import jsonify, make_response, request

# Enter your database connection details below
conn = MySQLdb.connect("localhost","root","18agustus98","atm")

#################################################################################
#                               1. LOGIN FUNCTION                               #
#################################################################################

def login_func(mysql):
    # Fungsi Untuk Melakukan Login dari Client
    # Fungsi ini akan melakukan komparasi data POST (JSON) yang disampaikan Client yang berisi
    # data hash function yang digenerate Client saat login dengan database pada Server
    #
    # Menerima data berformat JSON dengan isi:
    # - user_id : (No rekening)
    # - pass (hash code)
    #
    # Mengembalikan return data berformat JSON dengan isi :
    # - status (success(1)/failed(0))
    # - nama_nasabah (str)
    # - no_rek (int)
    #
    # Dan juga variabel :
    # - id_nasabah (int)
    # - no_rek (int)
    #
    # Apabila data yang dikirim salah, maka server akan membalikan data JSON:
    # - status : 0
    # - nama_nasabah : not_found
    #
    # Dan juga variabel :
    # - id_nasabah : None
    # - no_rek (int) : None

    req = request.get_json()
    cur = conn.cursor()
    no_rek = req.get("user_id")

    # Magic code = Auth/Hash code sent from client
    # Checking magic code on database
    select_stmt = "SELECT id_nasabah " \
                  "FROM auth " \
                  "WHERE magic_code =  %(magic_code)s"
    cur.execute(select_stmt, {'magic_code': req.get("pass")})
    id = cur.fetchall()

    # If Login Correct
    if len(id) == 1 :
        select_stmt = "SELECT nama, no_rek " \
                      "FROM nasabah " \
                      "WHERE id_nasabah =  %(id_nasabah)s"
        cur.execute(select_stmt, {'id_nasabah': id[0][0]})
        user = cur.fetchall()
        id_nasabah = id[0][0]
        no_rek_get = user[0][1]

        if no_rek_get == no_rek:
            response = {
                "status": 1,  # Success
                "nama_nasabah": user[0][0], # nama_nasabah
            }
            res = make_response(jsonify(response), 200)
            return res, id_nasabah, no_rek_get

        # Login Incorrect
        else:
            response = {
                "status": 0,
                "nama_nasabah": "not_found",
            }
            res = make_response(jsonify(response), 400)
            id_nasabah = None
            no_rek = None

            return res, id_nasabah, no_rek

    # If Login Incorrect
    else:
        response = {
            "status": 0,
            "nama_nasabah": "not_found",
        }
        res = make_response(jsonify(response), 400)
        id_nasabah = None
        no_rek = None

        return res, id_nasabah, no_rek

#################################################################################
#                   2. CHECK TRANSFER DESTINATION FUNCTION                      #
#################################################################################

def check_trans(mysql, no_rek):
    # Fungsi untuk melakukan cek rekening destinasi transfer
    # Fungsi ini akan melakukan cek data POST (JSON) yang disampaikan Client dan
    # dan menyimpan historinya dalam database
    #
    # Menerima data jason dengan parameter :
    # - no_rek_tujuan (int)
    #
    # Mengembalikan return data berformat JSON dengan isi :
    # - status (success(1)/failed(0))
    # - message (Nama Rekening Tujuan/Rekening Tujuan Tidak Ditemukan/Error, Ini No Rekening Anda Sendiri)

    req = request.get_json()
    cur = conn.cursor()

    rek_tujuan = req.get("no_rek_tujuan")

    # Ketika User Memasukkan No Rekeningnya Sendiri sebagai Tujuan
    if rek_tujuan == no_rek :
        response = {
            "status"    : 0, # Failed
            "message"   : "Error, Ini No Rekening Anda Sendiri"
        }
        res = make_response(jsonify(response), 400)
        return res

    else :
        # Cek Tujuan
        select_stmt = "SELECT id_nasabah, no_rek, nama " \
                      "FROM nasabah " \
                      "WHERE no_rek =  %(no_rek_tujuan)s"
        cur.execute(select_stmt, {'no_rek_tujuan': rek_tujuan})
        result = cur.fetchall()

        # Ketika Rekening Tujuan Ditemukan
        if len(result) == 1 :
            nama = result[0][2]
            response = {
                "status"    : 1, # Success
                "message"   : nama
            }
            res = make_response(jsonify(response), 200)
            return res
        # Ketika Rekening Tujuan Tidak Ditemukan
        else:
            response = {
                "status"    : 0, # Failed
                "message"   : "Rekening Tujuan Tidak Ditemukan"
            }
            res = make_response(jsonify(response), 400)
            return res



#################################################################################
#                  3. EXECUTE TRANSFER DESTINATION FUNCTION                     #
#################################################################################

def exec_trans(mysql, no_rek):
    # Fungsi untuk melakukan eksekusi transfer antar Client
    # Fungsi ini akan melakukan cek data POST (JSON) yang disampaikan Client dan
    # dan menyimpan historinya dalam database
    #
    # Menerima data jason dengan parameter :
    # - no_rek_tujuan (int)
    # - nominal_trans (int)
    #
    # Mengembalikan return data berformat JSON dengan isi :
    # - status (success(1)/failed(0))
    # - message (Transaksi Berhasil/Rekening Tujuan Tidak Ditemukan/Saldo Anda Kurang)

    req = request.get_json()
    cur = conn.cursor()

    rek_tujuan = req.get("no_rek_tujuan")
    nominal_trans = req.get("nominal_trans")

    # Penerima

    select_stmt = "SELECT id_nasabah " \
                  "FROM nasabah " \
                  "WHERE no_rek =  %(no_rek_tujuan)s "
    cur.execute(select_stmt, {'no_rek_tujuan': rek_tujuan})
    penerima = cur.fetchall()

    #Pengirim
    select_stmt = "SELECT n.id_nasabah, no_rek, saldo " \
                  "FROM nasabah n " \
                  "JOIN saldo s ON n.id_nasabah = s.id_nasabah " \
                  "WHERE n.no_rek =  %(no_rek)s "
    cur.execute(select_stmt, {'no_rek': no_rek})
    pengirim = cur.fetchall()
    id_pengirim = pengirim[0][0]

    # Ketika Rekening Tujuan Ditemukan dan Saldo >= dari yang ditransfer
    if rek_tujuan == no_rek :
        response = {
            "status"    : 0, # Failed
            "message"   : "Error, Ini No Rekening Anda Sendiri"
        }
        res = make_response(jsonify(response), 400)
        return res

    else :
        if (len(penerima) == 1) and pengirim[0][2] >= nominal_trans:

            id_tujuan = penerima[0][0]
            cur.close()

            # Pengurangan Saldo Pengirim
            cur = conn.cursor()
            select_stmt = "UPDATE saldo "\
                          "SET saldo = saldo - %(nominal_trans)s, "\
                            "last_change = CURRENT_TIMESTAMP "\
                          "WHERE id_nasabah = %(id_pengirim)s; "
            cur.execute(select_stmt, {'nominal_trans': nominal_trans, 'id_pengirim': id_pengirim})
            conn.commit()
            cur.close()

            # Input Histori
            cur = conn.cursor()
            select_stmt = "INSERT INTO `histori_transaksi` " \
                          "VALUES (DEFAULT, %(id_pengirim)s, DEFAULT, 2, %(rek_tujuan)s, %(nominal_trans)s)"
            cur.execute(select_stmt, {'id_pengirim': id_pengirim, 'rek_tujuan': rek_tujuan, 'nominal_trans': nominal_trans})
            conn.commit()
            cur.close()

            # Penambahan Saldo Penerima dan Input Histori
            cur = conn.cursor()
            select_stmt = "UPDATE saldo " \
                          "SET saldo = saldo + %(nominal_trans)s, " \
                            "last_change = CURRENT_TIMESTAMP " \
                          "WHERE id_nasabah = %(id_tujuan)s; "
            cur.execute(select_stmt, {'nominal_trans': nominal_trans, 'id_tujuan': id_tujuan})
            conn.commit()
            cur.close()

            # Input Histori
            cur = conn.cursor()
            select_stmt = "INSERT INTO `histori_transaksi` " \
                          "VALUES (DEFAULT, %(id_tujuan)s, DEFAULT, 3, %(rek_pengirim)s, %(nominal_trans)s)"
            cur.execute(select_stmt, {'id_tujuan': id_tujuan, 'rek_pengirim': no_rek, 'nominal_trans' : nominal_trans})
            conn.commit()
            cur.close()

            # Send Response to Client
            response = {
                "status": 1,# Success
                "message": "Transaksi Berhasil"
            }
            res = make_response(jsonify(response), 200)
            return res


        elif pengirim[0][2] < nominal_trans:
            response = {
                "status": 0, # Failed
                "message": "Saldo Anda Kurang"
            }
            res = make_response(jsonify(response), 400)
            return res

        else:
            response = {
                "status": 0,# Failed
                "message": "Rekening Tujuan Tidak Ditemukan"
            }
            res = make_response(jsonify(response), 400)
            return res


#################################################################################
#                            4. CEK SALDO FUNCTION                              #
#################################################################################
def cek_saldo(mysql, no_rek):
    # Fungsi untuk melakukan cek Saldo client
    # Fungsi ini akan melakukan cek data GET (JSON) yang disampaikan Client dan
    # dan memberikan balasan data histori akun tersebut
    #
    # Menerima data variabel dari session :
    # - no_rek (int)
    #
    # Mengembalikan return data berformat JSON dengan isi :
    # - status (success(1)/failed(0))
    # - saldo (str -> Rp x,xxx,xxx.xx)

    req = request.get_json()
    cur = conn.cursor()

    select_stmt = "SELECT no_rek, FORMAT(saldo,2) " \
                  "FROM saldo s " \
                  "JOIN nasabah n ON s.id_nasabah = n.id_nasabah "\
                  "WHERE no_rek = %(no_rek)s "
    cur.execute(select_stmt, {'no_rek': no_rek})
    result = cur.fetchall()
    cur.close()

    # Send Response to Client
    response = {
        "status": 1,
        "saldo": "Rp " + str(result[0][1])
    }
    res = make_response(jsonify(response), 200)
    return res


#################################################################################
#                      5. CEK HISTORI TRANSAKSI FUNCTION                        #
#################################################################################
def history(mysql, no_rek):
    # Fungsi untuk melakukan cek histori 10 transaksi terakhir dari client
    # Fungsi ini akan melakukan cek data GET (JSON) yang disampaikan Client dan
    # dan memberikan balasan data histori akun tersebut
    #
    # Menerima data variabel dari session :
    # - no_rek (int)
    #
    # Mengembalikan return data berformat JSON berupa list (history) dictionary/transaksi dengan isi :
    # - status (success(1)/failed(0))
    # - timestamp
    # - jenis_trans (ISI SALDO/ TRANSFER MASUK/ TRANSFER KELUAR)
    # - jumlah_transaksi (str -> x,xxx,xxx.xx)
    # - rek_tujuan_atau_asal (int)
    #
    # contoh balasan:
    # {
    #   "history": [
    #     {
    #       "jumlah_transaksi": "5,000,000.00",
    #       "nama": "ISI SALDO",
    #       "rek_asal_atau_tujuan": null,
    #       "timestamp": "Sat, 18 Apr 2020 20:34:40 GMT"
    #     },
    #     {
    #       "jumlah_transaksi": "100,000.00",
    #       "nama": "TRANSFER KELUAR",
    #       "rek_asal_atau_tujuan": 13216072,
    #       "timestamp": "Sun, 19 Apr 2020 22:58:09 GMT"
    #   ]
    #   "status": 1
    # }
    #
    # Dan mengembalikan List kosong apabila tidak ada histori transaksi

    req = request.get_json()
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    select_stmt = "SELECT " \
                  "timestamp, k.nama, FORMAT(jumlah_transaksi,2) AS 'jumlah_transaksi', rek_asal_atau_tujuan " \
                  "FROM histori_transaksi h " \
                  "JOIN nasabah n ON h.id_nasabah = n.id_nasabah " \
                  "JOIN list_kode_transaksi k ON h.kode_transaksi = k.kode_transaksi " \
                  "WHERE no_rek = %(no_rek)s " \
                  "ORDER BY timestamp DESC " \
                  "LIMIT 10"
    cur.execute(select_stmt, {'no_rek': no_rek})
    result = cur.fetchall()
    cur.close()
    last_row = len(result)

    # Send Response to Client
    response = {
        "status": 1,
        "history": result[0:last_row],
    }
    res = make_response(jsonify(response), 200)
    return res

