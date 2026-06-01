import re
from collections import Counter
import pandas as pd
import emoji

# Stopwords lists for Indonesian and English
INDONESIAN_STOPWORDS = {
    'yg', 'yang', 'dan', 'di', 'dari', 'ke', 'ini', 'itu', 'untuk', 'dengan', 'ada', 
    'bisa', 'aja', 'ya', 'ga', 'gak', 'mau', 'sudah', 'tapi', 'akan', 'atau', 'pada', 
    'juga', 'lah', 'kah', 'sih', 'kok', 'deh', 'loh', 'kan', 'saya', 'aku', 'kamu', 
    'kita', 'mereka', 'dia', 'kami', 'lu', 'gw', 'gue', 'kalo', 'kalau', 'buat', 
    'tersebut', 'adalah', 'seperti', 'dalam', 'si', 'nih', 'tuh', 'dah', 'oke', 'ok',
    'saja', 'yaa', 'sangat', 'secara', 'karena', 'oleh', 'telah', 'yaitu', 'yakni',
    'masih', 'belum', 'habis', 'lagi', 'lagian', 'kok', 'lah', 'dong', 'sih', 'pas'
}

ENGLISH_STOPWORDS = {
    'the', 'a', 'an', 'to', 'for', 'in', 'on', 'at', 'by', 'of', 'and', 'but', 'or', 
    'so', 'if', 'this', 'that', 'it', 'is', 'are', 'was', 'were', 'be', 'have', 'has', 
    'had', 'do', 'does', 'did', 'you', 'i', 'we', 'they', 'he', 'she', 'me', 'us', 
    'him', 'her', 'my', 'your', 'their', 'with', 'about', 'as', 'at', 'by', 'from'
}

STOPWORDS = INDONESIAN_STOPWORDS.union(ENGLISH_STOPWORDS)

def is_media_msg(message: str) -> bool:
    """Checks if a message contains typical media omission placeholders."""
    msg_lower = message.lower().strip()
    media_markers = [
        '<media omitted>',
        '<media tidak dicantumkan>',
        '<media disembunyikan>',
        '<berkas dilampirkan>',
        'media disembunyikan',
        'berkas dilampirkan',
        'media omitted',
        'image omitted',
        'video omitted',
        'sticker omitted',
        'audio omitted',
        'pesan suara disembunyikan',
        'stiker disembunyikan',
        'stiker disebarkan',
        'stiker dicantumkan',
        'stiker tidak dicantumkan',
        '.pdf (file',
        '.docx (file',
        '.xlsx (file',
        '.pptx (file'
    ]
    for marker in media_markers:
        if marker in msg_lower:
            return True
    return False

def is_deleted_msg(message: str) -> bool:
    """Checks if a message was deleted."""
    msg_lower = message.lower().strip()
    deleted_markers = [
        'pesan ini telah dihapus',
        'pesan ini dihapus',
        'this message was deleted',
        'you deleted this message'
    ]
    for marker in deleted_markers:
        if marker in msg_lower:
            return True
    return False

def get_general_stats(df: pd.DataFrame) -> dict:
    """Computes high-level KPI statistics from the chat DataFrame."""
    # Filter out system messages
    user_df = df[df['is_system'] == False]
    
    total_messages = len(user_df)
    
    # Calculate total words and links
    url_pattern = r'https?://\S+|www\.\S+'
    
    total_words = 0
    total_links = 0
    total_media = 0
    total_deleted = 0
    
    for msg in user_df['message']:
        # Media count
        if is_media_msg(msg):
            total_media += 1
            continue
            
        # Deleted count
        if is_deleted_msg(msg):
            total_deleted += 1
            continue
            
        # Words count
        words = msg.split()
        total_words += len(words)
        
        # Links count
        links = re.findall(url_pattern, msg)
        total_links += len(links)
        
    total_users = user_df['author'].nunique()
    
    return {
        'total_messages': total_messages,
        'total_words': total_words,
        'total_media': total_media,
        'total_links': total_links,
        'total_deleted': total_deleted,
        'total_users': total_users
    }

