from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

p = Path("index.html")
if not p.exists():
    print("❌ مش لاقي index.html في المجلد الحالي.")
    sys.exit(1)

s = p.read_text(encoding="utf-8")

if "id=\"carPreview\"" in s:
    print("ℹ️ معاينة العربية موجودة بالفعل؛ لم يتم تعديل أي شيء.")
    sys.exit(0)

checks = [
    ("اختيار الألوان", "playerColor"),
    ("لوحة الألوان", "#17b879"),
    ("لوحة الرسم", "const c=document.getElementById('game')"),
    ("دالة رسم العربية", "function drawCar("),
]
for name, marker in checks:
    if marker not in s:
        print(f"❌ لم أجد {name}. لم يتم تعديل الملف.")
        sys.exit(1)

backup = Path("backup-before-preview-" +
              datetime.now().strftime("%Y%m%d-%H%M%S") + ".html")
shutil.copy2(p, backup)

# إضافة معاينة صغيرة داخل قائمة البداية.
style = """
#carPreviewWrap{
  width:min(250px,85%); margin:14px auto 12px;
  padding:12px; border:1px solid #ffffff25;
  border-radius:18px;
  background:linear-gradient(145deg,#18232cdd,#080d13ee);
  box-shadow:0 8px 25px #0005;
}
#carPreviewTitle{font-size:12px;color:#aab9c8;margin-bottom:7px}
#carPreview{display:block;width:100%;height:105px}
#carPreviewCaption{font-size:12px;color:#dbe6ef;margin-top:4px}
"""
if "</style>" not in s:
    print("❌ لم أجد نهاية قسم CSS. النسخة الأصلية محفوظة ولم يتغير الملف.")
    sys.exit(1)
s = s.replace("</style>", style + "\n</style>", 1)

preview = """
<div id="carPreviewWrap">
  <div id="carPreviewTitle">معاينة سيارتك</div>
  <canvas id="carPreview" width="240" height="105"></canvas>
  <div id="carPreviewCaption">اختار لونك وانطلق!</div>
</div>
"""
start = s.find('<div id="overlay">')
button = s.find('<button id="start"', start)
if start < 0 or button < 0:
    print("❌ لم أجد قائمة البداية بالشكل المتوقع. لم يتم حفظ التعديلات.")
    sys.exit(1)
s = s[:button] + preview + s[button:]

# رسم سيارة مصغرة باستخدام اللون المختار.
script = r"""
(function(){
  const preview = document.getElementById('carPreview');
  if (!preview) return;
  const pc = preview.getContext('2d');

  function paintPreview(){
    const color = typeof playerColor !== 'undefined'
      ? playerColor : '#17b879';
    pc.clearRect(0,0,240,105);

    const glow = pc.createRadialGradient(120,54,5,120,54,65);
    glow.addColorStop(0,color+'55');
    glow.addColorStop(1,'#00000000');
    pc.fillStyle=glow;
    pc.fillRect(0,0,240,105);

    pc.fillStyle='#05090e';
    pc.beginPath();
    pc.ellipse(120,55,33,43,0,0,Math.PI*2);
    pc.fill();

    // عجلات
    pc.fillStyle='#080a0e';
    [[91,31],[143,31],[91,66],[143,66]].forEach(([x,y])=>{
      pc.fillRect(x,y,7,19);
    });

    // جسم السيارة
    pc.fillStyle=color;
    pc.beginPath();
    pc.moveTo(105,15); pc.quadraticCurveTo(120,7,135,15);
    pc.lineTo(145,34); pc.lineTo(141,76);
    pc.quadraticCurveTo(120,91,99,76);
    pc.lineTo(95,34); pc.closePath(); pc.fill();

    // الزجاج
    pc.fillStyle='#152b3d';
    pc.beginPath();
    pc.moveTo(108,24); pc.lineTo(132,24);
    pc.lineTo(137,39); pc.lineTo(103,39);
    pc.closePath(); pc.fill();

    pc.fillStyle='#243c50';
    pc.beginPath();
    pc.moveTo(103,48); pc.lineTo(137,48);
    pc.lineTo(134,64); pc.lineTo(106,64);
    pc.closePath(); pc.fill();

    // انعكاس على جسم السيارة
    pc.strokeStyle='#ffffffa8'; pc.lineWidth=2;
    pc.beginPath(); pc.moveTo(108,44); pc.lineTo(107,58);
    pc.stroke();

    // المصابيح الأمامية
    pc.fillStyle='#eaf8ff';
    pc.fillRect(102,13,9,4); pc.fillRect(129,13,9,4);

    // مصابيح خلفية
    pc.fillStyle='#ff3e48';
    pc.fillRect(102,76,9,4); pc.fillRect(129,76,9,4);
  }

  paintPreview();

  document.querySelectorAll('[data-car-color]').forEach(btn=>{
    btn.addEventListener('click', paintPreview);
  });
})();
"""
# إضافة المعاينة بعد تعريف playerColor وقبل بدء التشغيل.
marker = "let playerColor='#17b879';"
if marker not in s:
    print("❌ لم أجد تعريف لون السيارة. النسخة الأصلية محفوظة ولم يتم حفظ التعديل.")
    sys.exit(1)

s = s.replace(marker, marker + "\n" + script, 1)

# ربط أزرار الألوان بالمعاينة إن كانت أزرار اللون تستخدم ألوان CSS مباشرة.
# المعاينة تُحدّث عند الضغط على زر اللون من خلال حدث مستقل آمن.
s = s.replace(
    "document.querySelectorAll('[data-car-color]').forEach(btn=>{",
    "document.querySelectorAll('[data-car-color]').forEach(btn=>{"
)

p.write_text(s, encoding="utf-8")
print("✅ تمت إضافة معاينة السيارة.")
print("📦 النسخة الاحتياطية:", backup)
print("➡️ حدّث صفحة اللعبة في المتصفح واختبر اختيار الألوان.")
