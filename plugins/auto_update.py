import os
import re
from urllib.parse import quote
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# --- മുഴുവൻ സീരിയൽ മാപ്പിംഗും ---
SERIALS_MAPPING = {
    "kanmashi": "Kanmashi",
    "karnan": "Karnan",
    "valyettan": "Valyettan",
    "pranayavilasam": "Pranayavilasam",
    "durga": "Durga",
    "chembarathy": "Chembarathy",
    "saregamapa": "SaReGaMaPa",
    "saregamapa_lil_champs": "SaReGaMaPa Lil Champs",
    "kudumbasametham": "Kudumbasametham",
    "meghasandhesham": "Meghasandhesham",
    "seethayanam": "Seethayanam",
    "krishnagadha": "Krishnagadha",
    "meghasandesam": "Meghasandesam",
    "aval_arundhati": "Aval Arundhati",
    "akale": "Akale",
    "snehapoorvam_shyama": "Snehapoorvam Shyama",
    "mangalyam": "Mangalyam",
    "manathe_kottaram": "Manathe Kottaram",
    "ashwathi_nakshatram": "Ashwathi Nakshatram",
    "kudumbashree_sharada": "Kudumbashree Sharada",
    "bigg_boss": "Bigg Boss",
    "taste_time": "Taste Time",
    "sindhu_bhairavi": "Sindhu Bhairavi",
    "comedy_cooks": "Comedy Cooks",
    "ivar_vivahitharayal": "Ivar Vivahitharayal",
    "oru_kochu_swapnam": "Oru Kochu Swapnam",
    "advocate_anjali": "Advocate Anjali",
    "kattathe_kilikoodu": "Kattathe Kilikoodu",
    "ee_puzhayum_kadannu": "Ee Puzhayum Kadannu",
    "sindoorapottu": "Sindoorapottu",
    "star_singer": "Star Singer",
    "teacheramma": "Teacheramma",
    "mazha_thorum_munpe": "Mazha Thorum Munpe",
    "pavithram": "Pavithram",
    "ishtam_mathram": "Ishtam Mathram",
    "santhwanam": "Santhwanam",
    "snehakkoottu": "Snehakkoottu",
    "mounaragam": "Mounaragam",
    "patharamattu": "Patharamattu",
    "amma_manassu": "Amma Manassu",
    "chempaneer_poovu": "Chempaneer Poovu",
    "dharmma_yoddhavu_garudan": "Dharmma Yoddhavu Garudan",
    "othiri_othiri_swapnangal": "Othiri Othiri Swapnangal",
    "ottashikharam": "Ottashikharam",
    "archana_chechi_llb": "Archana Chechi LLB",
    "super_kanmani": "Super Kanmani",
    "marimayam": "Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri": "Oru Chiri Iru Chiri Bumper Chiri",
    "the_great_family_challenge": "The Great Family Challenge",
    "roopavathi": "Roopavathi",
    "thenmavin_kombath": "Thenmavin Kombath",
    "punnaram": "Punnaram",
    "anju_sundarikal": "Anju Sundarikal",
    "amme_mookambike": "Amme Mookambike",
    "peythozhiyathe": "Peythozhiyathe",
    "chattambipparu": "Chattambipparu",
    "hridayam": "Hridayam",
    "kanyadaanam": "Kanyadaanam",
    "swayamavarapanthal": "Swayamavarapanthal",
    "mangalyam_thanthunanena": "Mangalyam Thanthunanena"
}

