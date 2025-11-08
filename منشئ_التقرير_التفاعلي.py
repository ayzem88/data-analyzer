# -*- coding: utf-8 -*-
"""
منشئ التقرير التفاعلي - يجمع جميع النتائج في ملف HTML واحد
"""

import os
import json
from datetime import datetime

class منشئ_التقرير_التفاعلي:
    def __init__(self, مجلد_النتائج="نتائج_التحليل"):
        self.مجلد_النتائج = مجلد_النتائج
        self.ملف_النتيجة = "التقرير_التفاعلي_الشامل.html"
        
    def قراءة_ملف_txt(self, اسم_الملف):
        """قراءة محتوى ملف txt"""
        مسار_الملف = os.path.join(self.مجلد_النتائج, f"{اسم_الملف}.txt")
        try:
            with open(مسار_الملف, 'r', encoding='utf-8') as ملف:
                return ملف.read()
        except FileNotFoundError:
            return f"الملف {اسم_الملف}.txt غير موجود"
    
    def قراءة_أول_سطور(self, اسم_الملف, عدد_السطور=20):
        """قراءة أول سطور من ملف txt"""
        مسار_الملف = os.path.join(self.مجلد_النتائج, f"{اسم_الملف}.txt")
        try:
            with open(مسار_الملف, 'r', encoding='utf-8') as ملف:
                سطور = []
                for i, سطر in enumerate(ملف):
                    if i >= عدد_السطور:
                        break
                    سطور.append(سطر.strip())
                return '\n'.join(سطور)
        except FileNotFoundError:
            return f"الملف {اسم_الملف}.txt غير موجود"
    
    def تحويل_نص_إلى_html(self, نص):
        """تحويل النص إلى HTML مع الحفاظ على التنسيق"""
        return نص.replace('\n', '<br>').replace(' ', '&nbsp;')
    
    def استخراج_عدد_من_ملف(self, محتوى_الملف):
        """استخراج عدد العناصر من محتوى الملف"""
        if "غير موجود" in محتوى_الملف:
            return 0
        
        # حساب عدد السطور التي تحتوي على ":" (تطابقات)
        سطور_مطابقة = [سطر for سطر in محتوى_الملف.split('\n') if ':' in سطر and not سطر.startswith('===')]
        return len(سطور_مطابقة)
    
    def إنشاء_قسم_إحصائيات_عامة(self):
        """إنشاء قسم الإحصائيات العامة"""
        إحصائيات_الكلمات = self.قراءة_ملف_txt("إحصائيات_الكلمات")
        إحصائيات_المركبات = self.قراءة_ملف_txt("إحصائيات_المركبات")
        
        html = """
        <div class="section">
            <h2>📊 الإحصائيات العامة</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>📝 الكلمات</h3>
                    <div class="stat-content">
        """
        
        # استخراج الإحصائيات من النص
        for سطر in إحصائيات_الكلمات.split('\n'):
            if 'إجمالي عدد الكلمات:' in سطر:
                html += f"<p><strong>إجمالي الكلمات:</strong> {سطر.split(':')[1].strip()}</p>"
            elif 'عدد الكلمات الفريدة:' in سطر:
                html += f"<p><strong>الكلمات الفريدة:</strong> {سطر.split(':')[1].strip()}</p>"
            elif 'أكثر كلمة تكراراً:' in سطر:
                html += f"<p><strong>أكثر كلمة:</strong> {سطر.split(':')[1].strip()}</p>"
            elif 'متوسط طول الكلمات:' in سطر:
                html += f"<p><strong>متوسط الطول:</strong> {سطر.split(':')[1].strip()}</p>"
        
        html += """
                    </div>
                </div>
                <div class="stat-card">
                    <h3>🔗 المركبات</h3>
                    <div class="stat-content">
        """
        
        for سطر in إحصائيات_المركبات.split('\n'):
            if 'إجمالي عدد المركبات:' in سطر:
                html += f"<p><strong>إجمالي المركبات:</strong> {سطر.split(':')[1].strip()}</p>"
            elif 'عدد المركبات الفريدة:' in سطر:
                html += f"<p><strong>المركبات الفريدة:</strong> {سطر.split(':')[1].strip()}</p>"
            elif 'عدد المركبات المختارة:' in سطر:
                html += f"<p><strong>المركبات المختارة:</strong> {سطر.split(':')[1].strip()}</p>"
        
        html += """
                    </div>
                </div>
                <div class="stat-card">
                    <h3>🏷️ الكيانات</h3>
                    <div class="stat-content">
        """
        
        # قراءة إحصائيات الكيانات
        أسماء_وأعلام = self.قراءة_ملف_txt("الأسماء_والأعلام")
        دول_ومدن = self.قراءة_ملف_txt("الدول_والمدن")
        مؤسسات_ومنظمات = self.قراءة_ملف_txt("المؤسسات_والمنظمات")
        تواريخ_وأماكن = self.قراءة_ملف_txt("التواريخ_والأماكن")
        
        # استخراج الأرقام
        عدد_الأسماء = self.استخراج_عدد_من_ملف(أسماء_وأعلام)
        عدد_الأماكن = self.استخراج_عدد_من_ملف(دول_ومدن)
        عدد_المؤسسات = self.استخراج_عدد_من_ملف(مؤسسات_ومنظمات)
        عدد_التواريخ = self.استخراج_عدد_من_ملف(تواريخ_وأماكن)
        
        html += f"""
                        <p><strong>الأسماء والأعلام:</strong> {عدد_الأسماء:,}</p>
                        <p><strong>الدول والمدن:</strong> {عدد_الأماكن:,}</p>
                        <p><strong>المؤسسات:</strong> {عدد_المؤسسات:,}</p>
                        <p><strong>التواريخ:</strong> {عدد_التواريخ:,}</p>
                    </div>
                </div>

            </div>
        </div>
        """
        
        return html
    
    def إنشاء_قسم_الكلمات_المهمة(self):
        """إنشاء قسم الكلمات المهمة"""
        html = """
        <div class="section">
            <h2>📝 الكلمات الأكثر تكراراً</h2>
            <div class="content-box">
        """
        
        # قراءة أول 20 كلمة من ملف التكرار
        تكرار_الكلمات = self.قراءة_أول_سطور("تكرار_الكلمات", 20)
        
        html += '<div class="word-cloud">'
        for سطر in تكرار_الكلمات.split('\n'):
            if ':' in سطر:
                كلمة, تكرار = سطر.split(':', 1)
                كلمة = كلمة.strip()
                تكرار = تكرار.strip()
                try:
                    تكرار_رقم = int(تكرار)
                    حجم = min(48, max(12, تكرار_رقم // 100 + 12))  # حجم الخط حسب التكرار
                    html += f'<span class="word" style="font-size: {حجم}px;">{كلمة}</span>'
                except:
                    continue
        
        html += """
                </div>
            </div>
        </div>
        """
        
        return html
    
    def إنشاء_قسم_المركبات_المختارة(self):
        """إنشاء قسم المركبات المختارة"""
        html = """
        <div class="section">
            <h2>🔗 المركبات المختارة تركيبياً</h2>
            <div class="content-box">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>المرتبة</th>
                            <th>المركب</th>
                            <th>PMI</th>
                            <th>التصنيف</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # قراءة المركبات المختارة
        مركبات_مختارة = self.قراءة_أول_سطور("المركبات_المختارة_تركيبياً", 50)
        
        مرتبة = 1
        for سطر in مركبات_مختارة.split('\n'):
            if '|' in سطر and 'المركب' not in سطر and '---' not in سطر:
                أجزاء = سطر.split('|')
                if len(أجزاء) >= 8:
                    مركب = أجزاء[0].strip()
                    pmi = أجزاء[4].strip()
                    تصنيف = أجزاء[7].strip()
                    
                    html += f"""
                        <tr>
                            <td>{مرتبة}</td>
                            <td>{مركب}</td>
                            <td>{pmi}</td>
                            <td>{تصنيف}</td>
                        </tr>
                    """
                    مرتبة += 1
                    if مرتبة > 20:  # عرض أول 20 مركب فقط
                        break
        
        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """
        
        return html
    

    
    def إنشاء_قسم_الكيانات(self):
        """إنشاء قسم الكيانات المسماة"""
        html = """
        <div class="section">
            <h2>🏷️ الكيانات المسماة</h2>
            <div class="entities-grid">
                <div class="entity-card">
                    <h3>👤 الأسماء والأعلام</h3>
                    <div class="entity-list">
        """
        
        # قراءة أول 10 أسماء
        أسماء = self.قراءة_أول_سطور("الأسماء_والأعلام", 10)
        for سطر in أسماء.split('\n'):
            if ':' in سطر and 'الاسم' not in سطر and '---' not in سطر:
                اسم, تكرار = سطر.split(':', 1)
                html += f'<span class="entity-item">{اسم.strip()}</span>'
        
        html += """
                    </div>
                </div>
                <div class="entity-card">
                    <h3>🌍 الدول والمدن</h3>
                    <div class="entity-list">
        """
        
        # قراءة أول 10 أماكن
        أماكن = self.قراءة_أول_سطور("الدول_والمدن", 10)
        for سطر in أماكن.split('\n'):
            if ':' in سطر and 'المكان' not in سطر and '---' not in سطر:
                مكان, تكرار = سطر.split(':', 1)
                html += f'<span class="entity-item">{مكان.strip()}</span>'
        
        html += """
                    </div>
                </div>
                <div class="entity-card">
                    <h3>🏢 المؤسسات والمنظمات</h3>
                    <div class="entity-list">
        """
        
        # قراءة أول 10 مؤسسات
        مؤسسات = self.قراءة_أول_سطور("المؤسسات_والمنظمات", 10)
        for سطر in مؤسسات.split('\n'):
            if ':' in سطر and 'المؤسسة' not in سطر and '---' not in سطر:
                مؤسسة, تكرار = سطر.split(':', 1)
                html += f'<span class="entity-item">{مؤسسة.strip()}</span>'
        
        html += """
                    </div>
                </div>
                <div class="entity-card">
                    <h3>📅 التواريخ والأماكن</h3>
                    <div class="entity-list">
        """
        
        # قراءة أول 10 تواريخ
        تواريخ = self.قراءة_أول_سطور("التواريخ_والأماكن", 10)
        for سطر in تواريخ.split('\n'):
            if ':' in سطر and 'التاريخ' not in سطر and '---' not in سطر:
                تاريخ, تكرار = سطر.split(':', 1)
                html += f'<span class="entity-item">{تاريخ.strip()}</span>'
        
        html += """
                    </div>
                </div>
            </div>
        </div>
        """
        
        return html
    
    def إنشاء_التقرير_الكامل(self):
        """إنشاء التقرير التفاعلي الكامل"""
        html = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التقرير التفاعلي الشامل - محلل الكتب</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        
        .section:last-child {{
            border-bottom: none;
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        .stat-content p {{
            margin: 8px 0;
            color: #555;
        }}
        
        .content-box {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
        }}
        
        .word-cloud {{
            text-align: center;
            line-height: 2;
        }}
        
        .word {{
            display: inline-block;
            margin: 5px;
            padding: 5px 10px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .word:hover {{
            background: #764ba2;
            transform: scale(1.1);
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .data-table th,
        .data-table td {{
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }}
        
        .data-table th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        .data-table tr:hover {{
            background: #e3f2fd;
        }}
        

            margin-bottom: 15px;
        }}
        

        
        .entities-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .entity-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}
        
        .entity-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
        }}
        
        .entity-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .entity-item {{
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            

            
            .entities-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 التقرير التفاعلي الشامل</h1>
            <p>محلل الكتب العربية - نتائج التحليل الشامل</p>
            <p>تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        {self.إنشاء_قسم_إحصائيات_عامة()}
        {self.إنشاء_قسم_الكلمات_المهمة()}
        {self.إنشاء_قسم_المركبات_المختارة()}
        {self.إنشاء_قسم_الكيانات()}
        
        <div class="footer">
            <p>تم إنشاء هذا التقرير بواسطة محلل الكتب الشامل</p>
            <p>جميع النتائج محفوظة في ملفات txt في مجلد نتائج_التحليل</p>
        </div>
    </div>
</body>
</html>
        """
        
        # حفظ التقرير
        with open(self.ملف_النتيجة, 'w', encoding='utf-8') as ملف:
            ملف.write(html)
        
        print(f"تم إنشاء التقرير التفاعلي: {self.ملف_النتيجة}")

def main():
    print("إنشاء التقرير التفاعلي الشامل...")
    منشئ = منشئ_التقرير_التفاعلي()
    منشئ.إنشاء_التقرير_الكامل()
    print("تم إنشاء التقرير بنجاح!")

if __name__ == "__main__":
    main()