def get_user_leaderboard(df: pd.DataFrame) -> pd.DataFrame:
    """Generates user posting activity statistics."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return pd.DataFrame()
        
    stats = []
    total_messages = len(user_df)
    
    for author, group in user_df.groupby('author'):
        msg_count = len(group)
        percentage = (msg_count / total_messages) * 100
        
        # Compute words, media, and deleted messages
        words_count = 0
        media_count = 0
        deleted_count = 0
        emoji_count = 0
        
        for msg in group['message']:
            if is_media_msg(msg):
                media_count += 1
                continue
            if is_deleted_msg(msg):
                deleted_count += 1
                continue
                
            words_count += len(msg.split())
            emoji_count += len([c for c in msg if emoji.is_emoji(c)])
            
        avg_word_len = words_count / (msg_count - media_count - deleted_count) if (msg_count - media_count - deleted_count) > 0 else 0
        
        stats.append({
            'Author': author,
            'Total Chat': msg_count,
            'Persentase (%)': round(percentage, 1),
            'Total Kata': words_count,
            'Rata-rata Kata/Chat': round(avg_word_len, 1),
            'Media Terkirim': media_count,
            'Chat Dihapus': deleted_count,
            'Emoji Terkirim': emoji_count
        })
        
    stats_df = pd.DataFrame(stats)
    stats_df = stats_df.sort_values(by='Total Chat', ascending=False).reset_index(drop=True)
    return stats_df

def get_monthly_timeline(df: pd.DataFrame) -> pd.DataFrame:
    """Generates monthly chat frequency timeline."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return pd.DataFrame()
        
    timeline = user_df.groupby('month_year_str').size().reset_index(name='Total Chat')
    timeline = timeline.sort_values(by='month_year_str').reset_index(drop=True)
    return timeline

def get_daily_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Generates day-of-the-week chat frequency."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return pd.DataFrame()
        
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Mapping for Indonesian translation
    day_indonesia = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu', 
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }
    
    daily = user_df.groupby('day_name').size().reindex(days_order).fillna(0).reset_index(name='Total Chat')
    daily['Hari'] = daily['day_name'].map(day_indonesia)
    return daily

def get_hourly_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Generates hourly chat frequency."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return pd.DataFrame()
        
    hours_order = list(range(24))
    hourly = user_df.groupby('hour').size().reindex(hours_order).fillna(0).reset_index(name='Total Chat')
    hourly['Jam'] = hourly['hour'].apply(lambda x: f"{x:02d}:00")
    return hourly

def get_chat_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """Generates pivot table of Day vs Hour for heatmap."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return pd.DataFrame()
        
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_indonesia = {
        'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu', 
        'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
    }
    
    # Create crosstab
    pivot = pd.crosstab(user_df['day_name'], user_df['hour'])
    # Reindex days
    pivot = pivot.reindex(days_order).fillna(0).astype(int)
    # Rename index to Indonesian days
    pivot.index = pivot.index.map(day_indonesia)
    return pivot

def get_most_common_words(df: pd.DataFrame, num_words: int = 20) -> list:
    """Extracts and counts most frequent words excluding media markers and stopwords."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return []
        
    words_list = []
    
    for msg in user_df['message']:
        if is_media_msg(msg) or is_deleted_msg(msg):
            continue
            
        # Clean special chars, numbers, and lowercase
        cleaned_msg = re.sub(r'[^a-zA-Z\s]', '', msg).lower()
        words = cleaned_msg.split()
        
        # Filter stopwords and short words
        filtered = [w for w in words if w not in STOPWORDS and len(w) > 1]
        words_list.extend(filtered)
        
    counter = Counter(words_list)
    return counter.most_common(num_words)

def get_most_common_emojis(df: pd.DataFrame, num_emojis: int = 15) -> list:
    """Extracts and counts most frequent emoji characters."""
    user_df = df[df['is_system'] == False]
    if user_df.empty:
        return []
        
    emojis = []
    for msg in user_df['message']:
        if is_media_msg(msg) or is_deleted_msg(msg):
            continue
        emojis.extend([c for c in msg if emoji.is_emoji(c)])
        
    counter = Counter(emojis)
    return counter.most_common(num_emojis)

def get_transaction_leaderboard(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes transaction stats (media files representing proof of payment) per user.
    Ignores plain text messages.
    """
    user_df = df[df['is_system'] == False].copy()
    if user_df.empty:
        return pd.DataFrame()
        
    # Mark messages that are media/transactions
    user_df['is_transaction'] = user_df['message'].apply(is_media_msg)
    
    # Filter only transactions
    tx_df = user_df[user_df['is_transaction'] == True]
    
    if tx_df.empty:
        return pd.DataFrame()
        
    total_transactions = len(tx_df)
    
    stats = []
    for author, group in tx_df.groupby('author'):
        tx_count = len(group)
        percentage = (tx_count / total_transactions) * 100
        
        stats.append({
            'Author': author,
            'Total Transaksi': tx_count,
            'Persentase (%)': round(percentage, 1)
        })
        
    stats_df = pd.DataFrame(stats)
    stats_df = stats_df.sort_values(by='Total Transaksi', ascending=False).reset_index(drop=True)
    return stats_df