# --- കറക്റ്റ് ഫോർമാറ്റിലുള്ള മുഴുവൻ ഗെറ്റ് ഫയൽ ലിങ്കുകളും (Anujith1_bot) ---
GET_FILE_LINKS = [
    "https://telegram.me/Anujith1_bot?start=getfile-Kanmashi",
    "https://telegram.me/Anujith1_bot?start=getfile-Karnan",
    "https://telegram.me/Anujith1_bot?start=getfile-Valyettan",
    "https://telegram.me/Anujith1_bot?start=getfile-Pranayavilasam",
    "https://telegram.me/Anujith1_bot?start=getfile-Durga",
    "https://telegram.me/Anujith1_bot?start=getfile-Chembarathy",
    "https://telegram.me/Anujith1_bot?start=getfile-SaReGaMaPa",
    "https://telegram.me/Anujith1_bot?start=getfile-SaReGaMaPa-Lil-Champs",
    "https://telegram.me/Anujith1_bot?start=getfile-Kudumbasametham",
    "https://telegram.me/Anujith1_bot?start=getfile-Meghasandhesham",
    "https://telegram.me/Anujith1_bot?start=getfile-Seethayanam",
    "https://telegram.me/Anujith1_bot?start=getfile-Krishnagadha",
    "https://telegram.me/Anujith1_bot?start=getfile-Meghasandesam",
    "https://telegram.me/Anujith1_bot?start=getfile-Aval-Arundhati",
    "https://telegram.me/Anujith1_bot?start=getfile-Akale",
    "https://telegram.me/Anujith1_bot?start=getfile-Snehapoorvam-Shyama",
    "https://telegram.me/Anujith1_bot?start=getfile-Mangalyam",
    "https://telegram.me/Anujith1_bot?start=getfile-Manathe-Kottaram",
    "https://telegram.me/Anujith1_bot?start=getfile-Ashwathi-Nakshatram",
    "https://telegram.me/Anujith1_bot?start=getfile-Kudumbashree-Sharada",
    "https://telegram.me/Anujith1_bot?start=getfile-Bigg-Boss",
    "https://telegram.me/Anujith1_bot?start=getfile-Taste-Time",
    "https://telegram.me/Anujith1_bot?start=getfile-Sindhu-Bhairavi",
    "https://telegram.me/Anujith1_bot?start=getfile-Comedy-Cooks",
    "https://telegram.me/Anujith1_bot?start=getfile-Ivar-Vivahitharayal",
    "https://telegram.me/Anujith1_bot?start=getfile-Oru-Kochu-Swapnam",
    "https://telegram.me/Anujith1_bot?start=getfile-Advocate-Anjali",
    "https://telegram.me/Anujith1_bot?start=getfile-Kattathe-Kilikoodu",
    "https://telegram.me/Anujith1_bot?start=getfile-Ee-Puzhayum-Kadannu",
    "https://telegram.me/Anujith1_bot?start=getfile-Sindoorapottu",
    "https://telegram.me/Anujith1_bot?start=getfile-Star-Singer",
    "https://telegram.me/Anujith1_bot?start=getfile-Teacheramma",
    "https://telegram.me/Anujith1_bot?start=getfile-Mazha-Thorum-Munpe",
    "https://telegram.me/Anujith1_bot?start=getfile-Pavithram",
    "https://telegram.me/Anujith1_bot?start=getfile-Ishtam-Mathram",
    "https://telegram.me/Anujith1_bot?start=getfile-Santhwanam",
    "https://telegram.me/Anujith1_bot?start=getfile-Snehakkoottu",
    "https://telegram.me/Anujith1_bot?start=getfile-Mounaragam",
    "https://telegram.me/Anujith1_bot?start=getfile-Patharamattu",
    "https://telegram.me/Anujith1_bot?start=getfile-Amma-Manassu",
    "https://telegram.me/Anujith1_bot?start=getfile-Chempaneer-Poovu",
    "https://telegram.me/Anujith1_bot?start=getfile-Dharmma-Yoddhavu-Garudan",
    "https://telegram.me/Anujith1_bot?start=getfile-Othiri-Othiri-Swapnangal",
    "https://telegram.me/Anujith1_bot?start=getfile-Ottashikharam",
    "https://telegram.me/Anujith1_bot?start=getfile-Archana-Chechi-LLB",
    "https://telegram.me/Anujith1_bot?start=getfile-Super-Kanmani",
    "https://telegram.me/Anujith1_bot?start=getfile-Marimayam",
    "https://telegram.me/Anujith1_bot?start=getfile-Oru-Chiri-Iru-Chiri-Bumper-Chiri",
    "https://telegram.me/Anujith1_bot?start=getfile-The-Great-Family-Challenge",
    "https://telegram.me/Anujith1_bot?start=getfile-Roopavathi",
    "https://telegram.me/Anujith1_bot?start=getfile-Thenmavin-Kombath",
    "https://telegram.me/Anujith1_bot?start=getfile-Punnaram",
    "https://telegram.me/Anujith1_bot?start=getfile-Anju-Sundarikal",
    "https://telegram.me/Anujith1_bot?start=getfile-Amme-Mookambike",
    "https://telegram.me/Anujith1_bot?start=getfile-Peythozhiyathe",
    "https://telegram.me/Anujith1_bot?start=getfile-Chattambipparu",
    "https://telegram.me/Anujith1_bot?start=getfile-Hridayam",
    "https://telegram.me/Anujith1_bot?start=getfile-Kanyadaanam",
    "https://telegram.me/Anujith1_bot?start=getfile-Swayamavarapanthal",
    "https://telegram.me/Anujith1_bot?start=getfile-Mangalyam-Thanthunanena"
]

