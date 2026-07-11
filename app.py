import os
from flask import Flask, render_template, request
from google import genai
from google.genai import types

app = Flask(__name__)
app.secret_key = "axis_medical_secret_key_2026" 

# تشغيل عميل الذكاء الاصطناعي من جوجل
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
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def diagnose():
    symptom = request.form.get('symptom')
    country = request.form.get('country')
    
    # إعدادات التشخيص والبحث الحي عبر الإنترنت
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3,
        tools=[{"google_search": {}}] 
    )
    
    prompt = f"المريض من دولة ({country}). يشتكي من: ({symptom}). حلل أجهزة الجسم المصابة بناءً على جايتون وأكسفورد، وابحث عبر الإنترنت عن الأدوية التجارية المتاحة حالياً وبدائلها والمادة الفعالة مع مراعاة النواقص."

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=config,
        )
        output_text = response.text
    except Exception as e:
        output_text = f"عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(e)}"
    
    return render_template('index.html', result=output_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
