import requests
import time
from datetime import datetime
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import re

# ------------------ تمہاری ڈیٹیلز ------------------
API_URL = "http://147.135.212.197/crapi/st/viewstats"
TOKEN = "RFdUREJBUzR9T4dVc49ndmFra1NYV5CIhpGVcnaOYmqHhJZXfYGJSQ=="
params = {"token": TOKEN, "records": ""}

TELEGRAM_BOT_TOKEN = "8281944831:AAGrz2zrLVLwdDd2BKISYUndRnD6yLn8pEE"
TELEGRAM_GROUP_ID = -1003819384817

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def escape_v2(text):
    chars_to_escape = r'_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + c if c in chars_to_escape else c for c in str(text)])

def fetch_sms():
    try:
        response = requests.get(API_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        # ڈیبگ پرنٹ (ایک بار دیکھ لو، پھر ہٹا سکتے ہو)
        print("API response type:", type(data))
        if data and isinstance(data, list) and data:
            print("First entry example:", data[0])
        
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"API fetch failed: {e}")
        return []

def parse_timestamp(ts_str):
    try:
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None

# Country map (بہت سارے ممالک شامل)
country_map = {
{
    "1": ("United States", "🇺🇸"),
    "7": ("Russia", "🇷🇺"),
    "20": ("Egypt", "🇪🇬"),
    "27": ("South Africa", "🇿🇦"),
    "30": ("Greece", "🇬🇷"),
    "31": ("Netherlands", "🇳🇱"),
    "32": ("Belgium", "🇧🇪"),
    "33": ("France", "🇫🇷"),
    "34": ("Spain", "🇪🇸"),
    "36": ("Hungary", "🇭🇺"),
    "39": ("Italy", "🇮🇹"),
    "40": ("Romania", "🇷🇴"),
    "41": ("Switzerland", "🇨🇭"),
    "43": ("Austria", "🇦🇹"),
    "44": ("United Kingdom", "🇬🇧"),
    "45": ("Denmark", "🇩🇰"),
    "46": ("Sweden", "🇸🇪"),
    "47": ("Norway", "🇳🇴"),
    "48": ("Poland", "🇵🇱"),
    "49": ("Germany", "🇩🇪"),
    "51": ("Peru", "🇵🇪"),
    "52": ("Mexico", "🇲🇽"),
    "53": ("Cuba", "🇨🇺"),
    "54": ("Argentina", "🇦🇷"),
    "55": ("Brazil", "🇧🇷"),
    "56": ("Chile", "🇨🇱"),
    "57": ("Colombia", "🇨🇴"),
    "58": ("Venezuela", "🇻🇪"),
    "60": ("Malaysia", "🇲🇾"),
    "61": ("Australia", "🇦🇺"),
    "62": ("Indonesia", "🇮🇩"),
    "63": ("Philippines", "🇵🇭"),
    "64": ("New Zealand", "🇳🇿"),
    "65": ("Singapore", "🇸🇬"),
    "66": ("Thailand", "🇹🇭"),
    "81": ("Japan", "🇯🇵"),
    "82": ("South Korea", "🇰🇷"),
    "84": ("Vietnam", "🇻🇳"),
    "86": ("China", "🇨🇳"),
    "91": ("India", "🇮🇳"),
    "92": ("Pakistan", "🇵🇰"),
    "93": ("Afghanistan", "🇦🇫"),
    "94": ("Sri Lanka", "🇱🇰"),
    "95": ("Myanmar", "🇲🇲"),
    "98": ("Iran", "🇮🇷"),
    "211": ("South Sudan", "🇸🇸"),
    "212": ("Morocco", "🇲🇦"),
    "213": ("Algeria", "🇩🇿"),
    "216": ("Tunisia", "🇹🇳"),
    "218": ("Libya", "🇱🇾"),
    "220": ("Gambia", "🇬🇲"),
    "221": ("Senegal", "🇸🇳"),
    "222": ("Mauritania", "🇲🇷"),
    "223": ("Mali", "🇲🇱"),
    "224": ("Guinea", "🇬🇳"),
    "225": ("Ivory Coast", "🇨🇮"),
    "226": ("Burkina Faso", "🇧🇫"),
    "227": ("Niger", "🇳🇪"),
    "228": ("Togo", "🇹🇬"),
    "229": ("Benin", "🇧🇯"),
    "230": ("Mauritius", "🇲🇺"),
    "231": ("Liberia", "🇱🇷"),
    "232": ("Sierra Leone", "🇸🇱"),
    "233": ("Ghana", "🇬🇭"),
    "234": ("Nigeria", "🇳🇬"),
    "235": ("Chad", "🇹🇩"),
    "236": ("Central African Republic", "🇨🇫"),
    "237": ("Cameroon", "🇨🇲"),
    "238": ("Cape Verde", "🇨🇻"),
    "239": ("Sao Tome and Principe", "🇸🇹"),
    "240": ("Equatorial Guinea", "🇬🇶"),
    "241": ("Gabon", "🇬🇦"),
    "242": ("Congo", "🇨🇬"),
    "243": ("DR Congo", "🇨🇩"),
    "244": ("Angola", "🇦🇴"),
    "248": ("Seychelles", "🇸🇨"),
    "249": ("Sudan", "🇸🇩"),
    "250": ("Rwanda", "🇷🇼"),
    "251": ("Ethiopia", "🇪🇹"),
    "252": ("Somalia", "🇸🇴"),
    "253": ("Djibouti", "🇩🇯"),
    "254": ("Kenya", "🇰🇪"),
    "255": ("Tanzania", "🇹🇿"),
    "256": ("Uganda", "🇺🇬"),
    "257": ("Burundi", "🇧🇮"),
    "258": ("Mozambique", "🇲🇿"),
    "260": ("Zambia", "🇿🇲"),
    "261": ("Madagascar", "🇲🇬"),
    "262": ("Reunion", "🇷🇪"),
    "263": ("Zimbabwe", "🇿🇼"),
    "264": ("Namibia", "🇳🇦"),
    "265": ("Malawi", "🇲🇼"),
    "266": ("Lesotho", "🇱🇸"),
    "267": ("Botswana", "🇧🇼"),
    "268": ("Eswatini", "🇸🇿"),
    "269": ("Comoros", "🇰🇲"),
    "290": ("Saint Helena", "🇸🇭"),
    "291": ("Eritrea", "🇪🇷"),
    "297": ("Aruba", "🇦🇼"),
    "298": ("Faroe Islands", "🇫🇴"),
    "299": ("Greenland", "🇬🇱"),
    "350": ("Gibraltar", "🇬🇮"),
    "351": ("Portugal", "🇵🇹"),
    "352": ("Luxembourg", "🇱🇺"),
    "353": ("Ireland", "🇮🇪"),
    "354": ("Iceland", "🇮🇸"),
    "355": ("Albania", "🇦🇱"),
    "356": ("Malta", "🇲🇹"),
    "357": ("Cyprus", "🇨🇾"),
    "358": ("Finland", "🇫🇮"),
    "359": ("Bulgaria", "🇧🇬"),
    "370": ("Lithuania", "🇱🇹"),
    "371": ("Latvia", "🇱🇻"),
    "372": ("Estonia", "🇪🇪"),
    "373": ("Moldova", "🇲🇩"),
    "374": ("Armenia", "🇦🇲"),
    "375": ("Belarus", "🇧🇾"),
    "376": ("Andorra", "🇦🇩"),
    "377": ("Monaco", "🇲🇨"),
    "378": ("San Marino", "🇸🇲"),
    "380": ("Ukraine", "🇺🇦"),
    "381": ("Serbia", "🇷🇸"),
    "382": ("Montenegro", "🇲🇪"),
    "383": ("Kosovo", "🇽🇰"),
    "385": ("Croatia", "🇭🇷"),
    "386": ("Slovenia", "🇸🇮"),
    "387": ("Bosnia and Herzegovina", "🇧🇦"),
    "389": ("North Macedonia", "🇲🇰"),
    "420": ("Czech Republic", "🇨🇿"),
    "421": ("Slovakia", "🇸🇰"),
    "423": ("Liechtenstein", "🇱🇮"),
    "500": ("Falkland Islands", "🇫🇰"),
    "501": ("Belize", "🇧🇿"),
    "502": ("Guatemala", "🇬🇹"),
    "503": ("El Salvador", "🇸🇻"),
    "504": ("Honduras", "🇭🇳"),
    "505": ("Nicaragua", "🇳🇮"),
    "506": ("Costa Rica", "🇨🇷"),
    "507": ("Panama", "🇵🇦"),
    "509": ("Haiti", "🇭🇹"),
    "590": ("Guadeloupe", "🇬🇵"),
    "591": ("Bolivia", "🇧🇴"),
    "592": ("Guyana", "🇬🇾"),
    "593": ("Ecuador", "🇪🇨"),
    "594": ("French Guiana", "🇬🇫"),
    "595": ("Paraguay", "🇵🇾"),
    "596": ("Martinique", "🇲🇶"),
    "597": ("Suriname", "🇸🇷"),
    "598": ("Uruguay", "🇺🇾"),
    "599": ("Caribbean Netherlands", "🇧🇶"),
    "670": ("Timor-Leste", "🇹🇱"),
    "672": ("Norfolk Island", "🇳🇫"),  # Antarctica shared sometimes
    "673": ("Brunei", "🇧🇳"),
    "674": ("Nauru", "🇳🇷"),
    "675": ("Papua New Guinea", "🇵🇬"),
    "676": ("Tonga", "🇹🇴"),
    "677": ("Solomon Islands", "🇸🇧"),
    "678": ("Vanuatu", "🇻🇺"),
    "679": ("Fiji", "🇫🇯"),
    "680": ("Palau", "🇵🇼"),
    "681": ("Wallis and Futuna", "🇼🇫"),
    "682": ("Cook Islands", "🇨🇰"),
    "683": ("Niue", "🇳🇺"),
    "685": ("Samoa", "🇼🇸"),
    "686": ("Kiribati", "🇰🇮"),
    "687": ("New Caledonia", "🇳🇨"),
    "688": ("Tuvalu", "🇹🇻"),
    "689": ("French Polynesia", "🇵🇫"),
    "690": ("Tokelau", "🇹🇰"),
    "691": ("Micronesia", "🇫🇲"),
    "692": ("Marshall Islands", "🇲🇭"),
    "850": ("North Korea", "🇰🇵"),
    "852": ("Hong Kong", "🇭🇰"),
    "853": ("Macau", "🇲🇴"),
    "855": ("Cambodia", "🇰🇭"),
    "856": ("Laos", "🇱🇦"),
    "880": ("Bangladesh", "🇧🇩"),
    "886": ("Taiwan", "🇹🇼"),
    "960": ("Maldives", "🇲🇻"),
    "961": ("Lebanon", "🇱🇧"),
    "962": ("Jordan", "🇯🇴"),
    "963": ("Syria", "🇸🇾"),
    "964": ("Iraq", "🇮🇶"),
    "965": ("Kuwait", "🇰🇼"),
    "966": ("Saudi Arabia", "🇸🇦"),
    "967": ("Yemen", "🇾🇪"),
    "968": ("Oman", "🇴🇲"),
    "971": ("UAE", "🇦🇪"),
    "972": ("Israel", "💩"),
    "973": ("Bahrain", "🇧🇭"),
    "974": ("Qatar", "🇶🇦"),
    "975": ("Bhutan", "🇧🇹"),
    "976": ("Mongolia", "🇲🇳"),
    "977": ("Nepal", "🇳🇵"),
    "992": ("Tajikistan", "🇹🇯"),
    "993": ("Turkmenistan", "🇹🇲"),
    "994": ("Azerbaijan", "🇦🇿"),
    "995": ("Georgia", "🇬🇪"),
    "996": ("Kyrgyzstan", "🇰🇬"),
    "998": ("Uzbekistan", "🇺🇿"),
    # مزید چاہیے تو یہاں ایڈ کر سکتے ہیں (jaise special cases: NANP shared 1 for Canada etc., but main US rakha)
}
last_seen_time = None

print("✅ OTP Auto Forwarder Started... Checking every 40 seconds.")

while True:
    entries = fetch_sms()
    
    if not entries:
        time.sleep(40)
        continue
    
    new_entries = []
    
    if last_seen_time is None:
        new_entries = entries[:8]
        if new_entries:
            last_seen_time = parse_timestamp(new_entries[0][3])
    else:
        for entry in entries:
            ts = parse_timestamp(entry[3])
            if ts and ts > last_seen_time:
                new_entries.append(entry)
    
    if new_entries:
        latest_ts = parse_timestamp(new_entries[0][3])
        if latest_ts:
            last_seen_time = latest_ts
        print(f"Found {len(new_entries)} new OTP(s) | Latest: {new_entries[0][3]}")
    
    for entry in new_entries[::-1]:
        app       = entry[0].strip()
        phone     = entry[1].strip()
        full_msg  = entry[2].strip().replace('\n', ' ').replace('  ', ' ')
        timestamp = entry[3]

        # Country detection
        country_code = ""
        clean_phone = phone.lstrip('+')  # + ہٹا دو اگر ہو
        for code in sorted(country_map.keys(), key=len, reverse=True):
            if clean_phone.startswith(code):
                country_code = code
                break
        
        if country_code in country_map:
            country, flag = country_map[country_code]
        else:
            country = "Unknown"
            flag = "🌍"

        masked_phone = phone[:5] + "**" + phone[-5:] if len(phone) >= 10 else phone

        # OTP detect - تمام زبانوں سے
        otp = "N/A"
        otp_match = re.search(
            r'(?:code|كود|رمز|كود التفعيل|رمز التحقق|código|кود|验证码|code de vérification|codice|verification code|Your .* code|Your .* código|Your .* код|imo verification code|WhatsApp code|code is|is)[\s\W:-]*(\d{3,8})',
            full_msg, re.IGNORECASE | re.UNICODE
        )
        if otp_match:
            otp = otp_match.group(1)
        else:
            otp_match = re.search(r'\b(\d{4,8})\b', full_msg)
            if otp_match:
                otp = otp_match.group(1)

        otp = re.sub(r'[- ]', '', otp)

        text = f"""✉️ *New {escape_v2(app)} OTP Received*

> *Time:* {escape_v2(timestamp)} ""
> *Country:* {escape_v2(country)}, {flag} ""
> *Service:* {escape_v2(app)} ""
> *Number:* `{escape_v2(masked_phone)}` ""
> *OTP:* ```{escape_v2(otp)}``` ""
> *Message:* ""
> {escape_v2(full_msg.replace('n', '\\n').replace('  ', ' '))}

──────────────────────────────"""

        keyboard = [
            [InlineKeyboardButton("Main Channel", url="https://t.me/ProTech43")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=text,
                parse_mode="MarkdownV2",
                reply_markup=reply_markup,
                disable_notification=False
            )
            print(f"Sent → {masked_phone} ({app}) | Country: {country} | OTP: {otp}")
        except Exception as e:
            print(f"Telegram send FAILED: {str(e)}")
    
    time.sleep(40) "235": ("Chad", "🇹🇩"),
"236": ("Central African Republic", "🇨🇫"),
"237": ("Cameroon", "🇨🇲"),
"238": ("Cape Verde", "🇨🇻"),
"239": ("Sao Tome and Principe", "🇸🇹"),
"240": ("Equatorial Guinea", "🇬🇶"),
"241": ("Gabon", "🇬🇦"),
"242": ("Congo", "🇨🇬"),
"243": ("DR Congo", "🇨🇩"),
"244": ("Angola", "🇦🇴"),
"248": ("Seychelles", "🇸🇨"),
"249": ("Sudan", "🇸🇩"),
"250": ("Rwanda", "🇷🇼"),
"251": ("Ethiopia", "🇪🇹"),
"252": ("Somalia", "🇸🇴"),
"253": ("Djibouti", "🇩🇯"),
"254": ("Kenya", "🇰🇪"),
"255": ("Tanzania", "🇹🇿"),
"256": ("Uganda", "🇺🇬"),
"257": ("Burundi", "🇧🇮"),
"258": ("Mozambique", "🇲🇿"),
"260": ("Zambia", "🇿🇲"),
"261": ("Madagascar", "🇲🇬"),
"262": ("Reunion", "🇷🇪"),
"263": ("Zimbabwe", "🇿🇼"),
"264": ("Namibia", "🇳🇦"),
"265": ("Malawi", "🇲🇼"),
"266": ("Lesotho", "🇱🇸"),
"267": ("Botswana", "🇧🇼"),
"268": ("Eswatini", "🇸🇿"),
"269": ("Comoros", "🇰🇲"),
"290": ("Saint Helena", "🇸🇭"),
"291": ("Eritrea", "🇪🇷"),
"297": ("Aruba", "🇦🇼"),
"298": ("Faroe Islands", "🇫🇴"),
"299": ("Greenland", "🇬🇱"),
"350": ("Gibraltar", "🇬🇮"),
"351": ("Portugal", "🇵🇹"),
"352": ("Luxembourg", "🇱🇺"),
"353": ("Ireland", "🇮🇪"),
"354": ("Iceland", "🇮🇸"),
"355": ("Albania", "🇦🇱"),
"356": ("Malta", "🇲🇹"),
"357": ("Cyprus", "🇨🇾"),
"358": ("Finland", "🇫🇮"),
"359": ("Bulgaria", "🇧🇬"),
"370": ("Lithuania", "🇱🇹"),
"371": ("Latvia", "🇱🇻"),
"372": ("Estonia", "🇪🇪"),
"373": ("Moldova", "🇲🇩"),
"374": ("Armenia", "🇦🇲"),
"375": ("Belarus", "🇧🇾"),
"376": ("Andorra", "🇦🇩"),
"377": ("Monaco", "🇲🇨"),
"378": ("San Marino", "🇸🇲"),
"380": ("Ukraine", "🇺🇦"),
"381": ("Serbia", "🇷🇸"),
"382": ("Montenegro", "🇲🇪"),
"383": ("Kosovo", "🇽🇰"),
"385": ("Croatia", "🇭🇷"),
"386": ("Slovenia", "🇸🇮"),
"387": ("Bosnia and Herzegovina", "🇧🇦"),
"389": ("North Macedonia", "🇲🇰"),
"420": ("Czech Republic", "🇨🇿"),
"421": ("Slovakia", "🇸🇰"),
"423": ("Liechtenstein", "🇱🇮"),
"500": ("Falkland Islands", "🇫🇰"),
"501": ("Belize", "🇧🇿"),
"502": ("Guatemala", "🇬🇹"),
"503": ("El Salvador", "🇸🇻"),
"504": ("Honduras", "🇭🇳"),
"505": ("Nicaragua", "🇳🇮"),
"506": ("Costa Rica", "🇨🇷"),
"507": ("Panama", "🇵🇦"),
"509": ("Haiti", "🇭🇹"),
"590": ("Guadeloupe", "🇬🇵"),
"591": ("Bolivia", "🇧🇴"),
"592": ("Guyana", "🇬🇾"),
"593": ("Ecuador", "🇪🇨"),
"594": ("French Guiana", "🇬🇫"),
"595": ("Paraguay", "🇵🇾"),
"596": ("Martinique", "🇲🇶"),
"597": ("Suriname", "🇸🇷"),
"598": ("Uruguay", "🇺🇾"),
"599": ("Caribbean Netherlands", "🇧🇶"),
"670": ("Timor-Leste", "🇹🇱"),
"672": ("Norfolk Island", "🇳🇫"),
"673": ("Brunei", "🇧🇳"),
"674": ("Nauru", "🇳🇷"),
"675": ("Papua New Guinea", "🇵🇬"),
"676": ("Tonga", "🇹🇴"),
"677": ("Solomon Islands", "🇸🇧"),
"678": ("Vanuatu", "🇻🇺"),
"679": ("Fiji", "🇫🇯"),
"680": ("Palau", "🇵🇼"),
"681": ("Wallis and Futuna", "🇼🇫"),
"682": ("Cook Islands", "🇨🇰"),
"683": ("Niue", "🇳🇺"),
"685": ("Samoa", "🇼🇸"),
"686": ("Kiribati", "🇰🇮"),
"687": ("New Caledonia", "🇳🇨"),
"688": ("Tuvalu", "🇹🇻"),
"689": ("French Polynesia", "🇵🇫"),
"690": ("Tokelau", "🇹🇰"),
"691": ("Micronesia", "🇫🇲"),
"692": ("Marshall Islands", "🇲🇭"),
"850": ("North Korea", "🇰🇵"),
"852": ("Hong Kong", "🇭🇰"),
"853": ("Macau", "🇲🇴"),
"855": ("Cambodia", "🇰🇭"),
"856": ("Laos", "🇱🇦"),
"880": ("Bangladesh", "🇧🇩"),
"886": ("Taiwan", "🇹🇼"),
"960": ("Maldives", "🇲🇻"),
"961": ("Lebanon", "🇱🇧"),
"962": ("Jordan", "🇯🇴"),
"963": ("Syria", "🇸🇾"),
"964": ("Iraq", "🇮🇶"),
"965": ("Kuwait", "🇰🇼"),
"966": ("Saudi Arabia", "🇸🇦"),
"967": ("Yemen", "🇾🇪"),
"968": ("Oman", "🇴🇲"),
"971": ("UAE", "🇦🇪"),
"972": ("Israel", "💩"),
"973": ("Bahrain", "🇧🇭"),
"974": ("Qatar", "🇶🇦"),
"975": ("Bhutan", "🇧🇹"),
"976": ("Mongolia", "🇲🇳"),
"977": ("Nepal", "🇳🇵"),
"992": ("Tajikistan", "🇹🇯"),
"993": ("Turkmenistan", "🇹🇲"),
"994": ("Azerbaijan", "🇦🇿"),
"995": ("Georgia", "🇬🇪"),
"996": ("Kyrgyzstan", "🇰🇬"),
"998": ("Uzbekistan", "🇺🇿"),
}

# ---------------- START ----------------
last_seen = None

print("🚀 OTP Forwarder Started...")

while True:
    data = fetch_sms()

    if not data:
        time.sleep(30)
        continue

    new = []

    if last_seen is None:
        new = data[:5]
        if new:
            last_seen = parse_time(new[0][3])
    else:
        for i in data:
            t = parse_time(i[3])
            if t and t > last_seen:
                new.append(i)

    if new:
        last_seen = parse_time(new[0][3])

    for entry in new[::-1]:
        try:
            app = entry[0]
            phone = entry[1]
            msg = entry[2]
            time_str = entry[3]

            # country detect
            code = phone.lstrip("+")
            country = "Unknown"
            flag = "🌍"

            for c in sorted(country_map.keys(), key=len, reverse=True):
                if code.startswith(c):
                    country, flag = country_map[c]
                    break

            # OTP
            otp_match = re.search(r"\b\d{4,8}\b", msg)
            otp = otp_match.group() if otp_match else "N/A"

            masked = phone[:5] + "**" + phone[-4:]

            text = f"""✉️ *New OTP Received*

⏰ Time: {escape_v2(time_str)}
🌍 Country: {escape_v2(country)} {flag}
📱 Service: {escape_v2(app)}
📞 Number: `{escape_v2(masked)}`
🔑 OTP: *{escape_v2(otp)}*

💬 Message:
{escape_v2(msg)}

──────────────"""

            keyboard = [
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/ProTech43")]
            ]

            bot.send_message(
                chat_id=TELEGRAM_GROUP_ID,
                text=text,
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            print("✅ Sent:", phone)

        except Exception as e:
            print("SEND ERROR:", e)

    time.sleep(30) 