# --- ഓട്ടോമാറ്റിക് പോസ്റ്റ് ഹാൻഡ്‌ലർ ---
async def auto_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post or update.message
    if not message:
        return

    # നിങ്ങളുടെ ഡാറ്റാബേസ് ചാനൽ ഐഡിയും അപ്ഡേറ്റ് ചാനൽ ഐഡിയും ഇവിടെ നൽകുക
    DATABASE_CHANNEL_ID = -100xxxxxxxxxx  # നിങ്ങളുടെ Database Channel ID ഇവിടെ നൽകുക
    UPDATE_CHANNEL_ID = -100xxxxxxxxxx    # നിങ്ങളുടെ Update Channel ID ഇവിടെ നൽകുക

    # വരുന്ന മെസ്സേജ് ഡാറ്റാബേസ് ചാനലിൽ നിന്നാണോ എന്ന് പരിശോധിക്കുന്നു
    if message.chat.id != DATABASE_CHANNEL_ID:
        return

    # ഫയലിന്റെ പേര് കണ്ടെത്തുന്നു
    file_name = ""
    if message.document:
        file_name = message.document.file_name
    elif message.video:
        file_name = message.video.file_name or message.caption or "Unknown Video"
    elif message.caption:
        file_name = message.caption

    if not file_name:
        return

    file_name_lower = file_name.lower()
    detected_serial = None
    matched_key = None
    
    for key, serial_name in SERIALS_MAPPING.items():
        formatted_key = key.replace("_", " ")
        if formatted_key in file_name_lower or key in file_name_lower:
            detected_serial = serial_name
            matched_key = key
            break
            
    if not detected_serial:
        detected_serial = os.path.splitext(file_name)[0]

    # സീസൺ, എപ്പിസോഡ്, ക്വാളിറ്റി എന്നിവ വേർതിരിക്കുന്നു
    season_match = re.search(r'S(\d+)', file_name, re.IGNORECASE)
    season = season_match.group(1) if season_match else "01"
    
    episode_match = re.findall(r'E(\d+(?:-\d+)?)', file_name, re.IGNORECASE)
    if not episode_match:
        episode_match = re.findall(r'(\d+-\d+)', file_name)
    if not episode_match:
        episode_match = re.findall(r'Episode[_\s.-]*(\d+(?:-\d+)?)', file_name, re.IGNORECASE)
    
    episode = episode_match[0] if episode_match else "1076"

    qualities = re.findall(r'(\d{3,4}p)', file_name, re.IGNORECASE)
    quality = " - ".join(sorted(list(set(qualities)))) if qualities else "720p"

    # ക്യാപ്ഷൻ ഫോർമാറ്റ്
    caption_text = (
        "🍁 <b>Anujith Allu TV Serials</b> 🍁\n\n"
        f"📂 <b>File Name :</b> {detected_serial}\n"
        f"🎞 <b>Season :</b> {season}\n"
        f"📌 <b>Episode :</b> {episode}\n"
        f"🎬 <b>Quality :</b> {quality}"
    )

    # ഗെറ്റ് ഫയൽ ലിങ്ക് മാച്ച് ചെയ്ത് എടുക്കുന്നു
    get_file_url = None
    if matched_key:
        clean_matched_key = matched_key.replace("_", "").replace("-", "").lower()
        for link in GET_FILE_LINKS:
            clean_link = link.replace("-", "").replace("_", "").lower()
            if clean_matched_key in clean_link:
                get_file_url = link
                break
    
    if not get_file_url:
        encoded_title = quote(detected_serial)
        get_file_url = f"https://telegram.me/Anujith1_bot?start=getfile-{encoded_title}"

    # ഗെറ്റ് ഫയൽ ബട്ടൺ
    keyboard = [[InlineKeyboardButton("📥 Get File", url=get_file_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # അപ്ഡേറ്റ് ചാനലിലേക്ക് അയക്കാനുള്ള ബാനർ ഇമേജ് ലിങ്ക്
    banner_url = "നിങ്ങളുടെ_ബാനർ_ഇമേജ്_ലിങ്ക്_ഇവിടെ_നൽകുക"

    try:
        if banner_url:
            await context.bot.send_photo(
                chat_id=UPDATE_CHANNEL_ID,
                photo=banner_url,
                caption=caption_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        else:
            await context.bot.send_message(
                chat_id=UPDATE_CHANNEL_ID,
                text=caption_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(f"Error sending to Update Channel: {e}")
