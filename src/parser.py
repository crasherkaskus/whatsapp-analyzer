import re
import pandas as pd

def parse_chat_data(file_content: str) -> pd.DataFrame:
    """
    Parses raw WhatsApp chat export text into a structured Pandas DataFrame.
    
    Supports:
    - Android formats (12h and 24h, with or without AM/PM)
    - iOS format (bracketed timestamps)
    - Flexible separators (/, -, or . in dates)
    - Multi-line messages
    - System messages (e.g. member joined, group encryption notifications)
    """
    lines = file_content.split('\n')
    
    # Regex patterns
    # Android e.g. "15/09/20, 20:34 - Sender: Message" or "15/09/20, 08:34 PM - Sender: Message"
    android_pattern = r'^(\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s*(?:[aApP][mM]|[aApP]\.[mM]\.)?)\s*-\s*(.*)$'
    
    # iOS e.g. "[15/09/20, 20:34:12] Sender: Message" or "[15/09/20, 8:34:12 am] Sender: Message"
    ios_pattern = r'^\[(\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s*(?:[aApP][mM]|[aApP]\.[mM]\.)?)\]\s*(.*)$'
    
    parsed_messages = []
    current_msg = None
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
            
        # Try Android matching
        match = re.match(android_pattern, line)
        if match:
            if current_msg:
                parsed_messages.append(current_msg)
            date_str, time_str, rest = match.groups()
            current_msg = {
                'date_str': date_str,
                'time_str': time_str,
                'rest': rest
            }
            continue
            
        # Try iOS matching
        match = re.match(ios_pattern, line)
        if match:
            if current_msg:
                parsed_messages.append(current_msg)
            date_str, time_str, rest = match.groups()
            current_msg = {
                'date_str': date_str,
                'time_str': time_str,
                'rest': rest
            }
            continue
            
        # If it doesn't match any timestamp pattern, it's a multi-line message continuation
        if current_msg:
            current_msg['rest'] += '\n' + line
        else:
            # Skip any leading unparsed header lines
            pass
            
    if current_msg:
        parsed_messages.append(current_msg)
        
    # Further parse 'rest' to separate author and message body
    final_messages = []
    for msg in parsed_messages:
        rest = msg['rest']
        # Find first colon space separator ': ' to identify sender
        parts = rest.split(': ', 1)
        if len(parts) == 2:
            author = parts[0].strip()
            message = parts[1]
            is_system = False
        else:
            # If no colon space, it's a system event (e.g. "John left the group")
            author = 'System'
            message = rest
            is_system = True
            
        time_clean = re.sub(r'\s+', ' ', msg['time_str']).strip()
        date_clean = msg['date_str'].strip()
        
        final_messages.append({
            'date_str': date_clean,
            'time_str': time_clean,
            'author': author,
            'message': message,
            'is_system': is_system
        })
        
    df = pd.DataFrame(final_messages)
    if df.empty:
        return df
        
    # Standarize datetime parsing by trying multiple standard formats
    def parse_datetime(row):
        date_part = row['date_str']
        # Normalize separators to '/' for easier parsing
        date_part = date_part.replace('.', '/').replace('-', '/')
        
        time_part = row['time_str']
        # Normalize whitespace in time
        time_part = time_part.replace('\u202f', ' ').replace('\xa0', ' ')
        
        dt_str = f"{date_part} {time_part}"
        
        formats = [
            '%d/%m/%y %I:%M %p', '%d/%m/%Y %I:%M %p',
            '%d/%m/%y %H:%M:%S', '%d/%m/%Y %H:%M:%S',
            '%d/%m/%y %H:%M', '%d/%m/%Y %H:%M',
            '%m/%d/%y %I:%M %p', '%m/%d/%Y %I:%M %p',
            '%m/%d/%y %H:%M:%S', '%m/%d/%Y %H:%M:%S',
            '%y/%m/%d %H:%M', '%Y/%m/%d %H:%M',
        ]
        
        for fmt in formats:
            try:
                return pd.to_datetime(dt_str, format=fmt)
            except:
                continue
        # General fallback
        try:
            return pd.to_datetime(dt_str, errors='coerce')
        except:
            return pd.NaT
            
    df['datetime'] = df.apply(parse_datetime, axis=1)
    
    # Drop rows where datetime could not be resolved
    df = df.dropna(subset=['datetime'])
    
    # Sort chronologically
    df = df.sort_values(by='datetime').reset_index(drop=True)
    
    # Extract structural time components
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['month_name'] = df['datetime'].dt.strftime('%B')
    df['day'] = df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.strftime('%A')
    df['hour'] = df['datetime'].dt.hour
    df['time'] = df['datetime'].dt.time
    
    # Create a nice label for sorting and display, e.g. "2026-06"
    df['month_year'] = df['datetime'].dt.to_period('M')
    df['month_year_str'] = df['datetime'].dt.strftime('%Y-%m')
    
    return df
