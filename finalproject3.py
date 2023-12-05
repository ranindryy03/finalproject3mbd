import streamlit as st
from sqlalchemy import text

list_bank = ['', 'BCA', 'BRI', 'BNI', 'MANDIRI', 'BTN', 'BSI']
list_gender = ['', 'male', 'female']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://avindalutfiapb17:VNvKwPZaJ32O@ep-snowy-heart-34856175.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SCHEDULE (id serial, bank_name varchar, nasabah_name varchar, gender char(25), \
                                                       jenis_tabungan varchar, rekening varchar, alamat text, tanggal_pembuatan date);')
    session.execute(query)

st.header('DATABASE NASABAH BANK')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO schedule (bank_name, nasabah_name, gender, jenis_tabungan, rekening, alamat, waktu_pembuatan, tanggal_pembuatan) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        bank_name_lama = result["bank_name"]
        nasabah_name_lama = result["nasabah_name"]
        gender_lama = result["gender"]
        jenis_tabungan_lama = result["jenis_tabungan"]
        rekening_lama = result["rekening"]
        alamat_lama = result["alamat"]
        waktu_pembuatan_lama = result["waktu_pembuatan"]
        tanggal_pembuatan_lama = result["tanggal_pembuatan"]

        with st.expander(f'a.n. {nasabah_name_lama}'):
            with st.form(f'data-{id}'):
                bank_name_baru = st.selectbox("bank_name", list_bank, list_bank.index(bank_name_lama))
                nasabah_name_baru = st.text_input("nasabah_name", nasabah_name_lama)
                gender_baru = st.selectbox("gender", list_gender, list_gender.index(gender_lama))
                jenis_tabungan_baru = st.multiselect("jenis_tabungan", ['gold', 'platinum'], eval(jenis_tabungan_lama))
                rekening_baru = st.text_input("rekening", rekening_lama)
                alamat_baru = st.text_input("alamat", alamat_lama)
                waktu_pembuatan_baru = st.time_input("waktu_pembuatan", waktu_pembuatan_lama)
                tanggal_pembuatan_baru = st.date_input("tanggal_pembuatan", tanggal_pembuatan_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE schedule \
                                          SET bank_name=:1, nasabah_name=:2, gender=:3, jenis_tabungan=:4, \
                                          rekening=:5, alamat=:6, waktu_pembuatan=:7, tanggal_pembuatan=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':bank_name_baru, '2':nasabah_name_baru, '3':gender_baru, '4':str(jenis_tabungan_baru), 
                                                    '5':rekening_baru, '6':alamat_baru, '7':waktu_pembuatan_baru, '8':tanggal_pembuatan_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM schedule WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()