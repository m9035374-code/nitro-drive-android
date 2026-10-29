from pathlib import Path
from datetime import datetime
import shutil
import sys

p = Path("index.html")
s = p.read_text(encoding="utf-8")

marker = "  // Sport tyres"
if "NITRO_FLAME_EFFECT" in s:
    print("تأثير النيترو موجود بالفعل؛ لم يتم تعديل شيء.")
    sys.exit(0)

if marker not in s or "function drawCar(" not in s:
    print("لم أجد مكان التعديل المتوقع. الملف لم يتغير.")
    sys.exit(1)

backup = Path(
    "backup-nitro-flame-" +
    datetime.now().strftime("%Y%m%d-%H%M%S") + ".html"
)
shutil.copy2(p, backup)

effect = """
  // NITRO_FLAME_EFFECT: animated blue exhaust
  if (isPlayer && typeof nitroFrames !== 'undefined' && nitroFrames > 0) {
    const pulse = 0.8 + 0.2 * Math.sin(performance.now() / 45);

    ctx.save();
    ctx.globalAlpha = pulse;
    ctx.shadowColor = '#20cfff';
    ctx.shadowBlur = 18;

    const flame = ctx.createLinearGradient(0, 58, 0, 101);
    flame.addColorStop(0, '#eaffff');
    flame.addColorStop(0.25, '#31eaff');
    flame.addColorStop(0.65, '#168bff');
    flame.addColorStop(1, 'rgba(25,80,255,0)');

    ctx.fillStyle = flame;
    ctx.beginPath();
    ctx.moveTo(-7, 57);
    ctx.quadraticCurveTo(-13, 73, -5, 94);
    ctx.lineTo(0, 84 + 5 * pulse);
    ctx.lineTo(5, 94);
    ctx.quadraticCurveTo(13, 73, 7, 57);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
  }

"""

s = s.replace(marker, effect + marker, 1)
p.write_text(s, encoding="utf-8")

print("تمت إضافة لهب النيترو بنجاح.")
print("النسخة الاحتياطية:", backup)
print("حدّث صفحة اللعبة واختبر زر النيترو.")
