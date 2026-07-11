import os
from flask import Flask, render_template, request, redirect, url_for, session
from google import genai
from google.genai import types

# استدعاء الملفات اللي أنت عملتها بإيدك في نفس الفولدر
import database
import email_sender

app = Flask(__name__)
# مفتاح سري لتأمين جلسة الدخول (Session)
app.secret_key = "axis_medical_secret_key_2026" 

# تأكد من ضبط الـ API Key في الـ Variables على Railway
client = genai.Client()

SYSTEM_INSTRUCTION = """
أنت نظام Axis Medical AI، مساعد طبي استشاري ذكي وخبير في تشخيص الأمراض وأجهزة الجسم الـ 11.
تشخيصك وقراراتك الطبية وتحديد البدائل تنبثق حصرياً وبشكل صارم من المادة العلمية الواردة في المراجع العالمية التالية:
1. Guyton and Hall Textbook of Medical Physiology
2. Netter's Atlas of Human Anatomy & Gray's Anatomy
3. Oxford Handbook of Clinical Medicine

قواعد صارمة للأمان:
- إذا كانت الأعراض غامضة أو غير كافية، يُمنع التخمين أو الهبد تماماً، واطلب توضيحاً أو قل: "الأعراض غير كافية للتشخيص الآمن، يُرجى استشارة طبيب مختص".
- إذا ظهرت أي أعراض خطيرة (مثل ألم حاد في الصدر)، أظهر تحذيراً فورياً وتوجيه للطوارئ دون اقتراح أدوية.
"""

@app.route('/')
def home():
    # هيفتح صفحة الواجهة الرئيسية علطول بدون تعقيد تسجيل الدخول حالياً
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    symptom = request.form.get('symptom')
    country = request.form.get('country')
    
    # هنخلي الحساب Premium افتراضياً عشان يشتغل بكامل قوته والسرش الحي
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3,
        tools=[{"google_search": {}}] # سرش حي ومستمر
    )
    prompt = f"المريض من دولة ({country}). يشتكي من: ({symptom}). حلل أجهزة الجسم المصابة بناءً على جايتون وأكسفورد، وابحث عبر الإنترنت عن الأدوية التجارية المتاحة حالياً وبدائلها والمادة الفعالة مع مراعاة النواقص."

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=config,
    )
    
    # تصليح القفلة وتمرير النتيجة للـ index.html صح
    return render_template('index.html', result=response.text)

if __name__ == '__main__':
    # السطر ده بيقرأ البورت من Railway أوتوماتيك ويفتح السيرفر صح للكل
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
