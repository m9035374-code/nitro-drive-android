from pathlib import Path
from datetime import datetime
import shutil
import sys

p = Path("index.html")
html = p.read_text(encoding="utf-8")

marker = "NITRO_SPEEDOMETER_V1"
if marker in html:
    sys.exit("عداد السرعة الجديد موجود بالفعل، مفيش تعديل اتعمل.")

old = '<div class="stat"><small>السرعة</small><strong><span id="speed">80</span></strong><small>كم/س</small></div>'

if old not in html:
    sys.exit("مش لاقي سطر السرعة المتوقع. الملف لم يتغير.")

if "</style>" not in html:
    sys.exit("مش لاقي نهاية قسم CSS. الملف لم يتغير.")

backup = Path("backup-speedometer-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".html")
shutil.copy2(p, backup)

new_html = '''<div class="stat speed-stat">
  <div class="speed-ring">
    <small>السرعة</small>
    <strong><span id="speed">80</span></strong>
    <small>كم/س</small>
  </div>
</div>'''

css = '''
/* NITRO_SPEEDOMETER_V1 */
.speed-stat {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}
.speed-ring {
  width: 88px;
  height: 88px;
  box-sizing: border-box;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  border: 3px solid #35eaff;
  background: radial-gradient(circle, #123346 0%, #07131f 72%);
  box-shadow: 0 0 12px #00d9ff88, inset 0 0 12px #00d9ff33;
  color: #fff;
}
.speed-ring small {
  font-size: 10px;
  line-height: 1.2;
  color: #9defff;
}
.speed-ring strong {
  font-size: 25px;
  line-height: 1.05;
  font-weight: 900;
  color: #fff;
  text-shadow: 0 0 9px #00d9ff;
}
@media (max-width: 360px) {
  .speed-ring { width: 76px; height: 76px; }
  .speed-ring strong { font-size: 22px; }
}
'''

html = html.replace(old, new_html, 1)
html = html.replace("</style>", css + "\n</style>", 1)
p.write_text(html, encoding="utf-8")

print("✅ تم تطوير عداد السرعة الدائري!")
print("🛡️ النسخة الاحتياطية:", backup)
print("🏁 تم الحفاظ على id السرعة، فالتحديث التلقائي مستمر.")
