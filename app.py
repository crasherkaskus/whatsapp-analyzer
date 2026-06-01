import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import datetime
import random

# Import modular helper functions
from src.parser import parse_chat_data
import src.analyzer as analyzer

# Set Page Config
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Custom main font and header style */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #25D366, #128C7E, #075E54);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
        padding-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    
    /* Dashboard card metric */
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        border: 1px solid #E9ECEF;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.05);
        border-color: #25D366;
    }
    
    .metric-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1F2937;
        margin: 0;
    }
    
    .metric-lbl {
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Guide section styling */
    .guide-card {
        background-color: rgba(37, 211, 102, 0.06);
        border: 1px solid rgba(37, 211, 102, 0.2);
        border-left: 5px solid #25D366;
        padding: 1.8rem;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.01);
        margin-bottom: 1.5rem;
    }
    
    .guide-card h4 {
        color: #128C7E !important;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.25rem;
    }
    
    .guide-card ol {
        margin: 0;
        padding-left: 1.2rem;
    }
    
    .guide-card ol li {
        margin-bottom: 0.6rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Podium Leaderboard Styling */
    .podium-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 1.5rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .podium-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #E5E7EB;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 220px;
        transition: transform 0.3s ease;
    }
    
    .podium-card:hover {
        transform: translateY(-5px);
    }
    
    .podium-first {
        border-top: 5px solid #FFD700;
        height: 250px;
        justify-content: space-between;
    }
    
    .podium-second {
        border-top: 5px solid #C0C0C0;
        height: 210px;
        justify-content: space-between;
    }
    
    .podium-third {
        border-top: 5px solid #CD7F32;
        height: 180px;
        justify-content: space-between;
    }
    
    .podium-rank-badge {
        font-size: 2rem;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .podium-author {
        font-weight: 800;
        font-size: 1.2rem;
        color: #1F2937;
        word-break: break-word;
    }
    
    .podium-count {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2b6cb0;
        margin-top: 0.5rem;
    }
    
    .podium-lbl {
        font-size: 0.75rem;
        color: #9CA3AF;
        font-weight: 600;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to generate rich realistic sample chat data
def generate_sample_chat_log():
    users = ["Ahmad Fauzi", "Siti Rahma", "Budi Santoso", "Dewi Lestari", "Rian Hidayat", "Lina Marlina"]
    messages = [
        "Halo semuanya! Selamat pagi. Bagaimana kabar projek hari ini?",
        "Pagi juga! Ada agenda penting apa hari ini?",
        "Hari ini kita ada koordinasi jam 10:00 WIB ya.",
        "Oke siap, nanti saya siapkan dashboard visualisasinya.",
        "Jangan lupa kirim tautan Zoom-nya ya Siti.",
        "Siap, nanti segera dikirimkan. 👍",
        "Eh, lihat berita tech terbaru ini gak? Keren banget.",
        "Berita yang mana tuh? Kirim tautannya dong Budi.",
        "Ini dia artikel lengkapnya: https://techcrunch.com/whatsapp-updates",
        "Wah menarik sekali ya fitur barunya! Makasih infonya.",
        "Sama-sama! Semoga bermanfaat untuk semuanya. 😁",
        "Hahaha lucu banget sih ini sticker-nya.",
        "<Media tidak dicantumkan>",
        "Wkwkwk iya bener banget, kocak abis.",
        "<Media tidak dicantumkan>",
        "Pesan ini telah dihapus",
        "Eh maaf salah kirim grup chat 🙏",
        "Waduh ada gosip seru apa lagi nih?",
        "Hush, jangan mulai bergosip pagi-pagi 😂",
        "Koordinasi nanti jadi diundur atau tetap jam 10?",
        "Tetap jam 10 kok, ini link-nya: https://meet.google.com/abc-defg-hij",
        "Mantap Siti! Rian mana nih kok belum merespon?",
        "Rian paling masih mimpi wkwk.",
        "Hadir! Enak saja, saya sudah bangun dari subuh ya 😜",
        "Alibi terus Rian haha.",
        "Nanti sore ada yang berminat ngopi bareng?",
        "Kuy! Di tempat biasa ya, kafe pojokan.",
        "Ikut dong! Ajak Dewi juga ya.",
        "Boleh, nanti saya konfirmasi jam kumpulnya.",
        "Siap, kabari segera di grup ya!",
        "Ok, aman."
    ]
    
    start_date = datetime.datetime.now() - datetime.timedelta(days=95)
    current_time = start_date
    lines = []
    
    for i in range(800):
        # random date/time increments
        current_time += datetime.timedelta(hours=random.randint(0, 4), minutes=random.randint(1, 59))
        if current_time > datetime.datetime.now():
            break
            
        date_str = current_time.strftime("%d/%m/%Y")
        time_str = current_time.strftime("%H:%M")
        
        user = random.choice(users)
        msg = random.choice(messages)
        
        # Add system messages periodically
        if i == 0:
            line = f"{date_str}, {time_str} - Anda bergabung menggunakan tautan undangan grup ini"
        elif random.random() < 0.04:
            new_joined = random.choice(["Andi Wijaya", "Rina Amelia", "Joko Susilo"])
            line = f"{date_str}, {time_str} - {new_joined} bergabung menggunakan tautan undangan grup ini"
        else:
            line = f"{date_str}, {time_str} - {user}: {msg}"
            
        lines.append(line)
        
    return "\n".join(lines)

# Application state for chat text
if "chat_text" not in st.session_state:
    st.session_state.chat_text = None
if "filename" not in st.session_state:
    st.session_state.filename = None

# Sidebar Content
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", width=70)
    st.title("WhatsApp Analyzer")
    st.markdown("Analisis data chat grup Anda secara interaktif dan instan.")
    st.markdown("---")
    
    # File Uploader
    uploaded_file = st.file_uploader("Unggah file chat (.txt)", type=["txt"])
    
    if uploaded_file is not None:
        st.session_state.chat_text = uploaded_file.read().decode("utf-8")
        st.session_state.filename = uploaded_file.name
        st.success(f"Berhasil mengunggah: {uploaded_file.name}")
        
    st.markdown("### Atau Coba Aplikasi:")
    if st.button("✨ Gunakan Data Contoh Grup"):
        st.session_state.chat_text = generate_sample_chat_log()
        st.session_state.filename = "Grup_WhatsApp_Contoh.txt"
        st.success("Menggunakan data simulasi grup!")
        
    if st.session_state.chat_text:
        if st.button("🗑️ Reset Aplikasi"):
            st.session_state.chat_text = None
            st.session_state.filename = None
            st.rerun()

# Main Application Layout
st.markdown("<div class='main-title'>💬 WhatsApp Group Chat Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Temukan insight menarik dari riwayat obrolan grup WhatsApp Anda secara instan dan premium</div>", unsafe_allow_html=True)

if st.session_state.chat_text is None:
    # Beautiful Hero Banner
    st.markdown("""
    <div style='text-align: center; padding: 2.5rem 1.5rem; background: linear-gradient(135deg, rgba(37, 211, 102, 0.08), rgba(18, 140, 126, 0.04)); border-radius: 20px; border: 1px solid rgba(37, 211, 102, 0.15); margin-bottom: 2.5rem;'>
        <h2 style='font-size: 2.2rem; font-weight: 800; color: #128C7E; margin-top: 0; margin-bottom: 0.8rem;'>🚀 Siap Menganalisis Grup WhatsApp Anda?</h2>
        <p style='font-size: 1.1rem; color: #6c757d; max-width: 750px; margin: 0 auto 1.8rem auto; line-height: 1.6;'>
            Dapatkan statistik percakapan mendalam, lacak bukti foto transaksi, lihat siapa anggota teraktif, temukan kata kunci populer, hingga pola keaktifan waktu secara aman dan instan.
        </p>
        <div style='display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;'>
            <span style='background-color: #25D366; color: white; padding: 0.6rem 1.2rem; border-radius: 30px; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px rgba(37,211,102,0.25); display: inline-block;'>
                👈 Unggah File Teks (.txt) di Sidebar
            </span>
            <span style='background-color: #128C7E; color: white; padding: 0.6rem 1.2rem; border-radius: 30px; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 12px rgba(18,140,126,0.25); display: inline-block;'>
                ✨ Klik 'Gunakan Data Contoh Grup'
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature showcase
    st.markdown("### 🛠️ Fitur Utama Dashboard")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        st.markdown("""
        <div style='padding: 1.5rem; background: rgba(37, 211, 102, 0.04); border-radius: 16px; border: 1px solid rgba(37, 211, 102, 0.1); height: 100%; text-align: center;'>
            <div style='font-size: 2.8rem; margin-bottom: 0.8rem;'>📊</div>
            <h5 style='font-weight: 800; color: #128C7E; margin-top: 0; margin-bottom: 0.6rem; font-size: 1.1rem;'>Statistik Lengkap</h5>
            <p style='font-size: 0.85rem; color: #6B7280; line-height: 1.5; margin: 0;'>Metrik total chat, total kata, tautan, hingga persentase kontribusi setiap anggota grup secara detail.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div style='padding: 1.5rem; background: rgba(18, 140, 126, 0.04); border-radius: 16px; border: 1px solid rgba(18, 140, 126, 0.1); height: 100%; text-align: center;'>
            <div style='font-size: 2.8rem; margin-bottom: 0.8rem;'>💼</div>
            <h5 style='font-weight: 800; color: #128C7E; margin-top: 0; margin-bottom: 0.6rem; font-size: 1.1rem;'>Laporan Transaksi</h5>
            <p style='font-size: 0.85rem; color: #6B7280; line-height: 1.5; margin: 0;'>Tab khusus pelacakan bukti transaksi foto per anggota grup dengan visualisasi podium TOP 3 yang premium.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div style='padding: 1.5rem; background: rgba(37, 211, 102, 0.04); border-radius: 16px; border: 1px solid rgba(37, 211, 102, 0.1); height: 100%; text-align: center;'>
            <div style='font-size: 2.8rem; margin-bottom: 0.8rem;'>⏰</div>
            <h5 style='font-weight: 800; color: #128C7E; margin-top: 0; margin-bottom: 0.6rem; font-size: 1.1rem;'>Pola Waktu & Heatmap</h5>
            <p style='font-size: 0.85rem; color: #6B7280; line-height: 1.5; margin: 0;'>Analisis jam paling ramai chat, distribusi hari dalam seminggu, serta heatmap keaktifan grup 2D.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f4:
        st.markdown("""
        <div style='padding: 1.5rem; background: rgba(18, 140, 126, 0.04); border-radius: 16px; border: 1px solid rgba(18, 140, 126, 0.1); height: 100%; text-align: center;'>
            <div style='font-size: 2.8rem; margin-bottom: 0.8rem;'>🔒</div>
            <h5 style='font-weight: 800; color: #128C7E; margin-top: 0; margin-bottom: 0.6rem; font-size: 1.1rem;'>100% Aman & Privat</h5>
            <p style='font-size: 0.85rem; color: #6B7280; line-height: 1.5; margin: 0;'>Data chat Anda tidak pernah dikirim ke server. Pemrosesan dilakukan sepenuhnya secara lokal dan aman.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Showcase interactive instructions
    st.markdown("### 📖 Panduan Mengekspor Berkas Chat WhatsApp")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='guide-card'>
            <h4>📱 Cara Ekspor Chat dari Android:</h4>
            <ol>
                <li>Buka grup WhatsApp yang dituju.</li>
                <li>Ketuk menu <b>Tiga Titik</b> di pojok kanan atas.</li>
                <li>Pilih <b>Lainnya (More)</b> &rarr; <b>Ekspor chat (Export chat)</b>.</li>
                <li>Pilih <b>Tanpa Media (Without Media)</b> agar ekspor lebih cepat.</li>
                <li>Simpan file <code>.txt</code> hasil ekspor dan unggah di sini!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='guide-card'>
            <h4>🍏 Cara Ekspor Chat dari iOS (iPhone):</h4>
            <ol>
                <li>Buka grup WhatsApp yang dituju.</li>
                <li>Ketuk <b>Nama Grup</b> di bagian atas untuk info grup.</li>
                <li>Gulir ke bawah dan pilih <b>Ekspor Chat (Export Chat)</b>.</li>
                <li>Pilih opsi <b>Tanpa Media (Without Media)</b>.</li>
                <li>Simpan file <code>.txt</code> ke Files, lalu unggah di sini!</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    # Additional aesthetics
    st.info("💡 **Privasi Terjamin:** Semua pemrosesan data dilakukan sepenuhnya secara lokal di browser & server sesi Anda. Chat Anda tidak akan pernah disimpan di server mana pun.")
    
else:
    # Process & Analyze Data
    with st.spinner("Menganalisis data percakapan..."):
        try:
            raw_df = parse_chat_data(st.session_state.chat_text)
        except Exception as e:
            st.error(f"Gagal memproses file. Pastikan file berformat teks WhatsApp ekspor asli. Error: {e}")
            st.stop()
            
    if raw_df.empty:
        st.warning("⚠️ File teks tidak mengandung pesan yang valid atau format tidak dikenali. Silakan pastikan file berformat ekspor chat WhatsApp.")
        st.stop()
        
    # Get filters
    all_months = sorted(raw_df['month_year_str'].unique())
    all_authors = sorted(raw_df[raw_df['is_system'] == False]['author'].unique())
    
    # Filter selection in sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎛️ Filter Laporan")
        selected_month = st.selectbox("Pilih Rentang Bulan:", ["Semua Bulan"] + all_months)
        selected_author = st.selectbox("Pilih Anggota:", ["Semua Anggota"] + all_authors)
        
    # Apply filters
    filtered_df = raw_df.copy()
    if selected_month != "Semua Bulan":
        filtered_df = filtered_df[filtered_df['month_year_str'] == selected_month]
    if selected_author != "Semua Anggota":
        filtered_df = filtered_df[filtered_df['author'] == selected_author]
        
    if filtered_df.empty:
        st.warning("⚠️ Tidak ada data untuk kombinasi filter yang dipilih.")
        st.stop()
        
    # Compute Statistics
    stats = analyzer.get_general_stats(filtered_df)
    
    # Dashboard KPI Cards (Rows of 6 Columns)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>💬</div>
            <div class='metric-val'>{stats['total_messages']:,}</div>
            <div class='metric-lbl'>Total Chat</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>👥</div>
            <div class='metric-val'>{stats['total_users']}</div>
            <div class='metric-lbl'>Partisipan</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>🧾</div>
            <div class='metric-val'>{stats['total_media']:,}</div>
            <div class='metric-lbl'>Total Transaksi</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>🔗</div>
            <div class='metric-val'>{stats['total_links']:,}</div>
            <div class='metric-lbl'>Link Dibagi</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>🗑️</div>
            <div class='metric-val'>{stats['total_deleted']:,}</div>
            <div class='metric-lbl'>Chat Dihapus</div>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-icon'>📝</div>
            <div class='metric-val'>{stats['total_words']:,}</div>
            <div class='metric-lbl'>Total Kata</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Tren & Volume Chat", 
        "🏆 Pemimpin Chat (Leaderboard)", 
        "💼 Laporan Transaksi",
        "⏰ Pola Keaktifan waktu", 
        "💬 Kata Kunci & Emoji"
    ])
    
    # ------------------ Tab 1: Tren & Volume Chat ------------------
    with tab1:
        if selected_month != "Semua Bulan":
            st.markdown(f"### 📈 Tren Percakapan Harian ({selected_month})")
            # Salin DataFrame agar tidak memicu SettingWithCopyWarning
            daily_trend = filtered_df.copy()
            daily_trend['Tanggal'] = daily_trend['datetime'].dt.date
            daily_timeline = daily_trend.groupby('Tanggal').size().reset_index(name='Total Chat')
            daily_timeline = daily_timeline.sort_values(by='Tanggal').set_index('Tanggal')
            st.area_chart(daily_timeline, color="#25D366")
        else:
            st.markdown("### 📈 Tren Percakapan Bulanan (Waktu ke Waktu)")
            # Monthly timeline chart
            timeline_df = analyzer.get_monthly_timeline(filtered_df)
            if not timeline_df.empty:
                # Render using Streamlit Area Chart for modern feel
                timeline_chart_data = timeline_df.set_index('month_year_str')
                st.area_chart(timeline_chart_data, color="#25D366")
            else:
                st.info("Pilih jangkauan waktu yang lebih luas untuk melihat tren bulanan.")
            
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("#### 📅 Keaktifan Chat Berdasarkan Hari")
            daily_df = analyzer.get_daily_activity(filtered_df)
            if not daily_df.empty:
                st.bar_chart(data=daily_df.set_index('Hari')['Total Chat'], color="#128C7E")
                
        with col_t2:
            st.markdown("#### ⏰ Keaktifan Chat Berdasarkan Jam")
            hourly_df = analyzer.get_hourly_activity(filtered_df)
            if not hourly_df.empty:
                st.line_chart(data=hourly_df.set_index('Jam')['Total Chat'], color="#075E54")
                
    # ------------------ Tab 2: Leaderboard Pengirim ------------------
    with tab2:
        st.markdown("### 🏆 Papan Peringkat Anggota Teraktif")
        
        leaderboard_df = analyzer.get_user_leaderboard(filtered_df)
        
        if not leaderboard_df.empty:
            # Let's display visual leaderboard
            top_chatters_chart = leaderboard_df.head(10)[['Author', 'Total Chat']].set_index('Author')
            st.bar_chart(top_chatters_chart, color="#25D366", horizontal=True)
            
            st.markdown("#### 📊 Detail Statistik Anggota")
            # Style the Pandas DataFrame for a clean looking table
            st.dataframe(
                leaderboard_df.style.background_gradient(cmap="Greens", subset=['Total Chat', 'Persentase (%)']),
                width="stretch",
                hide_index=True
            )
            
            # Interactive user details breakdowns
            col_l1, col_l2, col_l3 = st.columns(3)
            with col_l1:
                st.markdown("##### 🗑️ Paling Sering Menghapus Chat")
                deleted_lead = leaderboard_df[['Author', 'Chat Dihapus']].sort_values(by='Chat Dihapus', ascending=False).head(5)
                st.dataframe(deleted_lead, width="stretch", hide_index=True)
                
            with col_l2:
                st.markdown("##### 📷 Pengirim Media Terbanyak")
                media_lead = leaderboard_df[['Author', 'Media Terkirim']].sort_values(by='Media Terkirim', ascending=False).head(5)
                st.dataframe(media_lead, width="stretch", hide_index=True)
                
            with col_l3:
                st.markdown("##### ✍️ Rata-rata Kata per Chat Terpanjang")
                word_lead = leaderboard_df[['Author', 'Rata-rata Kata/Chat']].sort_values(by='Rata-rata Kata/Chat', ascending=False).head(5)
                st.dataframe(word_lead, width="stretch", hide_index=True)
        else:
            st.info("Tidak ada data anggota.")
            
    # ------------------ Tab 3: Laporan Transaksi ------------------
    with tab3:
        st.markdown("### 💼 Laporan Transaksi (Bukti Foto)")
        st.write("Daftar transaksi berdasarkan foto bukti transaksi yang dikirim oleh anggota grup. Chat berupa teks biasa diabaikan.")
        
        tx_leaderboard = analyzer.get_transaction_leaderboard(filtered_df)
        
        if not tx_leaderboard.empty:
            # Let's render the Podium TOP 3 Leaderboard
            st.markdown("#### 🏆 TOP 3 Kontributor Bukti Transaksi")
            
            # Extract Top 3
            top_3 = tx_leaderboard.head(3)
            
            # Reorder for visual podium: [Second, First, Third] if possible
            podium_html = "<div class='podium-container'>"
            
            # Second Place Card
            if len(top_3) >= 2:
                author_2 = top_3.iloc[1]['Author']
                tx_2 = top_3.iloc[1]['Total Transaksi']
                pct_2 = top_3.iloc[1]['Persentase (%)']
                podium_html += f"""<div class='podium-card podium-second'>
<div>
<div class='podium-rank-badge'>🥈</div>
<div class='podium-author'>{author_2}</div>
</div>
<div>
<div class='podium-count'>{tx_2}</div>
<div class='podium-lbl'>Transaksi ({pct_2}%)</div>
</div>
</div>"""
            else:
                podium_html += """<div class='podium-card podium-second' style='opacity: 0.4;'>
<div class='podium-rank-badge'>🥈</div>
<div class='podium-author'>-</div>
<div class='podium-count'>0</div>
<div class='podium-lbl'>Belum ada</div>
</div>"""
                
            # First Place Card
            if len(top_3) >= 1:
                author_1 = top_3.iloc[0]['Author']
                tx_1 = top_3.iloc[0]['Total Transaksi']
                pct_1 = top_3.iloc[0]['Persentase (%)']
                podium_html += f"""<div class='podium-card podium-first'>
<div>
<div class='podium-rank-badge'>🥇</div>
<div class='podium-author' style='font-size:1.4rem;'>{author_1}</div>
</div>
<div>
<div class='podium-count' style='font-size:2.2rem; color:#FFD700;'>{tx_1}</div>
<div class='podium-lbl'>Transaksi ({pct_1}%)</div>
</div>
</div>"""
                
            # Third Place Card
            if len(top_3) >= 3:
                author_3 = top_3.iloc[2]['Author']
                tx_3 = top_3.iloc[2]['Total Transaksi']
                pct_3 = top_3.iloc[2]['Persentase (%)']
                podium_html += f"""<div class='podium-card podium-third'>
<div>
<div class='podium-rank-badge'>🥉</div>
<div class='podium-author'>{author_3}</div>
</div>
<div>
<div class='podium-count'>{tx_3}</div>
<div class='podium-lbl'>Transaksi ({pct_3}%)</div>
</div>
</div>"""
            else:
                podium_html += """<div class='podium-card podium-third' style='opacity: 0.4;'>
<div class='podium-rank-badge'>🥉</div>
<div class='podium-author'>-</div>
<div class='podium-count'>0</div>
<div class='podium-lbl'>Belum ada</div>
</div>"""
                
            podium_html += "</div>"
            st.markdown(podium_html, unsafe_allow_html=True)
            
            # Detailed Stats Table
            st.markdown("#### 📊 Rincian Transaksi Semua Anggota")
            col_tbl, col_chart = st.columns([3, 2])
            
            with col_tbl:
                st.dataframe(
                    tx_leaderboard.style.background_gradient(cmap="Blues", subset=['Total Transaksi', 'Persentase (%)']),
                    width="stretch",
                    hide_index=True
                )
                
            with col_chart:
                tx_chart_data = tx_leaderboard.set_index('Author')['Total Transaksi']
                st.bar_chart(tx_chart_data, color="#2B6CB0")
        else:
            st.info("Tidak ada transaksi bukti foto yang terdeteksi dalam data chat grup.")
            
    # ------------------ Tab 4: Pola Keaktifan (Heatmap) ------------------
    with tab4:
        st.markdown("### ⏰ Heatmap Pola Keaktifan Chat")
        st.write("Visualisasi intensitas chat berdasarkan kombinasi Hari dalam seminggu vs Jam dalam sehari.")
        
        heatmap_data = analyzer.get_chat_heatmap_data(filtered_df)
        
        if not heatmap_data.empty:
            # Matplotlib / Seaborn Heatmap
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # WhatsApp color palette gradient
            sns.heatmap(
                heatmap_data, 
                cmap="YlGnBu", 
                annot=True, 
                fmt="d", 
                linewidths=.5, 
                ax=ax,
                cbar_kws={'label': 'Jumlah Chat'}
            )
            
            ax.set_title("Heatmap Keaktifan Grup (Hari vs Jam)", fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel("Jam Operasional", fontsize=11)
            ax.set_ylabel("Hari dalam Seminggu", fontsize=11)
            plt.xticks(rotation=0)
            plt.tight_layout()
            
            st.pyplot(fig)
            
            # Simple automatic insights
            st.markdown("#### 💡 Temuan Menarik Keaktifan:")
            # Find coordinates of max chat
            max_val = heatmap_data.values.max()
            if max_val > 0:
                max_pos = (heatmap_data == max_val).stack()
                max_pos = max_pos[max_pos].index[0]
                st.write(f"🟢 Grup chat Anda **paling aktif** pada hari **{max_pos[0]}** sekitar pukul **{max_pos[1]}:00** dengan total **{max_val} chat**.")
        else:
            st.info("Pola keaktifan tidak dapat dikalkulasi.")
            
    # ------------------ Tab 5: Kata Kunci & Emoji ------------------
    with tab5:
        col_w1, col_w2 = st.columns(2)
        
        with col_w1:
            st.markdown("### 💬 Kata Kunci Terpopuler")
            top_words = analyzer.get_most_common_words(filtered_df, 40)
            
            if top_words:
                try:
                    from wordcloud import WordCloud
                    
                    # Generate beautiful Word Cloud
                    wordcloud = WordCloud(
                        width=800, 
                        height=500, 
                        background_color='white',
                        colormap='viridis',
                        font_path=None, # Default font
                        max_words=50
                    ).generate_from_frequencies(dict(top_words))
                    
                    fig_wc, ax_wc = plt.subplots(figsize=(10, 6.5))
                    ax_wc.imshow(wordcloud, interpolation='bilinear')
                    ax_wc.axis('off')
                    plt.tight_layout()
                    st.pyplot(fig_wc)
                except Exception as e:
                    # Fallback to bar chart if wordcloud package is failing/missing
                    words_df = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi']).head(15)
                    st.bar_chart(words_df.set_index('Kata')['Frekuensi'], color="#25D366")
                    
                st.markdown("#### Daftar Kata Terpopuler:")
                words_table = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi']).head(10)
                st.dataframe(words_table, width="stretch", hide_index=True)
            else:
                st.info("Tidak ada kata kunci yang memenuhi kriteria.")
                
        with col_w2:
            st.markdown("### 🤩 Leaderboard Emoji Terbanyak")
            top_emojis = analyzer.get_most_common_emojis(filtered_df, 15)
            
            if top_emojis:
                emoji_df = pd.DataFrame(top_emojis, columns=['Emoji', 'Frekuensi'])
                
                # Visual Bar Chart for Emoji
                st.bar_chart(emoji_df.set_index('Emoji')['Frekuensi'], color="#FFC107")
                
                st.markdown("#### Tabel Penggunaan Emoji:")
                st.dataframe(emoji_df, width="stretch", hide_index=True)
                
                # Emoji fun facts
                st.markdown("#### 💡 Kontribusi Emoji Anggota:")
                emoji_user_df = leaderboard_df[['Author', 'Emoji Terkirim']].sort_values(by='Emoji Terkirim', ascending=False)
                if not emoji_user_df.empty:
                    top_emoji_user = emoji_user_df.iloc[0]
                    st.write(f"👑 **{top_emoji_user['Author']}** adalah pengguna emoji terbanyak dengan total **{top_emoji_user['Emoji Terkirim']} emoji** terkirim!")
            else:
                st.info("Tidak ada emoji terdeteksi dalam percakapan.")
