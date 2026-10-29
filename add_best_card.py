from pathlib import Path
from datetime import datetime
import shutil
import sys

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if 'id="menuBest"' in s:
    print("البطاقة موجودة بالفعل؛ لم يتم تعديل شيء.")
    sys.exit(0)

message = '<p id="message">'
endgame = "  $('overlay').style.display='flex';"

if message not in s or "function endGame(){" not in s:
    print("لم أجد العناصر المطلوبة. لم يتم تعديل الملف.")
    sys.exit(1)

# تأكد من وجود سطر إظهار القائمة داخل endGame تحديدًا
start = s.index("function endGame(){")
end = s.find("\n}", start)
if end < 0 or endgame not in s[start:end]:
    print("شكل دالة نهاية السباق مختلف. لم يتم تعديل الملف.")
    sys.exit(1)

backup = Path(
    "backup-best-card-" +
    datetime.now().strftime("%Y%m%d-%H%M%S") + ".html"
)
shutil.copy2(p, backup)

card = """
<div id="menuBest" style="
  margin:12px auto;padding:12px 20px;
  max-width:250px;border:1px solid #48e0a066;
  border-radius:14px;background:linear-gradient(135deg,#142c2a,#101820);
  color:#8fffd0;font-weight:700;font-size:15px;
  box-shadow:0 0 18px #17b87922">
  🏆 أفضل نتيجة شخصية: 0
</div>
"""

s = s.replace(message, card + "\n" + message, 1)

# استرجاع النتيجة المحفوظة إن لم يكن الكود يسترجعها بالفعل
if "localStorage.getItem('roadrush-best')" not in s:
    marker = "let best=0;"
    if marker not in s:
        print("لم أجد تعريف أفضل نتيجة. لم يتم تعديل الملف.")
        sys.exit(1)
    s = s.replace(
        marker,
        marker + """
try {
  best = Number(localStorage.getItem('roadrush-best')) || 0;
  $('best').textContent = best;
} catch(e) {}
""",
        1
    )

# تحديث البطاقة عند انتهاء السباق
start = s.index("function endGame(){")
end = s.find("\n}", start)
part = s[start:end]
part = part.replace(
    endgame,
    "  $('menuBest').textContent='🏆 أفضل نتيجة شخصية: '+best+' نقطة';\n"
    + endgame,
    1
)
s = s[:start] + part + s[end:]

# عرض النتيجة الحالية في القائمة منذ بداية تشغيل الصفحة
marker = "player={x:195,y:500};"
if marker not in s:
    print("لم أجد تهيئة السيارة الأخيرة. لم يتم تعديل الملف.")
    sys.exit(1)

s = s.replace(
    marker,
    marker + "\n"
    + "if($('menuBest')) $('menuBest').textContent='🏆 أفضل نتيجة شخصية: '+best+' نقطة';",
    1
)

p.write_text(s, encoding="utf-8")
print("تمت إضافة بطاقة أفضل نتيجة بنجاح.")
print("النسخة الاحتياطية:", backup)
print("حدّث صفحة اللعبة لاختبار التعديل.")
